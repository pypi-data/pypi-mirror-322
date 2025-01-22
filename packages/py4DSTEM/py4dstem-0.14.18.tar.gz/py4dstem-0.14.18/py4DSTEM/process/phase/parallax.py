"""
Module for reconstructing virtual parallax (also known as tilted-shifted bright field)
images by aligning each virtual BF image.
"""

import warnings
from typing import Mapping, Tuple

import matplotlib.pyplot as plt
import numpy as np
from emdfile import Array, Custom, Metadata, _read_metadata, tqdmnd
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import PercentFormatter
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from py4DSTEM import Calibration, DataCube
from py4DSTEM.preprocess.utils import get_shifted_ar
from py4DSTEM.process.phase.phase_base_class import PhaseReconstruction
from py4DSTEM.process.phase.utils import (
    AffineTransform,
    bilinear_kernel_density_estimate,
    bilinearly_interpolate_array,
    calculate_aberration_gradient_basis,
    generate_batches,
    lanczos_interpolate_array,
    lanczos_kernel_density_estimate,
    pixel_rolling_kernel_density_estimate,
    polar_aberrations_to_cartesian,
    polar_aliases,
    polar_symbols,
)
from py4DSTEM.process.utils.cross_correlate import align_images_fourier
from py4DSTEM.process.utils.utils import electron_wavelength_angstrom
from py4DSTEM.visualize import return_scaled_histogram_ordering
from scipy.linalg import polar
from scipy.ndimage import distance_transform_edt, shift
from scipy.special import comb

try:
    import cupy as cp
except (ModuleNotFoundError, ImportError):
    cp = np

_aberration_names = {
    (1, 0): "C1",
    (1, 2): "stig",
    (2, 1): "coma",
    (2, 3): "trefoil",
    (3, 0): "C3",
    (3, 2): "stig2",
    (3, 4): "quadfoil",
    (4, 1): "coma2",
    (4, 3): "trefoil2",
    (4, 5): "pentafoil",
    (5, 0): "C5",
    (5, 2): "stig3",
    (5, 4): "quadfoil2",
    (5, 6): "hexafoil",
}


class Parallax(PhaseReconstruction):
    """
    Iterative parallax reconstruction class.

    Parameters
    ----------
    datacube: DataCube
        Input 4D diffraction pattern intensities
    energy: float
        The electron energy of the wave functions in eV
    verbose: bool, optional
        If True, class methods will inherit this and print additional information
    device: str, optional
        Calculation device will be perfomed on. Must be 'cpu' or 'gpu'
    object_padding_px: Tuple[int,int], optional
        Pixel dimensions to pad object with
        If None, the padding is set to half the probe ROI dimensions
    polar_parameters: dict, optional
        Mapping from aberration symbols to their corresponding values. All aberration
        magnitudes should be given in Å and angles should be given in radians.
    device: str, optional
        Device calculation will be perfomed on. Must be 'cpu' or 'gpu'
    storage: str, optional
        Device non-frequent arrays will be stored on. Must be 'cpu' or 'gpu'
    clear_fft_cache: bool, optional
        If True, and device = 'gpu', clears the cached fft plan at the end of function calls
    name: str, optional
        Class name
    kwargs:
        Provide the aberration coefficients as keyword arguments.
    """

    def __init__(
        self,
        energy: float,
        datacube: DataCube = None,
        verbose: bool = True,
        object_padding_px: Tuple[int, int] = (32, 32),
        polar_parameters: Mapping[str, float] = None,
        device: str = "cpu",
        storage: str = None,
        clear_fft_cache: bool = True,
        name: str = "parallax_reconstruction",
        **kwargs,
    ):
        Custom.__init__(self, name=name)

        if storage is None:
            storage = device

        if storage != device:
            raise NotImplementedError()

        self.set_device(device, clear_fft_cache)
        self.set_storage(storage)

        for key in kwargs.keys():
            if (key not in polar_symbols) and (key not in polar_aliases.keys()):
                raise ValueError("{} not a recognized parameter".format(key))

        self._polar_parameters = dict(zip(polar_symbols, [0.0] * len(polar_symbols)))

        if polar_parameters is None:
            polar_parameters = {}

        polar_parameters.update(kwargs)
        self._set_polar_parameters(polar_parameters)
        self.set_save_defaults()

        # Data
        self._datacube = datacube

        # Metadata
        self._energy = energy
        self._verbose = verbose
        self._object_padding_px = object_padding_px
        self._preprocessed = False

    def to_h5(self, group):
        """
        Wraps datasets and metadata to write in emdfile classes,
        notably the (subpixel-)aligned BF.
        """
        # instantiation metadata
        self.metadata = Metadata(
            name="instantiation_metadata",
            data={
                "energy": self._energy,
                "verbose": self._verbose,
                "device": self._device,
                "object_padding_px": self._object_padding_px,
                "name": self.name,
            },
        )

        # preprocessing metadata
        self.metadata = Metadata(
            name="preprocess_metadata",
            data={
                "scan_sampling": self._scan_sampling,
                "wavelength": self._wavelength,
            },
        )

        # reconstruction metadata
        recon_metadata = {"reconstruction_error": float(self._recon_error)}

        if hasattr(self, "aberrations_C1"):
            recon_metadata |= {
                "aberrations_rotation_QR": self.rotation_Q_to_R_rads,
                "aberrations_transpose": self.transpose,
                "aberrations_C1": self.aberrations_C1,
                "aberrations_C12a": self.aberrations_C12a,
                "aberrations_C12b": self.aberrations_C12b,
            }

        if hasattr(self, "_kde_upsample_factor"):
            recon_metadata |= {
                "kde_upsample_factor": self._kde_upsample_factor,
            }
            self._subpixel_aligned_BF_emd = Array(
                name="subpixel_aligned_BF",
                data=self._asnumpy(self._recon_BF_subpixel_aligned),
            )

        if hasattr(self, "aberrations_dict_cartesian"):
            self.metadata = Metadata(
                name="aberrations_dict_polar",
                data=self.aberrations_dict_polar,
            )

            self.metadata = Metadata(
                name="aberrations_dict_cartesian",
                data=self.aberrations_dict_cartesian,
            )

        self.metadata = Metadata(
            name="reconstruction_metadata",
            data=recon_metadata,
        )

        self._aligned_BF_emd = Array(
            name="aligned_BF",
            data=self._asnumpy(self._recon_BF),
        )

        # datacube
        if self._save_datacube:
            self.metadata = self._datacube.calibration
            Custom.to_h5(self, group)
        else:
            dc = self._datacube
            self._datacube = None
            Custom.to_h5(self, group)
            self._datacube = dc

    @classmethod
    def _get_constructor_args(cls, group):
        """
        Returns a dictionary of arguments/values to pass
        to the class' __init__ function
        """
        # Get data
        dict_data = cls._get_emd_attr_data(cls, group)

        # Get metadata dictionaries
        instance_md = _read_metadata(group, "instantiation_metadata")

        # Fix calibrations bug
        if "_datacube" in dict_data:
            calibrations_dict = _read_metadata(group, "calibration")._params
            cal = Calibration()
            cal._params.update(calibrations_dict)
            dc = dict_data["_datacube"]
            dc.calibration = cal
        else:
            dc = None

        # Populate args and return
        kwargs = {
            "datacube": dc,
            "energy": instance_md["energy"],
            "object_padding_px": instance_md["object_padding_px"],
            "name": instance_md["name"],
            "verbose": True,  # for compatibility
            "device": "cpu",  # for compatibility
            "storage": "cpu",  # for compatibility
            "clear_fft_cache": True,  # for compatibility
        }

        return kwargs

    def _populate_instance(self, group):
        """
        Sets post-initialization properties, notably some preprocessing meta
        optional; during read, this method is run after object instantiation.
        """

        xp = self._xp

        # Preprocess metadata
        preprocess_md = _read_metadata(group, "preprocess_metadata")
        self._scan_sampling = preprocess_md["scan_sampling"]
        self._wavelength = preprocess_md["wavelength"]

        # Reconstruction metadata
        reconstruction_md = _read_metadata(group, "reconstruction_metadata")
        self._recon_error = reconstruction_md["reconstruction_error"]

        # Data
        dict_data = Custom._get_emd_attr_data(Custom, group)

        if "aberrations_C1" in reconstruction_md.keys:
            self.rotation_Q_to_R_rads = reconstruction_md["aberrations_rotation_QR"]
            self.transpose = reconstruction_md["aberrations_transpose"]
            self.aberrations_C1 = reconstruction_md["aberrations_C1"]
            self.aberrations_C12a = reconstruction_md["aberrations_C12a"]
            self.aberrations_C12b = reconstruction_md["aberrations_C12b"]

        if "kde_upsample_factor" in reconstruction_md.keys:
            self._kde_upsample_factor = reconstruction_md["kde_upsample_factor"]
            self._recon_BF_subpixel_aligned = xp.asarray(
                dict_data["_subpixel_aligned_BF_emd"].data, dtype=xp.float32
            )

        self._recon_BF = xp.asarray(dict_data["_aligned_BF_emd"].data, dtype=xp.float32)

    def _set_polar_parameters(self, parameters: dict):
        """
        Set the probe aberrations dictionary.

        Parameters
        ----------
        parameters: dict
            Mapping from aberration symbols to their corresponding values.
        """

        for symbol, value in parameters.items():
            if symbol in self._polar_parameters.keys():
                self._polar_parameters[symbol] = value

            elif symbol == "defocus":
                self._polar_parameters[polar_aliases[symbol]] = -value

            elif symbol in polar_aliases.keys():
                self._polar_parameters[polar_aliases[symbol]] = value

            else:
                raise ValueError("{} not a recognized parameter".format(symbol))

    def preprocess(
        self,
        edge_blend: float = 16.0,
        dp_mask: np.ndarray = None,
        threshold_intensity: float = 0.8,
        normalize_images: bool = True,
        normalize_order=0,
        descan_correction_fit_function: str = None,
        shifting_interpolation_order: int = 3,
        force_rotation_angle_deg: float = 0,
        force_transpose: bool = None,
        aligned_bf_image_guess: np.ndarray = None,
        plot_average_bf: bool = True,
        realspace_mask: np.ndarray = None,
        apply_realspace_mask_to_stack: bool = True,
        vectorized_com_calculation: bool = True,
        device: str = None,
        clear_fft_cache: bool = None,
        max_batch_size: int = None,
        store_initial_arrays: bool = True,
        **kwargs,
    ):
        """
        Iterative parallax reconstruction preprocessing method.

        Parameters
        ----------
        edge_blend: float, optional
            Number of pixels to blend image at the border
        dp_mask: np.ndarray, bool
            Bright-field pixels mask used for cross-correlation, boolean array same shape as DPs
        threshold: float, optional
            Fraction of max of dp_mean for bright-field pixels
        normalize_images: bool, optional
            If True, bright images normalized to have a mean of 1
        normalize_order: integer, optional
            Polynomial order for normalization. 0 means constant, 1 means linear, etc.
        aligned_bf_image_guess: np.ndarray, optional
            Guess for the reference BF image to cross-correlate against during the first iteration
            If None, the incoherent BF image is used instead.
        force_rotation_angle_deg: float, optional
            Initial guess of rotation value in degrees.
        force_transpose: bool, optional
            Whether or not the dataset should be transposed.
        descan_correction_fit_function: str, optional
            If not None, descan correction will be performed using fit function.
            One of "constant", "plane", "parabola", or "bezier_two".
        shifting_interpolation_order: int, optional
            Spline interpolation order used in shifting DPs to origin. Default is bi-cubic.
        plot_average_bf: bool, optional
            If True, plots the average bright field image, using defocus_guess
        realspace_mask: np.array, optional
            If this array is provided, pixels in real space set to false will be
            set to zero in the virtual bright field images.
        apply_realspace_mask_to_stack: bool, optional
            If this value is set to true, output BF images will be masked by
            the edge filter and realspace_mask if it is passed in.
        vectorized_com_calculation: bool, optional
            If True (default), the memory-intensive CoM calculation is vectorized
        device: str, optional
            if not none, overwrites self._device to set device preprocess will be perfomed on.
        clear_fft_cache: bool, optional
            If True, and device = 'gpu', clears the cached fft plan at the end of function calls
        max_batch_size: int, optional
            Max number of virtual BF images to use at once in computing cross-correlation
        store_initial_arrays: bool, optional
            If True, stores a copy of the arrays necessary to reinitialize in reconstruct

        Returns
        --------
        self: ParallaxReconstruction
            Self to accommodate chaining
        """

        # handle device/storage
        self.set_device(device, clear_fft_cache)

        xp = self._xp
        device = self._device
        asnumpy = self._asnumpy

        if self._datacube is None:
            raise ValueError(
                (
                    "The preprocess() method requires a DataCube. "
                    "Please run parallax.attach_datacube(DataCube) first."
                )
            )

        # extract calibrations
        intensities = self._extract_intensities_and_calibrations_from_datacube(
            self._datacube,
            require_calibrations=True,
        )

        intensities = xp.asarray(intensities)

        self._region_of_interest_shape = np.array(intensities.shape[-2:])
        self._scan_shape = np.array(intensities.shape[:2])

        # descan correction
        if descan_correction_fit_function is not None:
            (
                _,
                _,
                com_fitted_x,
                com_fitted_y,
                _,
                _,
            ) = self._calculate_intensities_center_of_mass(
                intensities,
                dp_mask=None,
                fit_function=descan_correction_fit_function,
                com_shifts=None,
                com_measured=None,
                vectorized_calculation=vectorized_com_calculation,
            )

            com_fitted_x = asnumpy(com_fitted_x)
            com_fitted_y = asnumpy(com_fitted_y)
            intensities_np = asnumpy(intensities)
            intensities_shifted = np.zeros_like(intensities_np)

            center_x = com_fitted_x.mean()
            center_y = com_fitted_y.mean()

            for rx in range(intensities_shifted.shape[0]):
                for ry in range(intensities_shifted.shape[1]):
                    if shifting_interpolation_order == 1:
                        # faster but may lead to gridding artifacts
                        intensities_shifted[rx, ry] = get_shifted_ar(
                            intensities_np[rx, ry].astype(np.float32),
                            -com_fitted_x[rx, ry] + center_x,
                            -com_fitted_y[rx, ry] + center_y,
                            bilinear=True,
                            device="cpu",
                        )
                    else:
                        intensities_shifted[rx, ry] = shift(
                            intensities_np[rx, ry].astype(np.float32),
                            (
                                -com_fitted_x[rx, ry] + center_x,
                                -com_fitted_y[rx, ry] + center_y,
                            ),
                            order=shifting_interpolation_order,
                            mode="grid-wrap",
                        )

            intensities = xp.asarray(intensities_shifted, xp.float32)

        if dp_mask is not None:
            self._dp_mask = xp.asarray(dp_mask)
        else:
            dp_mean = intensities.mean((0, 1))
            self._dp_mask = dp_mean >= (xp.max(dp_mean) * threshold_intensity)

        # select virtual detector pixels
        self._num_bf_images = int(xp.count_nonzero(self._dp_mask))
        self._wavelength = electron_wavelength_angstrom(self._energy)

        # diffraction space coordinates
        self._xy_inds = np.argwhere(self._dp_mask)
        self._kxy = xp.asarray(
            (self._xy_inds - xp.mean(self._xy_inds, axis=0)[None])
            * xp.array(self._reciprocal_sampling)[None],
            dtype=xp.float32,
        )
        self._probe_angles = self._kxy * self._wavelength
        self._kr = xp.sqrt(xp.sum(self._kxy**2, axis=1))

        # real space mask blending function
        if realspace_mask is not None:
            im_edge_dist = xp.array(distance_transform_edt(realspace_mask))
            self._window_mask = xp.minimum(im_edge_dist / edge_blend, 1.0)
            self._window_mask = xp.sin(self._window_mask * (np.pi / 2)) ** 2

        # edge window function
        x = xp.linspace(-1, 1, self._grid_scan_shape[0] + 1, dtype=xp.float32)[1:]
        x -= (x[1] - x[0]) / 2
        wx = (
            xp.sin(
                xp.clip(
                    (1 - xp.abs(x)) * self._grid_scan_shape[0] / edge_blend / 2, 0, 1
                )
                * (xp.pi / 2)
            )
            ** 2
        )
        y = xp.linspace(-1, 1, self._grid_scan_shape[1] + 1, dtype=xp.float32)[1:]
        y -= (y[1] - y[0]) / 2
        wy = (
            xp.sin(
                xp.clip(
                    (1 - xp.abs(y)) * self._grid_scan_shape[1] / edge_blend / 2, 0, 1
                )
                * (xp.pi / 2)
            )
            ** 2
        )
        self._window_edge = wx[:, None] * wy[None, :]

        # if needed, combine edge mask with the input real space mask
        if realspace_mask is not None:
            self._window_edge *= self._window_mask

        # derived window functions
        self._window_pad = xp.zeros(
            (
                self._grid_scan_shape[0] + self._object_padding_px[0],
                self._grid_scan_shape[1] + self._object_padding_px[1],
            ),
            dtype=xp.float32,
        )
        self._window_pad[
            self._object_padding_px[0] // 2 : self._grid_scan_shape[0]
            + self._object_padding_px[0] // 2,
            self._object_padding_px[1] // 2 : self._grid_scan_shape[1]
            + self._object_padding_px[1] // 2,
        ] = self._window_edge
        self._window_inv = 1 - self._window_edge
        self._window_inv_pad = 1 - self._window_pad

        # Collect BF images
        all_bfs = xp.moveaxis(
            intensities[:, :, self._xy_inds[:, 0], self._xy_inds[:, 1]],
            (0, 1, 2),
            (1, 2, 0),
        )

        # initialize
        stack_shape = (
            self._num_bf_images,
            self._grid_scan_shape[0] + self._object_padding_px[0],
            self._grid_scan_shape[1] + self._object_padding_px[1],
        )
        if normalize_images:
            self._normalized_stack = True
            self._stack_BF_shifted = xp.ones(stack_shape, dtype=xp.float32)
            self._stack_BF_unshifted = xp.ones(stack_shape, xp.float32)

            if normalize_order == 0:
                weights = xp.average(
                    all_bfs.reshape((self._num_bf_images, -1)),
                    weights=self._window_edge.ravel(),
                    axis=1,
                )
                all_bfs /= weights[:, None, None]

                self._stack_BF_shifted[
                    :,
                    self._object_padding_px[0] // 2 : self._grid_scan_shape[0]
                    + self._object_padding_px[0] // 2,
                    self._object_padding_px[1] // 2 : self._grid_scan_shape[1]
                    + self._object_padding_px[1] // 2,
                ] = (
                    self._window_inv[None] + self._window_edge[None] * all_bfs
                )

                if apply_realspace_mask_to_stack:
                    self._stack_BF_unshifted = self._stack_BF_shifted.copy()
                else:
                    self._stack_BF_unshifted[
                        :,
                        self._object_padding_px[0] // 2 : self._grid_scan_shape[0]
                        + self._object_padding_px[0] // 2,
                        self._object_padding_px[1] // 2 : self._grid_scan_shape[1]
                        + self._object_padding_px[1] // 2,
                    ] = all_bfs

            elif normalize_order == 1:
                x = xp.linspace(-0.5, 0.5, all_bfs.shape[1], xp.float32)
                y = xp.linspace(-0.5, 0.5, all_bfs.shape[2], xp.float32)
                ya, xa = xp.meshgrid(y, x)
                basis = np.vstack(
                    (
                        xp.ones_like(xa.ravel()),
                        xa.ravel(),
                        ya.ravel(),
                    )
                ).T
                weights = np.sqrt(self._window_edge).ravel()

                for a0 in range(all_bfs.shape[0]):
                    # weighted least squares
                    coefs = np.linalg.lstsq(
                        weights[:, None] * basis,
                        weights * all_bfs[a0].ravel(),
                        rcond=None,
                    )

                    self._stack_BF_shifted[
                        a0,
                        self._object_padding_px[0] // 2 : self._grid_scan_shape[0]
                        + self._object_padding_px[0] // 2,
                        self._object_padding_px[1] // 2 : self._grid_scan_shape[1]
                        + self._object_padding_px[1] // 2,
                    ] = self._window_inv[None] + self._window_edge[None] * all_bfs[
                        a0
                    ] / xp.reshape(
                        basis @ coefs[0], all_bfs.shape[1:3]
                    )

                    if apply_realspace_mask_to_stack:
                        self._stack_BF_unshifted = self._stack_BF_shifted.copy()
                    else:
                        self._stack_BF_unshifted[
                            a0,
                            self._object_padding_px[0] // 2 : self._grid_scan_shape[0]
                            + self._object_padding_px[0] // 2,
                            self._object_padding_px[1] // 2 : self._grid_scan_shape[1]
                            + self._object_padding_px[1] // 2,
                        ] = all_bfs[a0] / xp.reshape(
                            basis @ coefs[0], all_bfs.shape[1:3]
                        )

            elif normalize_order == 2:
                x = xp.linspace(-0.5, 0.5, all_bfs.shape[1], xp.float32)
                y = xp.linspace(-0.5, 0.5, all_bfs.shape[2], xp.float32)
                ya, xa = xp.meshgrid(y, x)
                basis = np.vstack(
                    (
                        1 * xa.ravel() ** 2 * ya.ravel() ** 2,
                        2 * xa.ravel() ** 2 * ya.ravel() * (1 - ya.ravel()),
                        1 * xa.ravel() ** 2 * (1 - ya.ravel()) ** 2,
                        2 * xa.ravel() * (1 - xa.ravel()) * ya.ravel() ** 2,
                        4
                        * xa.ravel()
                        * (1 - xa.ravel())
                        * ya.ravel()
                        * (1 - ya.ravel()),
                        2 * xa.ravel() * (1 - xa.ravel()) * (1 - ya.ravel()) ** 2,
                        1 * (1 - xa.ravel()) ** 2 * ya.ravel() ** 2,
                        2 * (1 - xa.ravel()) ** 2 * ya.ravel() * (1 - ya.ravel()),
                        1 * (1 - xa.ravel()) ** 2 * (1 - ya.ravel()) ** 2,
                    )
                ).T
                weights = np.sqrt(self._window_edge).ravel()

                for a0 in range(all_bfs.shape[0]):
                    # weighted least squares
                    coefs = np.linalg.lstsq(
                        weights[:, None] * basis,
                        weights * all_bfs[a0].ravel(),
                        rcond=None,
                    )

                    self._stack_BF_shifted[
                        a0,
                        self._object_padding_px[0] // 2 : self._grid_scan_shape[0]
                        + self._object_padding_px[0] // 2,
                        self._object_padding_px[1] // 2 : self._grid_scan_shape[1]
                        + self._object_padding_px[1] // 2,
                    ] = self._window_inv[None] + self._window_edge[None] * all_bfs[
                        a0
                    ] / xp.reshape(
                        basis @ coefs[0], all_bfs.shape[1:3]
                    )
                    if apply_realspace_mask_to_stack:
                        self._stack_BF_unshifted = self._stack_BF_shifted.copy()
                    else:
                        self._stack_BF_unshifted[
                            a0,
                            self._object_padding_px[0] // 2 : self._grid_scan_shape[0]
                            + self._object_padding_px[0] // 2,
                            self._object_padding_px[1] // 2 : self._grid_scan_shape[1]
                            + self._object_padding_px[1] // 2,
                        ] = all_bfs[a0] / xp.reshape(
                            basis @ coefs[0], all_bfs.shape[1:3]
                        )

        else:
            self._normalized_stack = False
            all_means = xp.mean(all_bfs, axis=(1, 2))
            self._stack_BF_shifted = xp.full(stack_shape, all_means[:, None, None])
            self._stack_BF_unshifted = xp.full(stack_shape, all_means[:, None, None])
            self._stack_BF_shifted[
                :,
                self._object_padding_px[0] // 2 : self._grid_scan_shape[0]
                + self._object_padding_px[0] // 2,
                self._object_padding_px[1] // 2 : self._grid_scan_shape[1]
                + self._object_padding_px[1] // 2,
            ] = (
                self._window_inv[None] * all_means[:, None, None]
                + self._window_edge[None] * all_bfs
            )
            if apply_realspace_mask_to_stack:
                self._stack_BF_unshifted = self._stack_BF_shifted.copy()
            else:
                self._stack_BF_unshifted[
                    :,
                    self._object_padding_px[0] // 2 : self._grid_scan_shape[0]
                    + self._object_padding_px[0] // 2,
                    self._object_padding_px[1] // 2 : self._grid_scan_shape[1]
                    + self._object_padding_px[1] // 2,
                ] = all_bfs

        # Fourier space operators for image shifts
        qx = xp.fft.fftfreq(self._stack_BF_shifted.shape[1], d=1)
        qx = xp.asarray(qx, dtype=xp.float32)

        qy = xp.fft.fftfreq(self._stack_BF_shifted.shape[2], d=1)
        qy = xp.asarray(qy, dtype=xp.float32)

        qxa, qya = xp.meshgrid(qx, qy, indexing="ij")
        self._qx_shift = -2j * xp.pi * qxa
        self._qy_shift = -2j * xp.pi * qya

        # Initialization utilities
        self._stack_mask = xp.tile(self._window_pad[None], (self._num_bf_images, 1, 1))

        if max_batch_size is None:
            max_batch_size = self._num_bf_images

        self._xy_shifts = xp.zeros((self._num_bf_images, 2), dtype=xp.float32)

        # aberrations_coefs
        aberrations_mn = []
        aberrations_coefs = []
        cartesian_dict = polar_aberrations_to_cartesian(self._polar_parameters)
        for key, val in cartesian_dict.items():
            if np.abs(val) > 0:
                m = int(key[1])
                n = int(key[2])
                a = 1 if n > 0 and key[3] != "a" else 0
                aberrations_mn.append([m, n, a])
                aberrations_coefs.append(val)

        if len(aberrations_mn) > 0:
            # aberrations_basis
            sampling = 1 / (
                np.array(self._reciprocal_sampling) * self._region_of_interest_shape
            )

            # transpose rotation matrix
            if force_transpose:
                force_rotation_angle_deg *= -1

            aberrations_basis, aberrations_basis_du, aberrations_basis_dv = (
                calculate_aberration_gradient_basis(
                    aberrations_mn,
                    sampling,
                    self._region_of_interest_shape,
                    self._wavelength,
                    rotation_angle=np.deg2rad(force_rotation_angle_deg),
                    xp=xp,
                )
            )

            # shifts
            corner_indices = self._xy_inds - xp.array(
                self._region_of_interest_shape // 2
            )
            raveled_indices = xp.ravel_multi_index(
                corner_indices.T, self._region_of_interest_shape, mode="wrap"
            )
            gradients = xp.array(
                (
                    aberrations_basis_du[raveled_indices, :],
                    aberrations_basis_dv[raveled_indices, :],
                )
            )

            aberrations_coefs = xp.asarray(aberrations_coefs, dtype=xp.float32)
            shifts_ang = xp.tensordot(gradients, aberrations_coefs, axes=1).T

            if force_transpose:
                shifts_ang = xp.flip(shifts_ang, axis=1)

            shifts_px = shifts_ang / xp.array(self._scan_sampling)

            for start, end in generate_batches(
                self._num_bf_images, max_batch=max_batch_size
            ):
                shifted_BFs = self._stack_BF_shifted[start:end]
                xy_shifts = shifts_px[start:end]
                stack_mask = self._stack_mask[start:end]

                Gs = xp.fft.fft2(shifted_BFs)

                dx = xy_shifts[:, 0]
                dy = xy_shifts[:, 1]

                shift_op = xp.exp(
                    self._qx_shift[None] * dx[:, None, None]
                    + self._qy_shift[None] * dy[:, None, None]
                )
                stack_BF_shifted = xp.real(xp.fft.ifft2(Gs * shift_op))
                stack_mask = xp.real(xp.fft.ifft2(xp.fft.fft2(stack_mask) * shift_op))

                self._xy_shifts[start:end] = xy_shifts
                self._stack_BF_shifted[start:end] = stack_BF_shifted
                self._stack_mask[start:end] = stack_mask

                del Gs

        self._stack_mean = xp.mean(self._stack_BF_shifted)
        self._mask_sum = xp.sum(self._window_edge) * self._num_bf_images
        self._recon_mask = xp.mean(self._stack_mask, axis=0)

        mask_inv = 1 - xp.clip(self._recon_mask, 0, 1)

        if aligned_bf_image_guess is not None:
            aligned_bf_image_guess = xp.asarray(aligned_bf_image_guess)
            if normalize_images:
                self._recon_BF = xp.ones(stack_shape[-2:], dtype=xp.float32)
                aligned_bf_image_guess /= aligned_bf_image_guess.mean()
            else:
                self._recon_BF = xp.full(stack_shape[-2:], self._stack_mean)

            self._recon_BF[
                self._object_padding_px[0] // 2 : self._grid_scan_shape[0]
                + self._object_padding_px[0] // 2,
                self._object_padding_px[1] // 2 : self._grid_scan_shape[1]
                + self._object_padding_px[1] // 2,
            ] = (
                self._window_inv * self._stack_mean
                + self._window_edge * aligned_bf_image_guess
            )

        else:

            self._recon_BF = (
                self._stack_mean * mask_inv
                + xp.mean(self._stack_BF_shifted * self._stack_mask, axis=0)
            ) / (self._recon_mask + mask_inv)

        self._recon_error = (
            xp.atleast_1d(
                xp.sum(
                    xp.abs(self._stack_BF_shifted - self._recon_BF[None])
                    * self._stack_mask
                )
            )
            / self._mask_sum
            / self._stack_mean
        )

        if store_initial_arrays:
            self._recon_BF_initial = self._recon_BF.copy()
            self._stack_BF_shifted_initial = self._stack_BF_shifted.copy()
            self._stack_mask_initial = self._stack_mask.copy()
            self._recon_mask_initial = self._recon_mask.copy()
            self._xy_shifts_initial = self._xy_shifts.copy()

        self.recon_BF = asnumpy(self._recon_BF)

        if plot_average_bf:
            figsize = kwargs.pop("figsize", (8, 4))
            fig, ax = plt.subplots(1, 2, figsize=figsize)

            self._visualize_figax(fig, ax[0], **kwargs)

            ax[0].set_ylabel("x [A]")
            ax[0].set_xlabel("y [A]")
            ax[0].set_title("Average Bright Field Image")

            reciprocal_extent = [
                -0.5 * (self._reciprocal_sampling[1] * self._dp_mask.shape[1]),
                0.5 * (self._reciprocal_sampling[1] * self._dp_mask.shape[1]),
                0.5 * (self._reciprocal_sampling[0] * self._dp_mask.shape[0]),
                -0.5 * (self._reciprocal_sampling[0] * self._dp_mask.shape[0]),
            ]
            ax[1].imshow(
                self._asnumpy(self._dp_mask), extent=reciprocal_extent, cmap="gray"
            )
            ax[1].set_title("DP mask")
            ax[1].set_ylabel(r"$k_x$ [$A^{-1}$]")
            ax[1].set_xlabel(r"$k_y$ [$A^{-1}$]")
            plt.tight_layout()

        self._preprocessed = True
        self.clear_device_mem(self._device, self._clear_fft_cache)

        return self

    def guess_common_aberrations(
        self,
        rotation_angle_deg=0,
        transpose=False,
        kde_upsample_factor=None,
        kde_sigma_px=0.125,
        kde_lowpass_filter=False,
        lanczos_interpolation_order=None,
        polar_parameters=None,
        max_batch_size=None,
        interpolation_max_batch_size=None,
        plot_shifts_and_aligned_bf=True,
        return_shifts_and_aligned_bf=False,
        plot_arrow_freq=1,
        scale_arrows=1,
        **kwargs,
    ):
        """
        Generates analytical BF shifts and uses them to align the virtual BF stack,
        based on the experimental geometry (rotation, transpose), and common aberrations.

        Parameters
        ----------
        rotation_angle_deg: float, optional
            Relative rotation between the scan and the diffraction space coordinate systems
        transpose: bool, optional
            Whether the diffraction intensities are transposed
        kde_upsample_factor: int, optional
            Real-space upsampling factor
        kde_sigma_px: float, optional
            KDE gaussian kernel bandwidth in non-upsampled pixels
        kde_lowpass_filter: bool, optional
            If True, the resulting KDE upsampled image is lowpass-filtered using a sinc-function
        lanczos_interpolation_order: int, optional
            If not None, Lanczos interpolation with the specified order is used instead of bilinear
        polar_parameters: dict, optional
            Mapping from aberration symbols to their corresponding values. All aberration
            magnitudes should be given in Å and angles should be given in radians.
        max_batch_size: int, optional
            Max number of virtual BF images to use at once in computing cross-correlation
        plot_shifts_and_aligned_bf: bool, optional
            If True, the analytical shifts and the aligned virtual VF image are plotted
        return_shifts_and_aligned_bf: bool, optional
            If True, the analytical shifts and the aligned virtual VF image are returned
        plot_arrow_freq: int, optional
            Frequency of shifts to plot in quiver plot
        scale_arrows: float, optional
            Scale to multiply shifts by
        interpolation_max_batch_size: int, optional
            Max number of pixels to use at once in upsampling (max is #BF * upsampled_pixels)
        kwargs:
            Provide the aberration coefficients as keyword arguments.
            kwargs which are not recognized as aberrations will be passed to the visualizations
        """
        xp = self._xp
        asnumpy = self._asnumpy

        if not hasattr(self, "_recon_BF"):
            raise ValueError(
                (
                    "Aberration guessing is meant to be ran after preprocessing. "
                    "Please run the `preprocess()` function first."
                )
            )

        aberrations_kwargs = kwargs.copy()
        plotting_kwargs = {}

        for key, val in kwargs.items():
            if (key not in polar_symbols) and (key not in polar_aliases.keys()):
                aberrations_kwargs.pop(key)
                plotting_kwargs[key] = val

        if polar_parameters is None:
            polar_parameters = {}

        polar_dict = self._polar_parameters.copy()  # copy init dict
        polar_dict |= polar_parameters  # merge with passed dict

        for symbol, value in aberrations_kwargs.items():
            if symbol in polar_dict.keys():
                polar_dict[symbol] = value
            elif symbol == "defocus":
                polar_dict[polar_aliases[symbol]] = -value
            elif symbol in polar_aliases.keys():
                polar_dict[polar_aliases[symbol]] = value
            else:
                raise ValueError("{} not a recognized parameter".format(symbol))

        aberrations_mn = []
        for symbol in polar_symbols:
            if symbol[0] == "C":
                if np.abs(polar_dict[symbol]) > 0:
                    _, m, n = symbol
                    aberrations_mn.append([int(m), int(n), 0])
                    if int(n) > 0:
                        aberrations_mn.append([int(m), int(n), 1])

        coeffs = []
        for m, n, a in aberrations_mn:
            mag = polar_dict.get(f"C{m}{n}")
            if n == 0:
                coeffs.append(mag)
            else:
                angle = polar_dict.get(f"phi{m}{n}")
                if a == 0:
                    coeffs.append(mag * np.cos(angle * n))
                else:
                    coeffs.append(mag * np.sin(angle * n))

        aberrations_coefs = xp.array(coeffs)

        # transpose rotation matrix
        if transpose:
            rotation_angle_deg *= -1

        # aberrations_basis
        sampling = 1 / (
            np.array(self._reciprocal_sampling) * self._region_of_interest_shape
        )
        (
            aberrations_basis,
            aberrations_basis_du,
            aberrations_basis_dv,
        ) = calculate_aberration_gradient_basis(
            aberrations_mn,
            sampling,
            self._region_of_interest_shape,
            self._wavelength,
            rotation_angle=np.deg2rad(rotation_angle_deg),
            xp=xp,
        )

        # shifts
        corner_indices = self._xy_inds - xp.array(self._region_of_interest_shape // 2)
        raveled_indices = xp.ravel_multi_index(
            corner_indices.T, self._region_of_interest_shape, mode="wrap"
        )
        gradients = xp.array(
            (
                aberrations_basis_du[raveled_indices, :],
                aberrations_basis_dv[raveled_indices, :],
            )
        )
        shifts_ang = xp.tensordot(gradients, aberrations_coefs, axes=1).T

        # transpose predicted shifts
        if transpose:
            shifts_ang = xp.flip(shifts_ang, axis=1)

        shifts_px = shifts_ang / xp.array(self._scan_sampling)

        # upsampled stack
        if kde_upsample_factor is not None:
            BF_size = np.array(self._stack_BF_unshifted.shape[-2:])
            pixel_output_shape = np.round(BF_size * kde_upsample_factor).astype("int")

            x = xp.arange(BF_size[0], dtype=xp.float32)
            y = xp.arange(BF_size[1], dtype=xp.float32)
            xa_init, ya_init = xp.meshgrid(x, y, indexing="ij")

            # kernel density output the upsampled BF image
            xa = (xa_init + shifts_px[:, 0, None, None]) * kde_upsample_factor
            ya = (ya_init + shifts_px[:, 1, None, None]) * kde_upsample_factor

            pix_output = self._kernel_density_estimate(
                xa,
                ya,
                self._stack_BF_unshifted,
                pixel_output_shape,
                kde_sigma_px * kde_upsample_factor,
                lanczos_alpha=lanczos_interpolation_order,
                lowpass_filter=kde_lowpass_filter,
                max_batch_size=interpolation_max_batch_size,
            )

            # hack since cropping requires "_kde_upsample_factor"
            old_upsample_factor = getattr(self, "_kde_upsample_factor", None)
            self._kde_upsample_factor = kde_upsample_factor
            cropped_image = asnumpy(
                self._crop_padded_object(pix_output, upsampled=True)
            )
            if old_upsample_factor is not None:
                self._kde_upsample_factor = old_upsample_factor
            else:
                del self._kde_upsample_factor

        # shifted stack
        else:
            kde_upsample_factor = 1
            aligned_stack = xp.zeros_like(self._stack_BF_shifted_initial[0])

            if max_batch_size is None:
                max_batch_size = self._num_bf_images

            for start, end in generate_batches(
                self._num_bf_images, max_batch=max_batch_size
            ):
                shifted_BFs = self._stack_BF_shifted_initial[start:end]

                Gs = xp.fft.fft2(shifted_BFs)

                dx = shifts_px[start:end, 0]
                dy = shifts_px[start:end, 1]

                shift_op = xp.exp(
                    self._qx_shift[None] * dx[:, None, None]
                    + self._qy_shift[None] * dy[:, None, None]
                )
                stack_BF_shifted = xp.real(xp.fft.ifft2(Gs * shift_op))
                aligned_stack += stack_BF_shifted.sum(0)

            cropped_image = asnumpy(
                self._crop_padded_object(aligned_stack, upsampled=False)
            )

        if plot_shifts_and_aligned_bf:
            figsize = plotting_kwargs.pop("figsize", (8, 4))
            color = plotting_kwargs.pop("color", (1, 0, 0, 1))
            cmap = plotting_kwargs.pop("cmap", "magma")

            fig, axs = plt.subplots(1, 2, figsize=figsize)

            self.show_shifts(
                shifts_ang=shifts_ang,
                plot_arrow_freq=plot_arrow_freq,
                scale_arrows=scale_arrows,
                plot_rotated_shifts=False,
                color=color,
                figax=(fig, axs[0]),
            )

            axs[0].set_title("Predicted BF Shifts")

            extent = [
                0,
                self._scan_sampling[1] * cropped_image.shape[1] / kde_upsample_factor,
                self._scan_sampling[0] * cropped_image.shape[0] / kde_upsample_factor,
                0,
            ]

            axs[1].imshow(cropped_image, cmap=cmap, extent=extent, **plotting_kwargs)
            axs[1].set_ylabel("x [A]")
            axs[1].set_xlabel("y [A]")
            axs[1].set_title("Predicted Aligned BF Image")

            fig.tight_layout()

        if return_shifts_and_aligned_bf:
            return shifts_ang, cropped_image

    def reconstruct(
        self,
        max_alignment_bin: int = None,
        min_alignment_bin: int = 1,
        num_iter_at_min_bin: int = 2,
        alignment_bin_values: list = None,
        centered_alignment_bins: bool = False,
        cross_correlation_upsample_factor: int = 8,
        regularizer_matrix_size: Tuple[int, int] = (1, 1),
        regularize_shifts: bool = False,
        running_average: bool = True,
        progress_bar: bool = True,
        plot_aligned_bf: bool = True,
        plot_convergence: bool = True,
        reset: bool = None,
        device: str = None,
        clear_fft_cache: bool = None,
        max_batch_size: int = None,
        **kwargs,
    ):
        """
        Iterative Parallax Reconstruction main reconstruction method.

        Parameters
        ----------
        max_alignment_bin: int, optional
            Maximum bin size for bright field alignment
            If None, the bright field disk radius is used
        min_alignment_bin: int, optional
            Minimum bin size for bright field alignment
        num_iter_at_min_bin: int, optional
            Number of iterations to run at the smallest bin size
        alignment_bin_values: list, optional
            If not None, explicitly sets the iteration bin values
        cross_correlation_upsample_factor: int, optional
            DFT upsample factor for subpixel alignment
        regularizer_matrix_size: Tuple[int,int], optional
            Bernstein basis degree used for regularizing shifts
        regularize_shifts: bool, optional
            If True, the cross-correlated shifts are constrained to a spline interpolation
        running_average: bool, optional
            If True, the bright field reference image is updated in a spiral from the origin
        progress_bar: bool, optional
            If True, progress bar is displayed
        plot_aligned_bf: bool, optional
            If True, the aligned bright field image is plotted at each bin level
        plot_convergence: bool, optional
            If True, the convergence error is also plotted
        reset: bool, optional
            If True, the reconstruction is reset
        device: str, optional
            if not none, overwrites self._device to set device preprocess will be perfomed on.
        max_batch_size: int, optional
            Max number of virtual BF images to use at once in computing cross-correlation
        clear_fft_cache: bool, optional
            if true, and device = 'gpu', clears the cached fft plan at the end of function calls

        Returns
        --------
        self: BFReconstruction
            Self to accommodate chaining
        """

        # handle device/storage
        self.set_device(device, clear_fft_cache)

        xp = self._xp
        asnumpy = self._asnumpy

        if reset:
            self.error_iterations = []
            self._recon_BF = self._recon_BF_initial.copy()
            self._stack_BF_shifted = self._stack_BF_shifted_initial.copy()
            self._stack_mask = self._stack_mask_initial.copy()
            self._recon_mask = self._recon_mask_initial.copy()
            self._xy_shifts = self._xy_shifts_initial.copy()

        elif reset is None:
            if hasattr(self, "error_iterations"):
                warnings.warn(
                    (
                        "Continuing reconstruction from previous result. "
                        "Use reset=True for a fresh start."
                    ),
                    UserWarning,
                )
            else:
                self.error_iterations = []

        if not regularize_shifts:
            self._basis = self._kxy
        else:
            kr_max = xp.max(self._kr)
            u = self._kxy[:, 0] * 0.5 / kr_max + 0.5
            v = self._kxy[:, 1] * 0.5 / kr_max + 0.5

            self._basis = xp.zeros(
                (
                    self._num_bf_images,
                    (regularizer_matrix_size[0] + 1) * (regularizer_matrix_size[1] + 1),
                ),
                dtype=xp.float32,
            )
            for ii in np.arange(regularizer_matrix_size[0] + 1):
                Bi = (
                    comb(regularizer_matrix_size[0], ii)
                    * (u**ii)
                    * ((1 - u) ** (regularizer_matrix_size[0] - ii))
                )

                for jj in np.arange(regularizer_matrix_size[1] + 1):
                    Bj = (
                        comb(regularizer_matrix_size[1], jj)
                        * (v**jj)
                        * ((1 - v) ** (regularizer_matrix_size[1] - jj))
                    )

                    ind = ii * (regularizer_matrix_size[1] + 1) + jj
                    self._basis[:, ind] = Bi * Bj

        # Iterative binning for more robust alignment
        diameter_pixels = int(
            xp.maximum(
                xp.max(self._xy_inds[:, 0]) - xp.min(self._xy_inds[:, 0]),
                xp.max(self._xy_inds[:, 1]) - xp.min(self._xy_inds[:, 1]),
            )
            + 1
        )

        if max_alignment_bin is not None:
            max_alignment_bin = np.minimum(diameter_pixels, max_alignment_bin)
        else:
            max_alignment_bin = diameter_pixels

        if alignment_bin_values is not None:
            bin_vals = np.array(alignment_bin_values).clip(1, max_alignment_bin)
        else:
            bin_min = np.ceil(np.log(min_alignment_bin) / np.log(2))
            bin_max = np.ceil(np.log(max_alignment_bin) / np.log(2))
            bin_vals = 2 ** np.arange(bin_min, bin_max)[::-1]

            if num_iter_at_min_bin > 1:
                bin_vals = np.hstack(
                    (bin_vals, np.repeat(bin_vals[-1], num_iter_at_min_bin - 1))
                )

        bin_shift = 0 if centered_alignment_bins else 0.5

        if plot_aligned_bf:
            num_plots = bin_vals.shape[0]
            nrows = int(np.sqrt(num_plots))
            ncols = int(np.ceil(num_plots / nrows))

            if plot_convergence:
                spec = GridSpec(
                    ncols=ncols,
                    nrows=nrows + 1,
                    hspace=0.15,
                    wspace=0.15,
                    height_ratios=[1] * nrows + [1 / 4],
                )

                figsize = kwargs.pop("figsize", (4 * ncols, 4 * nrows + 1))
            else:
                spec = GridSpec(
                    ncols=ncols,
                    nrows=nrows,
                    hspace=0.15,
                    wspace=0.15,
                )

                figsize = kwargs.pop("figsize", (4 * ncols, 4 * nrows))

            fig = plt.figure(figsize=figsize)

        xy_center = (self._xy_inds - xp.median(self._xy_inds, axis=0)).astype("float")

        if max_batch_size is None:
            max_batch_size = self._num_bf_images

        # Loop over all binning values
        for a0 in range(bin_vals.shape[0]):
            G_ref = xp.fft.fft2(self._recon_BF)

            # Segment the virtual images with current binning values
            xy_inds = xp.round(xy_center / bin_vals[a0] + bin_shift).astype("int")
            xy_vals = np.unique(
                asnumpy(xy_inds), axis=0
            )  # axis is not yet supported in cupy
            # Sort by radial order, from center to outer edge
            inds_order = xp.argsort(xp.sum(xy_vals**2, axis=1))

            shifts_update = xp.zeros((self._num_bf_images, 2), dtype=xp.float32)

            for a1 in tqdmnd(
                xy_vals.shape[0],
                desc="Alignment at bin " + str(bin_vals[a0].astype("int")),
                unit=" image subsets",
                disable=not progress_bar,
            ):
                ind_align = inds_order[a1]

                # Generate mean image for alignment
                sub = xp.logical_and(
                    xy_inds[:, 0] == xy_vals[ind_align, 0],
                    xy_inds[:, 1] == xy_vals[ind_align, 1],
                )

                G = xp.fft.fft2(xp.mean(self._stack_BF_shifted[sub], axis=0))

                # Get best fit alignment
                xy_shift = align_images_fourier(
                    G_ref,
                    G,
                    upsample_factor=cross_correlation_upsample_factor,
                    device=self._device,
                )

                dx = (
                    xp.mod(
                        xy_shift[0] + self._stack_BF_shifted.shape[1] / 2,
                        self._stack_BF_shifted.shape[1],
                    )
                    - self._stack_BF_shifted.shape[1] / 2
                )
                dy = (
                    xp.mod(
                        xy_shift[1] + self._stack_BF_shifted.shape[2] / 2,
                        self._stack_BF_shifted.shape[2],
                    )
                    - self._stack_BF_shifted.shape[2] / 2
                )

                # output shifts
                shifts_update[sub, 0] = dx
                shifts_update[sub, 1] = dy

                # update running estimate of reference image
                shift_op = xp.exp(self._qx_shift * dx + self._qy_shift * dy)

                if running_average:
                    G_ref = G_ref * a1 / (a1 + 1) + (G * shift_op) / (a1 + 1)

            # regularize the shifts
            xy_shifts_new = self._xy_shifts + shifts_update
            coefs = xp.linalg.lstsq(self._basis, xy_shifts_new, rcond=None)[0]
            xy_shifts_fit = self._basis @ coefs
            shifts_update = xy_shifts_fit - self._xy_shifts

            # apply shifts
            for start, end in generate_batches(
                self._num_bf_images, max_batch=max_batch_size
            ):
                shifted_BFs = self._stack_BF_shifted[start:end]
                stack_mask = self._stack_mask[start:end]

                Gs = xp.fft.fft2(shifted_BFs)

                dx = shifts_update[start:end, 0]
                dy = shifts_update[start:end, 1]

                shift_op = xp.exp(
                    self._qx_shift[None] * dx[:, None, None]
                    + self._qy_shift[None] * dy[:, None, None]
                )

                stack_BF_shifted = xp.real(xp.fft.ifft2(Gs * shift_op))
                stack_mask = xp.real(xp.fft.ifft2(xp.fft.fft2(stack_mask) * shift_op))

                self._stack_BF_shifted[start:end] = xp.asarray(
                    stack_BF_shifted, dtype=xp.float32
                )
                self._stack_mask[start:end] = xp.asarray(stack_mask, dtype=xp.float32)
                self._xy_shifts[start:end, 0] += dx
                self._xy_shifts[start:end, 1] += dy

                del Gs

            # Center the shifts
            xy_shifts_median = xp.round(xp.median(self._xy_shifts, axis=0)).astype(int)
            self._xy_shifts -= xy_shifts_median[None, :]
            self._stack_BF_shifted = xp.roll(
                self._stack_BF_shifted, -xy_shifts_median, axis=(1, 2)
            )
            self._stack_mask = xp.roll(self._stack_mask, -xy_shifts_median, axis=(1, 2))

            # Generate new estimate
            self._recon_mask = xp.mean(self._stack_mask, axis=0)

            mask_inv = 1 - np.clip(self._recon_mask, 0, 1)
            self._recon_BF = (
                self._stack_mean * mask_inv
                + xp.mean(self._stack_BF_shifted * self._stack_mask, axis=0)
            ) / (self._recon_mask + mask_inv)

            self._recon_error = (
                xp.atleast_1d(
                    xp.sum(
                        xp.abs(self._stack_BF_shifted - self._recon_BF[None])
                        * self._stack_mask
                    )
                )
                / self._mask_sum
                / self._stack_mean
            )

            self.error_iterations.append(float(self._recon_error))

            if plot_aligned_bf:
                row_index, col_index = np.unravel_index(a0, (nrows, ncols))

                ax = fig.add_subplot(spec[row_index, col_index])
                self._visualize_figax(fig, ax, **kwargs)

                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_title(f"Aligned BF at bin {int(bin_vals[a0])}")

        if plot_aligned_bf:
            if plot_convergence:
                ax = fig.add_subplot(spec[-1, :])
                x_range = np.arange(len(self.error_iterations))
                ax.plot(x_range, self.error_iterations)
                ax.set_xticks(x_range)
                ax.set_ylabel("Error")
            spec.tight_layout(fig)

        self.recon_BF = asnumpy(self._recon_BF)

        self.clear_device_mem(self._device, self._clear_fft_cache)

        return self

    def subpixel_alignment(
        self,
        virtual_detector_mask=None,
        kde_upsample_factor=None,
        kde_sigma_px=0.125,
        kde_lowpass_filter=False,
        lanczos_interpolation_order=None,
        integer_pixel_rolling_alignment=False,
        plot_upsampled_BF_comparison: bool = True,
        plot_upsampled_FFT_comparison: bool = False,
        position_correction_num_iter=None,
        position_correction_initial_step_size=1.0,
        position_correction_min_step_size=0.1,
        position_correction_step_size_factor=0.75,
        position_correction_checkerboard_steps=False,
        position_correction_gaussian_filter_sigma=None,
        position_correction_butterworth_q_lowpass=None,
        position_correction_butterworth_q_highpass=None,
        position_correction_butterworth_order=(2, 2),
        plot_position_correction_convergence: bool = True,
        progress_bar: bool = True,
        interpolation_max_batch_size: int = None,
        **kwargs,
    ):
        """
        Upsample and subpixel-align BFs using the measured image shifts.
        Uses kernel density estimation (KDE) to interpolate the upsampled BFs.

        Parameters
        ----------
        virtual_detector_mask: np.ndarray, bool
            Virtual detector mask, as a boolean array the same size as dp_mask
        kde_upsample_factor: int, optional
            Real-space upsampling factor
        kde_sigma_px: float, optional
            KDE gaussian kernel bandwidth in non-upsampled pixels
        kde_lowpass_filter: bool, optional
            If True, the resulting KDE upsampled image is lowpass-filtered using a sinc-function
        lanczos_interpolation_order: int, optional
            If not None, Lanczos interpolation with the specified order is used instead of bilinear
        fourier_upsampling_additional_factor: int, optional
            If not None, Fourier upsampling with integer rolling is used instead of bilinear/Lanczos
        plot_upsampled_BF_comparison: bool, optional
            If True, the pre/post alignment BF images are plotted for comparison
        plot_upsampled_FFT_comparison: bool, optional
            If True, the pre/post alignment BF FFTs are plotted for comparison
        position_correction_num_iter: int, optional
            If not None, parallax positions are corrected iteratively for this many iterations
        position_correction_initial_step_size: float, optional
            Initial position correction step-size in pixels
        position_correction_min_step_size: float, optional
            Minimum position correction step-size in pixels
        position_correction_step_size_factor: float, optional
            Factor to multiply step-size by between iterations
        position_correction_checkerboard_steps: bool, optional
            If True, uses steepest-descent checkerboarding steps, as opposed to gradient direction
        position_correction_gaussian_filter_sigma: tuple(float, float), optional
            Standard deviation of gaussian kernel in A
        position_correction_butterworth_q_lowpass: tuple(float, float), optional
            Cut-off frequency in A^-1 for low-pass butterworth filter
        position_correction_butterworth_q_highpass: tuple(float, float), optional
            Cut-off frequency in A^-1 for high-pass butterworth filter
        position_correction_butterworth_order: tuple(int,int), optional
            Butterworth filter order. Smaller gives a smoother filter
        plot_position_correction_convergence: bool, optional
            If True, position correction convergence is plotted
        progress_bar: bool, optional
            If True, a progress bar is printed with position correction progress
        interpolation_max_batch_size: int, optional
            Max number of pixels to use at once in upsampling (max is #BF * upsampled_pixels)

        """
        xp = self._xp
        asnumpy = self._asnumpy
        gaussian_filter = self._scipy.ndimage.gaussian_filter

        BF_sampling = 1 / asnumpy(self._kr).max() / 2
        DF_sampling = 1 / (
            self._reciprocal_sampling[0] * self._region_of_interest_shape[0]
        )

        self._BF_upsample_limit = self._scan_sampling[0] / BF_sampling
        self._DF_upsample_limit = self._scan_sampling[0] / DF_sampling

        if self._DF_upsample_limit < 1:
            warnings.warn(
                (
                    f"Dark-field upsampling limit of {self._DF_upsample_limit:.2f} "
                    "is less than 1, implying a scan step-size smaller than Nyquist. "
                    "setting to 1."
                ),
                UserWarning,
            )
            self._DF_upsample_limit = 1

        if kde_upsample_factor is None:
            if self._BF_upsample_limit * 3 / 2 > self._DF_upsample_limit:
                kde_upsample_factor = self._DF_upsample_limit

                warnings.warn(
                    (
                        f"Upsampling factor set to {kde_upsample_factor:.2f} (the "
                        "dark-field upsampling limit)."
                    ),
                    UserWarning,
                )

            elif self._BF_upsample_limit * 3 / 2 > 1:
                kde_upsample_factor = self._BF_upsample_limit * 3 / 2

                warnings.warn(
                    (
                        f"Upsampling factor set to {kde_upsample_factor:.2f} (1.5 times the "
                        f"bright-field upsampling limit of {self._BF_upsample_limit:.2f})."
                    ),
                    UserWarning,
                )
            else:
                kde_upsample_factor = np.maximum(self._DF_upsample_limit * 2 / 3, 1)

                warnings.warn(
                    (
                        f"Upsampling factor set to {kde_upsample_factor:.2f} (2/3 times the "
                        f"dark-field upsampling limit of {self._DF_upsample_limit:.2f})."
                    ),
                    UserWarning,
                )

        if kde_upsample_factor < 1:
            raise ValueError("kde_upsample_factor must be larger than 1")

        if kde_upsample_factor > self._DF_upsample_limit:
            warnings.warn(
                (
                    "Requested upsampling factor exceeds "
                    f"dark-field upsampling limit of {self._DF_upsample_limit:.2f}."
                ),
                UserWarning,
            )

        self._kde_upsample_factor = kde_upsample_factor

        # virtual detector
        if virtual_detector_mask is None:
            xy_shifts = self._xy_shifts
            stack_BF_unshifted = self._stack_BF_unshifted
        else:
            virtual_detector_mask = np.asarray(virtual_detector_mask, dtype="bool")
            xy_inds_np = asnumpy(self._xy_inds)
            inds = virtual_detector_mask[xy_inds_np[:, 0], xy_inds_np[:, 1]]

            xy_shifts = self._xy_shifts[inds]
            stack_BF_unshifted = self._stack_BF_unshifted[inds]

        BF_size = np.array(stack_BF_unshifted.shape[-2:])
        pixel_output_shape = np.round(BF_size * self._kde_upsample_factor).astype("int")

        if (
            not integer_pixel_rolling_alignment
            or position_correction_num_iter is not None
        ):
            # shifted coordinates
            x = xp.arange(BF_size[0], dtype=xp.float32)
            y = xp.arange(BF_size[1], dtype=xp.float32)
            xa_init, ya_init = xp.meshgrid(x, y, indexing="ij")

            # kernel density output the upsampled BF image
            xa = (xa_init + xy_shifts[:, 0, None, None]) * self._kde_upsample_factor
            ya = (ya_init + xy_shifts[:, 1, None, None]) * self._kde_upsample_factor

            pix_output = self._kernel_density_estimate(
                xa,
                ya,
                stack_BF_unshifted,
                pixel_output_shape,
                kde_sigma_px * self._kde_upsample_factor,
                lanczos_alpha=lanczos_interpolation_order,
                lowpass_filter=kde_lowpass_filter,
                max_batch_size=interpolation_max_batch_size,
            )
        else:
            upsample_fraction, upsample_int = np.modf(self._kde_upsample_factor)

            if upsample_fraction:
                upsample_nearest = np.round(self._kde_upsample_factor).astype("int")

                warnings.warn(
                    (
                        f"Upsampling factor of {self._kde_upsample_factor} "
                        f"rounded to nearest integer {upsample_nearest}."
                    ),
                    UserWarning,
                )

                self._kde_upsample_factor = upsample_nearest

            pix_output = pixel_rolling_kernel_density_estimate(
                stack_BF_unshifted,
                xy_shifts,
                self._kde_upsample_factor,
                kde_sigma_px * self._kde_upsample_factor,
                xp=xp,
                gaussian_filter=gaussian_filter,
            )

        # Perform probe position correction if needed
        if position_correction_num_iter is not None:
            if integer_pixel_rolling_alignment:
                interpolation_method = (
                    "bilinear" if lanczos_interpolation_order is None else "Lanczos"
                )
                warnings.warn(
                    (
                        "Integer pixel rolling is not compatible with position-correction, "
                        f"{interpolation_method} KDE interpolation will be used instead."
                    ),
                    UserWarning,
                )

            recon_BF_subpixel_aligned_reference = pix_output.copy()

            # init position shift array
            self._probe_dx = xp.zeros_like(xa_init)
            self._probe_dy = xp.zeros_like(xa_init)

            # step size of initial search, cost function
            step = xp.ones_like(xa_init) * position_correction_initial_step_size

            # init scores and stats
            position_correction_stats = np.zeros(position_correction_num_iter + 1)

            scores = (
                xp.mean(
                    xp.abs(
                        self._interpolate_array(
                            pix_output,
                            xa,
                            ya,
                            lanczos_alpha=None,
                            max_batch_size=interpolation_max_batch_size,
                        )
                        - stack_BF_unshifted
                    ),
                    axis=0,
                )
                * self._window_pad
            )

            position_correction_stats[0] = scores.mean()

            # gradient search directions

            if position_correction_checkerboard_steps:
                # checkerboard steps
                dxy = np.array(
                    [
                        [-1.0, 0.0],
                        [1.0, 0.0],
                        [0.0, -1.0],
                        [0.0, 1.0],
                    ]
                )

            else:
                # centered finite-difference directions
                dxy = np.array(
                    [
                        [-0.5, 0.0],
                        [0.5, 0.0],
                        [0.0, -0.5],
                        [0.0, 0.5],
                    ]
                )

            scores_test = xp.zeros(
                (
                    dxy.shape[0],
                    scores.shape[0],
                    scores.shape[1],
                )
            )

            # main loop for position correction
            for a0 in tqdmnd(
                position_correction_num_iter,
                desc="Correcting positions: ",
                unit=" iteration",
                disable=not progress_bar,
            ):
                # Evaluate scores for step directions and magnitudes

                for a1 in range(dxy.shape[0]):
                    xa = (
                        xa_init
                        + self._probe_dx
                        + dxy[a1, 0] * step
                        + xy_shifts[:, 0, None, None]
                    ) * self._kde_upsample_factor

                    ya = (
                        ya_init
                        + self._probe_dy
                        + dxy[a1, 1] * step
                        + xy_shifts[:, 1, None, None]
                    ) * self._kde_upsample_factor

                    scores_test[a1] = xp.mean(
                        xp.abs(
                            self._interpolate_array(
                                pix_output,
                                xa,
                                ya,
                                lanczos_alpha=None,
                                max_batch_size=interpolation_max_batch_size,
                            )
                            - stack_BF_unshifted
                        ),
                        axis=0,
                    )

                if position_correction_checkerboard_steps:
                    # Check where cost function has improved

                    scores_test *= self._window_pad[None]
                    update = np.min(scores_test, axis=0) < scores
                    scores_ind = np.argmin(scores_test, axis=0)

                    for a1 in range(dxy.shape[0]):
                        sub = np.logical_and(update, scores_ind == a1)
                        self._probe_dx[sub] += (
                            dxy[a1, 0] * step[sub] * self._window_pad[sub]
                        )
                        self._probe_dy[sub] += (
                            dxy[a1, 1] * step[sub] * self._window_pad[sub]
                        )

                else:
                    # Check where cost function has improved
                    dx = scores_test[0] - scores_test[1]
                    dy = scores_test[2] - scores_test[3]

                    dr = xp.sqrt(dx**2 + dy**2) / step
                    dx *= self._window_pad / dr
                    dy *= self._window_pad / dr

                    # Fixed-size step
                    xa = (
                        xa_init + self._probe_dx + dx + xy_shifts[:, 0, None, None]
                    ) * self._kde_upsample_factor

                    ya = (
                        ya_init + self._probe_dy + dy + xy_shifts[:, 1, None, None]
                    ) * self._kde_upsample_factor

                    fixed_step_scores = (
                        xp.mean(
                            xp.abs(
                                self._interpolate_array(
                                    pix_output,
                                    xa,
                                    ya,
                                    lanczos_alpha=None,
                                    max_batch_size=interpolation_max_batch_size,
                                )
                                - stack_BF_unshifted
                            ),
                            axis=0,
                        )
                        * self._window_pad
                    )

                    update = fixed_step_scores < scores
                    self._probe_dx[update] += dx[update]
                    self._probe_dy[update] += dy[update]

                # reduce gradient step for sites which did not improve
                step[xp.logical_not(update)] *= position_correction_step_size_factor

                # enforce minimum step size
                step = xp.maximum(step, position_correction_min_step_size)

                # apply regularization if needed
                if position_correction_gaussian_filter_sigma is not None:
                    self._probe_dx = gaussian_filter(
                        self._probe_dx,
                        position_correction_gaussian_filter_sigma[0]
                        / self._scan_sampling[0],
                        # mode="nearest",
                    )
                    self._probe_dy = gaussian_filter(
                        self._probe_dy,
                        position_correction_gaussian_filter_sigma[1]
                        / self._scan_sampling[1],
                        # mode="nearest",
                    )

                if (
                    position_correction_butterworth_q_lowpass is not None
                    or position_correction_butterworth_q_highpass is not None
                ):
                    qx = xp.fft.fftfreq(BF_size[0], self._scan_sampling[0]).astype(
                        xp.float32
                    )
                    qy = xp.fft.fftfreq(BF_size[1], self._scan_sampling[1]).astype(
                        xp.float32
                    )

                    qya, qxa = xp.meshgrid(qy, qx)
                    qra = xp.sqrt(qxa**2 + qya**2)

                    if position_correction_butterworth_q_lowpass:
                        (
                            q_lowpass_x,
                            q_lowpass_y,
                        ) = position_correction_butterworth_q_lowpass
                    else:
                        q_lowpass_x, q_lowpass_y = (None, None)
                    if position_correction_butterworth_q_highpass:
                        (
                            q_highpass_x,
                            q_highpass_y,
                        ) = position_correction_butterworth_q_highpass
                    else:
                        q_highpass_x, q_highpass_y = (None, None)

                    order_x, order_y = position_correction_butterworth_order

                    # dx
                    env = xp.ones_like(qra)
                    if q_highpass_x:
                        env *= 1 - 1 / (1 + (qra / q_highpass_x) ** (2 * order_x))
                    if q_lowpass_x:
                        env *= 1 / (1 + (qra / q_lowpass_x) ** (2 * order_x))

                    probe_dx_mean = xp.mean(self._probe_dx)
                    self._probe_dx -= probe_dx_mean
                    self._probe_dx = xp.real(
                        xp.fft.ifft2(xp.fft.fft2(self._probe_dx) * env)
                    )
                    self._probe_dx += probe_dx_mean

                    # dy
                    env = xp.ones_like(qra)
                    if q_highpass_y:
                        env *= 1 - 1 / (1 + (qra / q_highpass_y) ** (2 * order_y))
                    if q_lowpass_y:
                        env *= 1 / (1 + (qra / q_lowpass_y) ** (2 * order_y))

                    probe_dy_mean = xp.mean(self._probe_dy)
                    self._probe_dy -= probe_dy_mean
                    self._probe_dy = xp.real(
                        xp.fft.ifft2(xp.fft.fft2(self._probe_dy) * env)
                    )
                    self._probe_dy += probe_dy_mean

                # kernel density output the upsampled BF image
                xa = (
                    xa_init + self._probe_dx + xy_shifts[:, 0, None, None]
                ) * self._kde_upsample_factor

                ya = (
                    ya_init + self._probe_dy + xy_shifts[:, 1, None, None]
                ) * self._kde_upsample_factor

                pix_output = self._kernel_density_estimate(
                    xa,
                    ya,
                    stack_BF_unshifted,
                    pixel_output_shape,
                    kde_sigma_px * self._kde_upsample_factor,
                    lanczos_alpha=lanczos_interpolation_order,
                    lowpass_filter=kde_lowpass_filter,
                    max_batch_size=interpolation_max_batch_size,
                )

                # update cost function and stats
                scores = (
                    xp.mean(
                        xp.abs(
                            self._interpolate_array(
                                pix_output,
                                xa,
                                ya,
                                lanczos_alpha=None,
                                max_batch_size=interpolation_max_batch_size,
                            )
                            - stack_BF_unshifted
                        ),
                        axis=0,
                    )
                    * self._window_pad
                )

                position_correction_stats[a0 + 1] = scores.mean()

        else:
            plot_position_correction_convergence = False

        self._recon_BF_subpixel_aligned = pix_output
        self.recon_BF_subpixel_aligned = asnumpy(self._recon_BF_subpixel_aligned)

        if self._device == "gpu":
            xp._default_memory_pool.free_all_blocks()
            xp.clear_memo()

        # plotting
        nrows = np.count_nonzero(
            np.array(
                [
                    plot_upsampled_BF_comparison,
                    plot_upsampled_FFT_comparison,
                    plot_position_correction_convergence,
                ]
            )
        )
        if nrows > 0:
            ncols = 3 if position_correction_num_iter is not None else 2
            height_ratios = (
                [4, 4, 2][-nrows:]
                if plot_position_correction_convergence
                else [4, 4, 2][:nrows]
            )
            spec = GridSpec(
                ncols=ncols, nrows=nrows, height_ratios=height_ratios, hspace=0.15
            )

            figsize = kwargs.pop("figsize", (4 * ncols, sum(height_ratios)))
            cmap = kwargs.pop("cmap", "magma")
            fig = plt.figure(figsize=figsize)

            row_index = 0

            if plot_upsampled_BF_comparison:
                ax1 = fig.add_subplot(spec[row_index, 0])
                ax2 = fig.add_subplot(spec[row_index, 1])

                cropped_object = self._crop_padded_object(self._recon_BF)

                if ncols == 3:
                    ax3 = fig.add_subplot(spec[row_index, 2])

                    cropped_object_reference_aligned = self._crop_padded_object(
                        recon_BF_subpixel_aligned_reference, upsampled=True
                    )
                    cropped_object_aligned = self._crop_padded_object(
                        self._recon_BF_subpixel_aligned, upsampled=True
                    )
                    axs = [ax1, ax2, ax3]

                else:
                    cropped_object_reference_aligned = self._crop_padded_object(
                        self._recon_BF_subpixel_aligned, upsampled=True
                    )
                    axs = [ax1, ax2]

                extent = [
                    0,
                    self._scan_sampling[1] * cropped_object.shape[1],
                    self._scan_sampling[0] * cropped_object.shape[0],
                    0,
                ]

                axs[0].imshow(
                    cropped_object,
                    extent=extent,
                    cmap=cmap,
                    **kwargs,
                )
                axs[0].set_title("Aligned Bright Field")

                axs[1].imshow(
                    cropped_object_reference_aligned,
                    extent=extent,
                    cmap=cmap,
                    **kwargs,
                )
                axs[1].set_title("Upsampled Bright Field")

                if ncols == 3:
                    axs[2].imshow(
                        cropped_object_aligned,
                        extent=extent,
                        cmap=cmap,
                        **kwargs,
                    )
                    axs[2].set_title("Probe-Corrected Bright Field")

                for ax in axs:
                    ax.set_ylabel("x [A]")
                    ax.set_xlabel("y [A]")

                row_index += 1

            if plot_upsampled_FFT_comparison:
                ax1 = fig.add_subplot(spec[row_index, 0])
                ax2 = fig.add_subplot(spec[row_index, 1])

                reciprocal_extent = [
                    -0.5 / (self._scan_sampling[1] / self._kde_upsample_factor),
                    0.5 / (self._scan_sampling[1] / self._kde_upsample_factor),
                    0.5 / (self._scan_sampling[0] / self._kde_upsample_factor),
                    -0.5 / (self._scan_sampling[0] / self._kde_upsample_factor),
                ]

                nx, ny = self._recon_BF_subpixel_aligned.shape
                kx = xp.fft.fftfreq(nx, d=1).astype(xp.float32)
                ky = xp.fft.fftfreq(ny, d=1).astype(xp.float32)
                k = xp.fft.fftshift(xp.sqrt(kx[:, None] ** 2 + ky[None, :] ** 2))

                recon_fft = xp.fft.fftshift(
                    xp.abs(xp.fft.fft2(self._recon_BF)) / np.prod(self._recon_BF.shape)
                )
                sx, sy = recon_fft.shape

                pad_x_post = (nx - sx) // 2
                pad_x_pre = nx - sx - pad_x_post
                pad_y_post = (ny - sy) // 2
                pad_y_pre = ny - sy - pad_y_post

                pad_recon_fft = asnumpy(
                    xp.pad(
                        recon_fft, ((pad_x_pre, pad_x_post), (pad_y_pre, pad_y_post))
                    )
                    * k
                )

                if ncols == 3:
                    ax3 = fig.add_subplot(spec[row_index, 2])
                    upsampled_fft_reference = asnumpy(
                        xp.fft.fftshift(
                            xp.abs(xp.fft.fft2(recon_BF_subpixel_aligned_reference))
                            / (nx * ny)
                        )
                        * k
                    )

                    upsampled_fft = asnumpy(
                        xp.fft.fftshift(
                            xp.abs(xp.fft.fft2(self._recon_BF_subpixel_aligned))
                            / (nx * ny)
                        )
                        * k
                    )
                    axs = [ax1, ax2, ax3]
                else:
                    upsampled_fft_reference = asnumpy(
                        xp.fft.fftshift(
                            xp.abs(xp.fft.fft2(self._recon_BF_subpixel_aligned))
                            / (nx * ny)
                        )
                        * k
                    )
                    axs = [ax1, ax2]

                _, vmin, vmax = return_scaled_histogram_ordering(
                    upsampled_fft_reference
                )

                axs[0].imshow(
                    pad_recon_fft,
                    extent=reciprocal_extent,
                    vmin=vmin,
                    vmax=vmax,
                    cmap="gray",
                    **kwargs,
                )
                axs[0].set_title("Aligned Bright Field FFT")

                axs[1].imshow(
                    upsampled_fft_reference,
                    extent=reciprocal_extent,
                    vmin=vmin,
                    vmax=vmax,
                    cmap="gray",
                    **kwargs,
                )
                axs[1].set_title("Upsampled Bright Field FFT")

                if ncols == 3:
                    axs[2].imshow(
                        upsampled_fft,
                        extent=reciprocal_extent,
                        vmin=vmin,
                        vmax=vmax,
                        cmap="gray",
                        **kwargs,
                    )
                    axs[2].set_title("Probe-Corrected Bright Field FFT")

                for ax in axs:
                    ax.set_ylabel(r"$k_x$ [$A^{-1}$]")
                    ax.set_xlabel(r"$k_y$ [$A^{-1}$]")

                row_index += 1

            if plot_position_correction_convergence:
                axs = fig.add_subplot(spec[row_index, :])

                kwargs.pop("vmin", None)
                kwargs.pop("vmax", None)
                color = kwargs.pop("color", (1, 0, 0))

                axs.semilogy(
                    np.arange(position_correction_num_iter + 1),
                    position_correction_stats / position_correction_stats[0],
                    color=color,
                    **kwargs,
                )
                axs.set_xlabel("Iteration number")
                axs.set_ylabel("NMSE")
                axs.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
                axs.yaxis.set_minor_formatter(PercentFormatter(1.0, decimals=0))

            spec.tight_layout(fig)

        self.clear_device_mem(self._device, self._clear_fft_cache)

        return self

    def _interpolate_array(
        self,
        image,
        xa,
        ya,
        lanczos_alpha,
        max_batch_size=None,
    ):
        """ """

        xp = self._xp

        if lanczos_alpha is not None:
            return lanczos_interpolate_array(
                image, xa, ya, lanczos_alpha, xp=xp, max_batch_size=max_batch_size
            )
        else:
            return bilinearly_interpolate_array(
                image,
                xa,
                ya,
                xp=xp,
                max_batch_size=max_batch_size,
            )

    def _kernel_density_estimate(
        self,
        xa,
        ya,
        intensities,
        output_shape,
        kde_sigma,
        lanczos_alpha=None,
        lowpass_filter=False,
        max_batch_size=None,
    ):
        """ """

        xp = self._xp
        gaussian_filter = self._scipy.ndimage.gaussian_filter

        if lanczos_alpha is not None:
            return lanczos_kernel_density_estimate(
                xa,
                ya,
                intensities,
                output_shape,
                kde_sigma,
                lanczos_alpha,
                lowpass_filter=lowpass_filter,
                xp=xp,
                gaussian_filter=gaussian_filter,
                max_batch_size=max_batch_size,
            )
        else:
            return bilinear_kernel_density_estimate(
                xa,
                ya,
                intensities,
                output_shape,
                kde_sigma,
                lowpass_filter=lowpass_filter,
                xp=xp,
                gaussian_filter=gaussian_filter,
                max_batch_size=max_batch_size,
            )

    def _aberration_fit_polar_decomposition(
        self,
        xy_shifts,
        scan_sampling,
        probe_angles,
        force_transpose: bool = False,
        force_rotation_angle_deg: float = None,
    ):
        """ """

        xp = self._xp
        asnumpy = self._asnumpy

        # Numpy arrays
        shifts = asnumpy(xy_shifts)
        angles = asnumpy(probe_angles)
        sampling = asnumpy(scan_sampling)

        if force_transpose:
            shifts = np.flip(shifts, axis=1)

        shifts_Ang = shifts * sampling

        # Solve affine transformation
        m = np.linalg.lstsq(angles, shifts_Ang, rcond=None)[0]

        if force_rotation_angle_deg is None:
            m_rotation, m_aberration = polar(m, side="right")

            if force_transpose:
                m_rotation = m_rotation.T

            # Convert into rotation and aberration coefficients
            rotation_rad = -1 * np.arctan2(m_rotation[1, 0], m_rotation[0, 0])
            if 2 * np.abs(np.mod(rotation_rad + np.pi, 2 * np.pi) - np.pi) > np.pi:
                rotation_rad = np.mod(rotation_rad, 2 * np.pi) - np.pi
                m_aberration *= -1.0
        else:
            rotation_rad = np.deg2rad(force_rotation_angle_deg)
            c, s = np.cos(rotation_rad), np.sin(rotation_rad)

            m_rotation = np.array([[c, -s], [s, c]])
            if force_transpose:
                m_rotation = m_rotation.T

            m_aberration = m_rotation @ m

        aberrations_C1 = (m_aberration[0, 0] + m_aberration[1, 1]) / 2

        if force_transpose:
            aberrations_C12a = -(m_aberration[0, 0] - m_aberration[1, 1]) / 2
            aberrations_C12b = (m_aberration[1, 0] + m_aberration[0, 1]) / 2
        else:
            aberrations_C12a = (m_aberration[0, 0] - m_aberration[1, 1]) / 2
            aberrations_C12b = (m_aberration[1, 0] + m_aberration[0, 1]) / 2

        return (
            xp.asarray(shifts_Ang),
            rotation_rad,
            aberrations_C1,
            aberrations_C12a,
            aberrations_C12b,
        )

    def _aberration_fit_deltas_and_increment(
        self,
        measured_shifts,
        fitted_shifts,
        gradients,
        aberrations_coefs,
        indices,
    ):
        """ """
        xp = self._xp
        asnumpy = self._asnumpy

        delta_shifts = (measured_shifts - fitted_shifts).T.ravel()
        coefs = xp.linalg.lstsq(gradients, delta_shifts, rcond=None)[0]
        deltas = xp.tensordot(gradients, coefs, axes=1).reshape((2, -1)).T

        aberrations_coefs[indices] += asnumpy(coefs)
        fitted_shifts += deltas

        return aberrations_coefs, fitted_shifts

    def aberration_fit(
        self,
        max_radial_order: int = 3,
        max_angular_order: int = 4,
        min_radial_order: int = 2,
        min_angular_order: int = 0,
        aberrations_mn: list = None,
        initialize_fit_with_polar_decomposition: bool = True,
        fit_method="recursive",
        force_transpose: bool = False,
        force_rotation_angle_deg: float = None,
        plot_CTF_comparison: bool = False,
        plot_BF_shifts_comparison: bool = False,
        **kwargs,
    ):
        """
        Fit aberrations to the measured image shifts.

        Parameters
        ----------
        max_radial_order: int, optional
            Max radial order for fitting of aberrations.
        max_angular_order: int, optional
            Max angular order for fitting of aberrations.
        min_radial_order: int, optional
            Min radial order for fitting of aberrations.
        min_angular_order: int, optional
            Min angular order for fitting of aberrations.
        aberrations_mn: list, optional
            If not None, sets aberrations mn explicitly.
        initialize_fit_with_polar_decomposition: bool, optional
            If True (default), the defocus/stig estimates arising from the polar decomposition
            are subtracted before the first aberrations order fit, and thus refined.
        fit_method: str, optional
            Order in which to fit aberration coefficients. One of:
            'global': all orders are fitted at-once.
              I.e. [[C1,C12a,C12b,C21a,C21b,C23a,C23b, ...]]
            'recursive': fit happens recursively in increasing order of radial-aberrations. (Default)
              I.e. [[C1,C12a,C12b],[C1,C12a,C12b,C21a, C21b, C23a, C23b], ...]
            'recursive-exclusive': same as 'recursive' but previous orders are not refined further.
              I.e. [[C1,C12a,C12b],[C21a, C21b, C23a, C23b], ...]
        force_transpose: bool, optional
            If True, flips the measured x and y shifts.
        force_rotation_deg: float, optional
            If not None, sets the rotation angle to value in degrees.
        plot_CTF_comparison: bool, optional
            If True, the fitted CTF is plotted against the reconstructed frequencies.
        plot_BF_shifts_comparison: bool, optional
            If True, the measured vs fitted BF shifts are plotted.
        """
        xp = self._xp
        asnumpy = self._asnumpy

        # Initial estimate
        shifts_Ang, rotation_rad, aberrations_C1, aberrations_C12a, aberrations_C12b = (
            self._aberration_fit_polar_decomposition(
                self._xy_shifts,
                self._scan_sampling,
                self._probe_angles,
                force_transpose=force_transpose,
                force_rotation_angle_deg=force_rotation_angle_deg,
            )
        )

        self.aberrations_C1 = aberrations_C1
        self.aberrations_C12a = aberrations_C12a
        self.aberrations_C12b = aberrations_C12b
        self.rotation_Q_to_R_rads = rotation_rad
        self.transpose = force_transpose

        # Aberration coefs

        if min_radial_order < 2 or max_radial_order < min_radial_order:
            raise ValueError()

        if min_angular_order < 0 or max_angular_order < min_angular_order:
            raise ValueError()

        if aberrations_mn is None:
            mn = []

            for m in range(min_radial_order - 1, max_radial_order):
                n_max = np.minimum(max_angular_order, m + 1)
                for n in range(min_angular_order, n_max + 1):
                    if (m + n) % 2:
                        mn.append([m, n, 0])
                        if n > 0:
                            mn.append([m, n, 1])
        else:
            mn = aberrations_mn

        self._aberrations_mn = np.array(mn)
        sub = self._aberrations_mn[:, 1] > 0
        self._aberrations_mn[sub, :] = self._aberrations_mn[sub, :][
            np.argsort(self._aberrations_mn[sub, 0]), :
        ]
        self._aberrations_mn[~sub, :] = self._aberrations_mn[~sub, :][
            np.argsort(self._aberrations_mn[~sub, 0]), :
        ]
        self._aberrations_num = self._aberrations_mn.shape[0]
        self._aberrations_coefs = np.zeros(self._aberrations_num)

        # Basis functions
        sampling = 1 / (
            np.array(self._reciprocal_sampling) * self._region_of_interest_shape
        )
        (
            self._aberrations_basis,
            self._aberrations_basis_du,
            self._aberrations_basis_dv,
        ) = calculate_aberration_gradient_basis(
            self._aberrations_mn,
            sampling,
            self._region_of_interest_shape,
            self._wavelength,
            rotation_angle=rotation_rad,
            xp=xp,
        )

        corner_indices = self._xy_inds - xp.asarray(self._region_of_interest_shape // 2)
        raveled_indices = np.ravel_multi_index(
            corner_indices.T, self._region_of_interest_shape, mode="wrap"
        )

        # CTF function
        def calculate_CTF(alpha_shape, *coefs):
            chi = xp.zeros_like(self._aberrations_basis[:, 0])
            for a0 in range(len(coefs)):
                chi += coefs[a0] * self._aberrations_basis[:, a0]
            return xp.reshape(chi, alpha_shape)

        # Initialization
        if initialize_fit_with_polar_decomposition:
            aberrations_mn_list = self._aberrations_mn.tolist()
            initialization_inds = []
            if [1, 0, 0] in aberrations_mn_list:
                ind_C1 = aberrations_mn_list.index([1, 0, 0])
                self._aberrations_coefs[ind_C1] = aberrations_C1
                initialization_inds.append(ind_C1)

            if [1, 2, 0] in aberrations_mn_list:
                ind_C12a = aberrations_mn_list.index([1, 2, 0])
                ind_C12b = aberrations_mn_list.index([1, 2, 1])
                self._aberrations_coefs[ind_C12a] = aberrations_C12a
                self._aberrations_coefs[ind_C12b] = aberrations_C12b
                initialization_inds.append(ind_C12a)
                initialization_inds.append(ind_C12b)

            initialization_inds = np.array(initialization_inds)
            gradients = xp.array(
                (
                    self._aberrations_basis_du[
                        raveled_indices[:, None], initialization_inds[None, :]
                    ],
                    self._aberrations_basis_dv[
                        raveled_indices[:, None], initialization_inds[None, :]
                    ],
                )
            )

            aberrations_coefs = xp.asarray(
                self._aberrations_coefs[initialization_inds], dtype=xp.float32
            )
            fitted_shifts_Ang = xp.tensordot(gradients, aberrations_coefs, axes=1).T
        else:
            fitted_shifts_Ang = xp.zeros_like(shifts_Ang)

        # Incremental fitting
        chunks = np.unique(self._aberrations_mn[:, 0], return_index=True)[1][1:]
        split_order = np.split(np.arange(self._aberrations_num), chunks)

        if fit_method == "recursive-exclusive":
            self._aberrations_split_order = split_order
        elif fit_method == "recursive":
            self._aberrations_split_order = [
                np.concatenate(split_order[:n]) for n in range(1, len(split_order) + 1)
            ]
        elif fit_method == "global":
            self._aberrations_split_order = [np.concatenate(split_order)]
        else:
            raise ValueError()

        for indices in self._aberrations_split_order:
            gradients = xp.vstack(
                (
                    self._aberrations_basis_du[
                        raveled_indices[:, None], indices[None, :]
                    ],
                    self._aberrations_basis_dv[
                        raveled_indices[:, None], indices[None, :]
                    ],
                )
            )

            self._aberrations_coefs, fitted_shifts_Ang = (
                self._aberration_fit_deltas_and_increment(
                    shifts_Ang,
                    fitted_shifts_Ang,
                    gradients,
                    self._aberrations_coefs,
                    indices,
                )
            )

        if force_transpose:
            aberrations_to_flip = (self._aberrations_mn[:, 1] > 0) & (
                self._aberrations_mn[:, 2] == 0
            )
            self._aberrations_coefs[aberrations_to_flip] *= -1

        # format aberrations
        dict_cartesian = {
            tuple(self._aberrations_mn[a0]): self._aberrations_coefs[a0]
            for a0 in range(self._aberrations_num)
        }
        dict_polar = {}
        unique_aberrations = np.unique(self._aberrations_mn[:, :2], axis=0)
        for aberration_order in unique_aberrations:
            m, n = aberration_order
            modulus_name = "C" + str(m) + str(n)

            if n != 0:
                value_a = dict_cartesian[(m, n, 0)]
                value_b = dict_cartesian[(m, n, 1)]
                dict_polar[modulus_name] = np.sqrt(value_a**2 + value_b**2)

                argument_name = "phi" + str(m) + str(n)
                dict_polar[argument_name] = np.arctan2(value_b, value_a) / n
            else:
                dict_polar[modulus_name] = dict_cartesian[(m, n, 0)]

        dict_cartesian = polar_aberrations_to_cartesian(dict_polar)
        self.aberrations_dict_cartesian = dict_cartesian
        self.aberrations_dict_polar = dict_polar

        # Plot the measured/fitted shifts comparison
        nrows = np.count_nonzero(
            np.array(
                [
                    plot_BF_shifts_comparison,
                    plot_CTF_comparison,
                ]
            )
        )

        if nrows > 0:
            spec = GridSpec(ncols=2, nrows=nrows)

            figsize = kwargs.pop("figsize", (8, 4 * nrows))
            fig = plt.figure(figsize=figsize)

            row_index = 0

            if plot_CTF_comparison:
                if hasattr(self, "_kde_upsample_factor"):
                    im_FFT = xp.abs(xp.fft.fft2(self._recon_BF_subpixel_aligned))
                    sx = self._scan_sampling[0] / self._kde_upsample_factor
                    sy = self._scan_sampling[1] / self._kde_upsample_factor

                    reciprocal_extent = [
                        -0.5 / (self._scan_sampling[1] / self._kde_upsample_factor),
                        0.5 / (self._scan_sampling[1] / self._kde_upsample_factor),
                        0.5 / (self._scan_sampling[0] / self._kde_upsample_factor),
                        -0.5 / (self._scan_sampling[0] / self._kde_upsample_factor),
                    ]

                else:
                    im_FFT = xp.abs(xp.fft.fft2(self._recon_BF))
                    sx = self._scan_sampling[0]
                    sy = self._scan_sampling[1]

                    reciprocal_extent = [
                        -0.5 / self._scan_sampling[1],
                        0.5 / self._scan_sampling[1],
                        0.5 / self._scan_sampling[0],
                        -0.5 / self._scan_sampling[0],
                    ]

                # FFT coordinates
                qx = xp.fft.fftfreq(im_FFT.shape[0], sx).astype(xp.float32)
                qy = xp.fft.fftfreq(im_FFT.shape[1], sy).astype(xp.float32)
                qr2 = qx[:, None] ** 2 + qy[None, :] ** 2

                alpha_FFT = xp.sqrt(qr2) * self._wavelength
                theta_FFT = xp.arctan2(qy[None, :], qx[:, None])

                # Aberration basis

                chi_FFT = xp.zeros(alpha_FFT.shape)
                for a0 in range(self._aberrations_num):
                    m, n, a = self._aberrations_mn[a0]
                    coeff = self._aberrations_coefs[a0]
                    if n == 0:
                        # Radially symmetric basis
                        chi_FFT += (alpha_FFT ** (m + 1) / (m + 1)) * coeff

                    elif a == 0:
                        # cos coef
                        chi_FFT += (
                            alpha_FFT ** (m + 1) * xp.cos(n * theta_FFT) / (m + 1)
                        ) * coeff
                    else:
                        # sin coef
                        chi_FFT += (
                            alpha_FFT ** (m + 1) * xp.sin(n * theta_FFT) / (m + 1)
                        ) * coeff

                # global scaling
                chi_FFT *= 2 * np.pi / self._wavelength
                plot_mask = qr2 > np.pi**2 / 4 / np.abs(aberrations_C1)
                angular_mask = np.cos(8.0 * theta_FFT) ** 2 < 0.25

                # Generate FFT plotting image
                im_scale = np.fft.fftshift(asnumpy(im_FFT))
                im_scale, vmin, vmax = return_scaled_histogram_ordering(
                    im_scale, normalize=True
                )
                im_plot = np.tile(im_scale[:, :, None], (1, 1, 3))

                # Add CTF zero crossings
                im_CTF_plot = xp.abs(xp.sin(chi_FFT))

                chi_FFT[xp.abs(chi_FFT) > 12.5 * np.pi] = np.pi / 2
                chi_FFT = xp.abs(xp.sin(chi_FFT)) < 0.15
                chi_FFT[xp.logical_not(plot_mask)] = 0

                chi_FFT = np.fft.fftshift(asnumpy(chi_FFT * angular_mask))
                im_plot[:, :, 0] += chi_FFT
                im_plot[:, :, 1] -= chi_FFT
                im_plot[:, :, 2] -= chi_FFT
                im_plot = np.clip(im_plot, 0, 1)

                ax1 = fig.add_subplot(spec[row_index, 0])
                ax2 = fig.add_subplot(spec[row_index, 1])

                ax1.imshow(im_plot, vmin=vmin, vmax=vmax, extent=reciprocal_extent)
                ax2.imshow(
                    np.fft.fftshift(asnumpy(im_CTF_plot)),
                    cmap="gray",
                    extent=reciprocal_extent,
                )

                for ax in (ax1, ax2):
                    ax.set_ylabel(r"$k_x$ [$A^{-1}$]")
                    ax.set_xlabel(r"$k_y$ [$A^{-1}$]")

                ax1.set_title("Aligned Bright Field FFT")
                ax2.set_title("Fitted CTF ")
                row_index += 1

            if plot_BF_shifts_comparison:

                scale_arrows = kwargs.pop("scale_arrows", 1)
                plot_arrow_freq = kwargs.pop("plot_arrow_freq", 1)

                ax1 = fig.add_subplot(spec[row_index, 0])
                ax2 = fig.add_subplot(spec[row_index, 1])

                self.show_shifts(
                    shifts_ang=shifts_Ang,
                    plot_rotated_shifts=False,
                    plot_arrow_freq=plot_arrow_freq,
                    scale_arrows=scale_arrows,
                    color=(1, 0, 0),
                    figax=(fig, ax1),
                )

                self.show_shifts(
                    shifts_ang=fitted_shifts_Ang,
                    plot_rotated_shifts=False,
                    plot_arrow_freq=plot_arrow_freq,
                    scale_arrows=scale_arrows,
                    color=(0, 0, 1),
                    figax=(fig, ax2),
                )
                ax2.set_title("Fitted BF Shifts")
                row_index += 1

            spec.tight_layout(fig)

        # Print results
        if self._verbose:
            heading = "Initial aberration coefficients"
            print(f"{heading:^50}")
            print("-" * 50)
            print("  rotation   transpose    C1      stig  stig angle")
            print("   [deg]       ---       [Ang]   [Ang]     [deg]  ")
            print("----------   -------   -------   -----   ---------")

            angle = f"{np.round(np.rad2deg(rotation_rad),decimals=1):^10}"
            transpose = f"{str(force_transpose):^7}"
            C1 = np.round(aberrations_C1).astype("int")
            C1 = f"{C1:^7}"
            stig = np.round(
                np.sqrt(aberrations_C12a**2 + aberrations_C12b**2)
            ).astype("int")
            stig = f"{stig:^5}"
            stig_angle = np.round(
                np.rad2deg(np.arctan2(aberrations_C12b, aberrations_C12a) / 2),
                decimals=1,
            )
            stig_angle = f"{stig_angle:^9}"
            print("   ".join([angle, transpose, C1, stig, stig_angle]))

            print()
            heading = "Refined aberration coefficients"
            print(f"{heading:^50}")
            print("-" * 50)
            print("aberration    radial   angular   angle   magnitude")
            print("   name       order     order    [deg]     [Ang]  ")
            print("----------   -------   -------   -----   ---------")

            for mn in np.unique(self._aberrations_mn[:, :2], axis=0):
                m, n = mn
                name = _aberration_names.get((m, n), "---")
                mag = dict_polar.get(f"C{m}{n}", "---")
                angle = dict_polar.get(f"phi{m}{n}", "---")
                if angle != "---":
                    angle = np.round(np.rad2deg(angle), decimals=1)
                if mag != "---":
                    mag = np.round(mag).astype("int")

                name = f"{name:^10}"
                radial_order = f"{m+1:^7}"
                angular_order = f"{n:^7}"
                angle = f"{angle:^5}"
                mag = f"{mag:^9}"
                print("   ".join([name, radial_order, angular_order, angle, mag]))

        self.clear_device_mem(self._device, self._clear_fft_cache)

        return self

    def _calculate_CTF(self, alpha_shape, sampling, aberrations_mn, coefs):
        xp = self._xp

        # FFT coordinates
        sx, sy = sampling
        nx, ny = alpha_shape
        qx = xp.fft.fftfreq(nx, sx).astype(xp.float32)
        qy = xp.fft.fftfreq(ny, sy).astype(xp.float32)
        qr2 = qx[:, None] ** 2 + qy[None, :] ** 2

        alpha = xp.sqrt(qr2) * self._wavelength
        theta = xp.arctan2(qy[None, :], qx[:, None])

        chi = xp.zeros(alpha_shape, dtype=xp.float32)
        aberrations_num = len(aberrations_mn)

        for a0 in range(aberrations_num):
            m, n, a = aberrations_mn[a0]
            coef = coefs[a0]
            if n == 0:
                # Radially symmetric basis
                chi += (alpha ** (m + 1) / (m + 1)) * coef

            elif a == 0:
                # cos coef
                chi += (alpha ** (m + 1) * xp.cos(n * theta) / (m + 1)) * coef
            else:
                # sin coef
                chi += (alpha ** (m + 1) * xp.sin(n * theta) / (m + 1)) * coef

        # global scaling
        chi *= 2 * np.pi / self._wavelength

        return chi

    def aberration_correct(
        self,
        use_CTF_fit=None,
        plot_corrected_phase: bool = True,
        q_lowpass: float = None,
        q_highpass: float = None,
        butterworth_order: int = 2,
        upsampled: bool = True,
        **kwargs,
    ):
        """
        CTF correction of the phase image using the measured defocus aberration.

        Parameters
        ----------
        use_FFT_fit: bool
            Use the CTF fitted to the zero crossings of the FFT.
            Default is True
        plot_corrected_phase: bool, optional
            If True, the CTF-corrected phase is plotted
        q_lowpass: float
            Cut-off frequency in A^-1 for low-pass butterworth filter
        butterworth_order: float
            Butterworth filter order. Smaller gives a smoother filter
        """

        xp = self._xp
        asnumpy = self._asnumpy

        if not hasattr(self, "aberrations_C1"):
            raise ValueError(
                (
                    "CTF correction is meant to be ran after alignment and aberration fitting. "
                    "Please run the `reconstruct()` and `aberration_fit()` functions first."
                )
            )

        if upsampled and hasattr(self, "_kde_upsample_factor"):
            im = self._recon_BF_subpixel_aligned
            sx = self._scan_sampling[0] / self._kde_upsample_factor
            sy = self._scan_sampling[1] / self._kde_upsample_factor
        else:
            upsampled = False
            im = self._recon_BF
            sx = self._scan_sampling[0]
            sy = self._scan_sampling[1]

        # Fourier coordinates
        kx = xp.fft.fftfreq(im.shape[0], sx).astype(xp.float32)
        ky = xp.fft.fftfreq(im.shape[1], sy).astype(xp.float32)
        kra2 = (kx[:, None]) ** 2 + (ky[None, :]) ** 2

        if use_CTF_fit is None:
            if hasattr(self, "_aberrations_surface_shape"):
                use_CTF_fit = True

        if use_CTF_fit:
            # note m+1 is radial order
            even_radial_orders = (self._aberrations_mn[:, 0] % 2) == 1
            odd_radial_orders = (self._aberrations_mn[:, 0] % 2) == 0

            odd_mn = self._aberrations_mn[odd_radial_orders]
            odd_coefs = self._aberrations_coefs[odd_radial_orders]
            chi_odd = self._calculate_CTF(im.shape, (sx, sy), odd_mn, odd_coefs)

            even_mn = self._aberrations_mn[even_radial_orders]
            even_coefs = self._aberrations_coefs[even_radial_orders]
            chi_even = self._calculate_CTF(im.shape, (sx, sy), even_mn, even_coefs)

            if not chi_even.any():  # check if all zeros
                chi_even = xp.ones_like(chi_even)

        else:
            chi_even = (xp.pi * self._wavelength * self.aberrations_C1) * kra2
            chi_odd = xp.zeros_like(chi_even)

        CTF_corr = xp.sign(xp.sin(chi_even)) * xp.exp(-1j * chi_odd)
        CTF_corr[0, 0] = 0

        # apply correction to mean reconstructed BF image
        im_fft_corr = xp.fft.fft2(im) * CTF_corr

        # if needed, add low pass filter output image
        if q_lowpass is not None:
            im_fft_corr /= 1 + (xp.sqrt(kra2) / q_lowpass) ** (2 * butterworth_order)

        # Output phase image
        self._recon_phase_corrected = xp.real(xp.fft.ifft2(im_fft_corr))
        self.recon_phase_corrected = asnumpy(self._recon_phase_corrected)

        # plotting
        if plot_corrected_phase:
            figsize = kwargs.pop("figsize", (6, 6))
            cmap = kwargs.pop("cmap", "magma")

            fig, ax = plt.subplots(figsize=figsize)

            cropped_object = self._crop_padded_object(
                self._recon_phase_corrected, upsampled=upsampled
            )

            extent = [
                0,
                sy * cropped_object.shape[1],
                sx * cropped_object.shape[0],
                0,
            ]

            ax.imshow(
                cropped_object,
                extent=extent,
                cmap=cmap,
                **kwargs,
            )

            ax.set_ylabel("x [A]")
            ax.set_xlabel("y [A]")
            ax.set_title("Parallax-Corrected Phase Image")

        self.clear_device_mem(self._device, self._clear_fft_cache)
        return self

    def depth_section(
        self,
        depth_angstroms=None,
        use_CTF_fit=True,
        plot_depth_sections=True,
        k_info_limit: float = None,
        k_info_power: float = 1.0,
        progress_bar=True,
        **kwargs,
    ):
        """
        CTF correction of the BF image using the measured defocus aberration.

        Parameters
        ----------
        depth_angstroms: np.array
            Specify the depths
        k_info_limit: float, optional
            maximum allowed frequency in butterworth filter
        k_info_power: float, optional
            power of butterworth filter


        Returns
        -------
        stack_depth: np.array
            stack of phase images at different depths with shape [depth Nx Ny]

        """

        xp = self._xp
        asnumpy = self._asnumpy

        if not hasattr(self, "aberrations_C1"):
            raise ValueError(
                (
                    "Depth sectioning is meant to be ran after alignment and aberration fitting. "
                    "Please run the `reconstruct()` and `aberration_fit()` functions first."
                )
            )

        if depth_angstroms is None:
            depth_angstroms = np.linspace(-256, 256, 33)
        depth_angstroms = xp.atleast_1d(depth_angstroms)

        # Fourier coordinates
        sx, sy = self._scan_sampling
        nx, ny = self._recon_BF.shape
        kx = xp.fft.fftfreq(nx, sx).astype(xp.float32)
        ky = xp.fft.fftfreq(ny, sy).astype(xp.float32)
        kra2 = (kx[:, None]) ** 2 + (ky[None, :]) ** 2

        if use_CTF_fit:
            sin_chi = xp.sin(
                self._calculate_CTF((nx, ny), (sx, sy), *self._aberrations_coefs)
            )
        else:
            sin_chi = xp.sin((xp.pi * self._wavelength * self.aberrations_C1) * kra2)

        CTF_corr = xp.sign(sin_chi)
        CTF_corr[0, 0] = 0

        # init
        stack_depth = xp.zeros(
            (depth_angstroms.shape[0], self._recon_BF.shape[0], self._recon_BF.shape[1])
        )

        # plotting
        if plot_depth_sections:
            num_plots = depth_angstroms.shape[0]
            nrows = int(np.sqrt(num_plots))
            ncols = int(np.ceil(num_plots / nrows))

            spec = GridSpec(
                ncols=ncols,
                nrows=nrows,
                hspace=0.15,
                wspace=0.15,
            )

            figsize = kwargs.pop("figsize", (4 * ncols, 4 * nrows))
            cmap = kwargs.pop("cmap", "magma")

            fig = plt.figure(figsize=figsize)

        # main loop
        for a0 in tqdmnd(
            depth_angstroms.shape[0],
            desc="Depth sectioning ",
            unit="plane",
            disable=not progress_bar,
        ):
            dz = depth_angstroms[a0]

            # Parallax
            im_depth = xp.zeros_like(self._recon_BF, dtype=xp.complex64)
            dx = -self._probe_angles[:, 0] * dz / self._scan_sampling[0]
            dy = -self._probe_angles[:, 1] * dz / self._scan_sampling[1]
            shift_op = xp.exp(
                self._qx_shift[None] * dx[:, None, None]
                + self._qy_shift[None] * dy[:, None, None]
            )
            im_depth = xp.fft.fft2(self._stack_BF_shifted) * shift_op * CTF_corr

            if k_info_limit is not None:
                im_depth /= 1 + (kra2**k_info_power) / (
                    (k_info_limit) ** (2 * k_info_power)
                )

            stack_depth[a0] = xp.real(xp.fft.ifft2(im_depth)).mean(0)

            if plot_depth_sections:
                row_index, col_index = np.unravel_index(a0, (nrows, ncols))
                ax = fig.add_subplot(spec[row_index, col_index])

                cropped_object = self._crop_padded_object(asnumpy(stack_depth[a0]))

                extent = [
                    0,
                    self._scan_sampling[1] * cropped_object.shape[1],
                    self._scan_sampling[0] * cropped_object.shape[0],
                    0,
                ]

                ax.imshow(
                    cropped_object,
                    extent=extent,
                    cmap=cmap,
                    **kwargs,
                )

                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_title(f"Depth section: {dz} A")

        self.clear_device_mem(self._device, self._clear_fft_cache)
        return stack_depth

    def _crop_padded_object(
        self,
        padded_object: np.ndarray,
        remaining_padding: int = 0,
        upsampled: bool = False,
    ):
        """
        Utility function to crop padded object

        Parameters
        ----------
        padded_object: np.ndarray
            Padded object to be cropped
        remaining_padding: int, optional
            Padding to leave uncropped

        Returns
        -------
        cropped_object: np.ndarray
            Cropped object

        """

        asnumpy = self._asnumpy

        if upsampled:
            pad_x = np.round(
                self._object_padding_px[0] * self._kde_upsample_factor
            ).astype("int")
            pad_x_left = np.round(
                self._object_padding_px[0] / 2 * self._kde_upsample_factor
            ).astype("int")
            pad_x_right = pad_x_left - pad_x

            pad_y = np.round(
                self._object_padding_px[1] * self._kde_upsample_factor
            ).astype("int")
            pad_y_left = np.round(
                self._object_padding_px[1] / 2 * self._kde_upsample_factor
            ).astype("int")
            pad_y_right = pad_y_left - pad_y

        else:
            pad_x_left = self._object_padding_px[0] // 2
            pad_x_right = pad_x_left - self._object_padding_px[0]
            pad_y_left = self._object_padding_px[1] // 2
            pad_y_right = pad_y_left - self._object_padding_px[1]

        pad_x_left -= remaining_padding
        pad_x_right += remaining_padding
        pad_y_left -= remaining_padding
        pad_y_right += remaining_padding

        sx = slice(
            pad_x_left if pad_x_left else None, pad_x_right if pad_x_right else None
        )
        sy = slice(
            pad_y_left if pad_y_left else None, pad_y_right if pad_y_right else None
        )

        return asnumpy(padded_object[sx, sy])

    def _visualize_figax(
        self,
        fig,
        ax,
        remaining_padding: int = 0,
        upsampled: bool = False,
        **kwargs,
    ):
        """
        Utility function to visualize bright field average on given fig/ax

        Parameters
        ----------
        fig: Figure
            Matplotlib figure ax lives in
        ax: Axes
            Matplotlib axes to plot bright field average in
        remaining_padding: int, optional
            Padding to leave uncropped

        """

        cmap = kwargs.pop("cmap", "magma")

        if upsampled:
            cropped_object = self._crop_padded_object(
                self._recon_BF_subpixel_aligned, remaining_padding, upsampled
            )

            extent = [
                0,
                self._scan_sampling[1]
                * cropped_object.shape[1]
                / self._kde_upsample_factor,
                self._scan_sampling[0]
                * cropped_object.shape[0]
                / self._kde_upsample_factor,
                0,
            ]

        else:
            cropped_object = self._crop_padded_object(self._recon_BF, remaining_padding)

            extent = [
                0,
                self._scan_sampling[1] * cropped_object.shape[1],
                self._scan_sampling[0] * cropped_object.shape[0],
                0,
            ]

        ax.imshow(
            cropped_object,
            extent=extent,
            cmap=cmap,
            **kwargs,
        )

    def show_shifts(
        self,
        shifts_ang=None,
        scale_arrows=1,
        plot_arrow_freq=1,
        plot_rotated_shifts=True,
        figax=None,
        **kwargs,
    ):
        """
        Utility function to visualize bright field disk pixel shifts

        Parameters
        ----------
        shifts_ang: np.ndarray, optional
            If None, self._xy_shifts is used
        scale_arrows: float, optional
            Scale to multiply shifts by
        plot_arrow_freq: int, optional
            Frequency of shifts to plot in quiver plot
        plot_rotated_shifts: bool, optional
            If True, shifts are plotted with the relative rotation decomposed
        figax: optional
            Tuple of figure, axes to plot against
        """

        xp = self._xp
        asnumpy = self._asnumpy

        color = kwargs.pop("color", (1, 0, 0, 1))

        if shifts_ang is None:
            shifts_px = self._xy_shifts
        else:
            shifts_px = shifts_ang / xp.array(self._scan_sampling)

        shifts = shifts_px * scale_arrows * xp.array(self._reciprocal_sampling)

        if plot_rotated_shifts and hasattr(self, "rotation_Q_to_R_rads"):
            if figax is None:
                figsize = kwargs.pop("figsize", (8, 4))
                fig, ax = plt.subplots(1, 2, figsize=figsize)
            else:
                fig, ax = figax

            rotated_color = kwargs.pop("rotated_color", (0, 0, 0, 1))

            if shifts_ang is None:
                rotated_shifts_px = self._xy_shifts.copy()
            else:
                rotated_shifts_px = shifts_ang / xp.array(self._scan_sampling)

            if self.transpose:
                rotated_shifts_px = xp.flip(rotated_shifts_px, axis=1)

            rotated_shifts = (
                rotated_shifts_px * scale_arrows * xp.array(self._reciprocal_sampling)
            )

        else:
            if figax is None:
                figsize = kwargs.pop("figsize", (4, 4))
                fig, ax = plt.subplots(figsize=figsize)
            else:
                fig, ax = figax

        dp_mask_ind = xp.nonzero(self._dp_mask)
        yy, xx = xp.meshgrid(
            xp.arange(self._region_of_interest_shape[1]),
            xp.arange(self._region_of_interest_shape[0]),
        )
        freq_mask = xp.logical_and(xx % plot_arrow_freq == 0, yy % plot_arrow_freq == 0)
        masked_ind = xp.logical_and(freq_mask, self._dp_mask)
        plot_ind = masked_ind[dp_mask_ind]

        kr_max = xp.max(self._kr)
        if plot_rotated_shifts and hasattr(self, "rotation_Q_to_R_rads"):
            ax[0].quiver(
                asnumpy(self._kxy[plot_ind, 1]),
                asnumpy(self._kxy[plot_ind, 0]),
                asnumpy(shifts[plot_ind, 1]),
                asnumpy(shifts[plot_ind, 0]),
                color=color,
                angles="xy",
                scale_units="xy",
                scale=1,
                **kwargs,
            )

            ax[0].set_xlim([-1.2 * kr_max, 1.2 * kr_max])
            ax[0].set_ylim([-1.2 * kr_max, 1.2 * kr_max])
            ax[0].set_title("Measured Bright Field Shifts")
            ax[0].set_ylabel(r"$k_x$ [$A^{-1}$]")
            ax[0].set_xlabel(r"$k_y$ [$A^{-1}$]")
            ax[0].set_aspect("equal")

            # passive coordinate rotation
            tf_T = AffineTransform(angle=-self.rotation_Q_to_R_rads)
            rotated_kxy = tf_T(self._kxy[plot_ind], xp=xp)
            ax[1].quiver(
                asnumpy(rotated_kxy[:, 1]),
                asnumpy(rotated_kxy[:, 0]),
                asnumpy(rotated_shifts[plot_ind, 1]),
                asnumpy(rotated_shifts[plot_ind, 0]),
                angles="xy",
                scale_units="xy",
                scale=1,
                color=rotated_color,
                **kwargs,
            )

            ax[1].set_xlim([-1.2 * kr_max, 1.2 * kr_max])
            ax[1].set_ylim([-1.2 * kr_max, 1.2 * kr_max])
            ax[1].set_title("Rotated Bright Field Shifts")
            ax[1].set_ylabel(r"$k_x$ [$A^{-1}$]")
            ax[1].set_xlabel(r"$k_y$ [$A^{-1}$]")
            ax[1].set_aspect("equal")
        else:
            ax.quiver(
                asnumpy(self._kxy[plot_ind, 1]),
                asnumpy(self._kxy[plot_ind, 0]),
                asnumpy(shifts[plot_ind, 1]),
                asnumpy(shifts[plot_ind, 0]),
                color=color,
                angles="xy",
                scale_units="xy",
                scale=1,
                **kwargs,
            )

            ax.set_xlim([-1.2 * kr_max, 1.2 * kr_max])
            ax.set_ylim([-1.2 * kr_max, 1.2 * kr_max])
            ax.set_title("Measured BF Shifts")
            ax.set_ylabel(r"$k_x$ [$A^{-1}$]")
            ax.set_xlabel(r"$k_y$ [$A^{-1}$]")
            ax.set_aspect("equal")

        fig.tight_layout()

    def show_probe_position_shifts(
        self,
        **kwargs,
    ):
        """
        Utility function to visualize probe-position shifts.
        """
        probe_dx = self._crop_padded_object(self._probe_dx)
        probe_dy = self._crop_padded_object(self._probe_dy)
        max_shift = np.abs(np.dstack((probe_dx, probe_dy))).max()

        figsize = kwargs.pop("figsize", (9, 4))
        vmin = kwargs.pop("vmin", -max_shift)
        vmax = kwargs.pop("vmax", max_shift)
        cmap = kwargs.pop("cmap", "PuOr")

        extent = [
            0,
            self._scan_sampling[1] * probe_dx.shape[1],
            self._scan_sampling[0] * probe_dx.shape[0],
            0,
        ]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        im1 = ax1.imshow(probe_dx, extent=extent, vmin=vmin, vmax=vmax, cmap=cmap)
        im2 = ax2.imshow(probe_dy, extent=extent, vmin=vmin, vmax=vmax, cmap=cmap)

        for ax, im in zip([ax1, ax2], [im1, im2]):
            divider = make_axes_locatable(ax)
            ax_cb = divider.append_axes("right", size="5%", pad="2.5%")
            fig.add_axes(ax_cb)
            cb = fig.colorbar(im, cax=ax_cb)
            cb.set_label("pix", rotation=0, ha="center", va="bottom")
            cb.ax.yaxis.set_label_coords(0.5, 1.01)
            ax.set_ylabel("x [A]")
            ax.set_xlabel("y [A]")

        ax1.set_title("Probe Position Vertical Shifts")
        ax2.set_title("Probe Position Horizontal Shifts")

        fig.tight_layout()

    def visualize(
        self,
        **kwargs,
    ):
        """
        Visualization function for bright field average

        Returns
        --------
        self: BFReconstruction
            Self to accommodate chaining
        """

        figsize = kwargs.pop("figsize", (6, 6))

        fig, ax = plt.subplots(figsize=figsize)

        self._visualize_figax(fig, ax, **kwargs)

        ax.set_ylabel("x [A]")
        ax.set_xlabel("y [A]")
        ax.set_title("Reconstructed Bright Field Image")

        return self

    @property
    def object_cropped(self):
        """cropped object"""
        if hasattr(self, "_recon_phase_corrected"):
            if hasattr(self, "_kde_upsample_factor"):
                return self._crop_padded_object(
                    self._recon_phase_corrected, upsampled=True
                )
            else:
                return self._crop_padded_object(self._recon_phase_corrected)
        else:
            if hasattr(self, "_kde_upsample_factor"):
                return self._crop_padded_object(
                    self._recon_BF_subpixel_aligned, upsampled=True
                )
            else:
                return self._crop_padded_object(self._recon_BF)
