"""
Module for reconstructing phase objects from 4DSTEM datasets using iterative methods,
namely x-ray magnetic ptychography.
"""

import warnings
from typing import Mapping, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from py4DSTEM.visualize.vis_special import (
    Complex2RGB,
    add_colorbar_arg,
    return_scaled_histogram_ordering,
)

try:
    import cupy as cp
except (ImportError, ModuleNotFoundError):
    cp = np

from emdfile import Custom, tqdmnd
from py4DSTEM import DataCube
from py4DSTEM.process.phase.phase_base_class import PtychographicReconstruction
from py4DSTEM.process.phase.ptychographic_constraints import (
    ObjectNDConstraintsMixin,
    PositionsConstraintsMixin,
    ProbeConstraintsMixin,
)
from py4DSTEM.process.phase.ptychographic_methods import (
    MultipleMeasurementsMethodsMixin,
    ObjectNDMethodsMixin,
    ObjectNDProbeMethodsMixin,
    ProbeMethodsMixin,
)
from py4DSTEM.process.phase.ptychographic_visualizations import VisualizationsMixin
from py4DSTEM.process.phase.utils import (
    ComplexProbe,
    copy_to_device,
    fft_shift,
    generate_batches,
    polar_aliases,
    polar_symbols,
)


class XRayMagneticPtychography(
    VisualizationsMixin,
    PositionsConstraintsMixin,
    ProbeConstraintsMixin,
    ObjectNDConstraintsMixin,
    MultipleMeasurementsMethodsMixin,
    ObjectNDProbeMethodsMixin,
    ProbeMethodsMixin,
    ObjectNDMethodsMixin,
    PtychographicReconstruction,
):
    """
    Iterative X-Ray Magnetic Ptychographic Reconstruction Class.

    Diffraction intensities dimensions         : (Rx,Ry,Qx,Qy) (for each measurement)
    Reconstructed probe dimensions             : (Sx,Sy)
    Reconstructed electrostatic dimensions     : (Px,Py)
    Reconstructed magnetic dimensions          : (Px,Py)

    such that (Sx,Sy) is the region-of-interest (ROI) size of our probe
    and (Px,Py) is the padded-object size we position our ROI around in.

    Parameters
    ----------
    datacube: Sequence[DataCube]
        Tuple of input 4D diffraction pattern intensities
    energy: float
        The electron energy of the wave functions in eV
    magnetic_contribution_sign: str, optional
        One of '-+', '-0+', '0+'
    semiangle_cutoff: float, optional
        Semiangle cutoff for the initial probe guess in mrad
    semiangle_cutoff_pixels: float, optional
        Semiangle cutoff for the initial probe guess in pixels
    rolloff: float, optional
        Semiangle rolloff for the initial probe guess
    vacuum_probe_intensity: np.ndarray, optional
        Vacuum probe to use as intensity aperture for initial probe guess
    polar_parameters: dict, optional
        Mapping from aberration symbols to their corresponding values. All aberration
        magnitudes should be given in Å and angles should be given in radians.
    object_padding_px: Tuple[int,int], optional
        Pixel dimensions to pad objects with
        If None, the padding is set to half the probe ROI dimensions
    positions_mask: np.ndarray, optional
        Boolean real space mask to select positions in datacube to skip for reconstruction
    initial_object_guess: np.ndarray, optional
        Initial guess for complex-valued object of dimensions (2,Px,Py)
        If None, initialized to 1.0j for complex objects and 0.0 for potential objects
    initial_probe_guess: np.ndarray, optional
        Initial guess for complex-valued probe of dimensions (Sx,Sy). If None,
        initialized to ComplexProbe with semiangle_cutoff, energy, and aberrations
    initial_scan_positions: np.ndarray, optional
        Probe positions in Å for each diffraction intensity
        If None, initialized to a grid scan
    object_fov_ang: Tuple[int,int], optional
        Fixed object field of view in Å. If None, the fov is initialized using the
        probe positions and object_padding_px
    positions_offset_ang: np.ndarray, optional
        Offset of positions in A
    verbose: bool, optional
        If True, class methods will inherit this and print additional information
    device: str, optional
        Calculation device will be perfomed on. Must be 'cpu' or 'gpu'
    storage: str, optional
        Device non-frequent arrays will be stored on. Must be 'cpu' or 'gpu'
    clear_fft_cache: bool, optional
        If True, and device = 'gpu', clears the cached fft plan at the end of function calls
    object_type: str, optional
        The object can be reconstructed as a real potential ('potential') or a complex
        object ('complex')
    name: str, optional
        Class name
    kwargs:
        Provide the aberration coefficients as keyword arguments.
    """

    # Class-specific Metadata
    _class_specific_metadata = ("_magnetic_contribution_sign",)

    def __init__(
        self,
        energy: float,
        datacube: Sequence[DataCube] = None,
        magnetic_contribution_sign: str = "-+",
        semiangle_cutoff: float = None,
        semiangle_cutoff_pixels: float = None,
        rolloff: float = 2.0,
        vacuum_probe_intensity: np.ndarray = None,
        polar_parameters: Mapping[str, float] = None,
        object_padding_px: Tuple[int, int] = None,
        positions_mask: np.ndarray = None,
        initial_object_guess: np.ndarray = None,
        initial_probe_guess: np.ndarray = None,
        initial_scan_positions: np.ndarray = None,
        object_fov_ang: Tuple[float, float] = None,
        positions_offset_ang: np.ndarray = None,
        object_type: str = "complex",
        verbose: bool = True,
        device: str = "cpu",
        storage: str = None,
        clear_fft_cache: bool = True,
        name: str = "xray_magnetic_ptychographic_reconstruction",
        **kwargs,
    ):
        Custom.__init__(self, name=name)

        if storage is None:
            storage = device

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

        if object_type != "complex":
            raise NotImplementedError()

        self.set_save_defaults()

        # Data
        self._datacube = datacube
        self._object = initial_object_guess
        self._probe_init = initial_probe_guess

        # Common Metadata
        self._vacuum_probe_intensity = vacuum_probe_intensity
        self._scan_positions = initial_scan_positions
        self._positions_offset_ang = positions_offset_ang
        self._energy = energy
        self._semiangle_cutoff = semiangle_cutoff
        self._semiangle_cutoff_pixels = semiangle_cutoff_pixels
        self._rolloff = rolloff
        self._object_type = object_type
        self._object_padding_px = object_padding_px
        self._object_fov_ang = object_fov_ang
        self._positions_mask = positions_mask
        self._verbose = verbose
        self._preprocessed = False

        # Class-specific Metadata
        self._magnetic_contribution_sign = magnetic_contribution_sign

    def preprocess(
        self,
        diffraction_intensities_shape: Tuple[int, int] = None,
        reshaping_method: str = "bilinear",
        shifting_interpolation_order: int = 3,
        padded_diffraction_intensities_shape: Tuple[int, int] = None,
        region_of_interest_shape: Tuple[int, int] = None,
        dp_mask: np.ndarray = None,
        in_place_datacube_modification: bool = False,
        fit_function: str = "plane",
        plot_rotation: bool = True,
        maximize_divergence: bool = False,
        rotation_angles_deg: np.ndarray = None,
        plot_probe_overlaps: bool = True,
        force_com_rotation: float = None,
        force_com_transpose: float = None,
        force_com_shifts: Sequence[np.ndarray] = None,
        force_com_measured: Sequence[np.ndarray] = None,
        vectorized_com_calculation: bool = True,
        force_scan_sampling: float = None,
        force_angular_sampling: float = None,
        force_reciprocal_sampling: float = None,
        progress_bar: bool = True,
        object_fov_mask: np.ndarray = True,
        crop_patterns: bool = False,
        center_positions_in_fov: bool = True,
        store_initial_arrays: bool = True,
        device: str = None,
        clear_fft_cache: bool = None,
        max_batch_size: int = None,
        **kwargs,
    ):
        """
        Ptychographic preprocessing step.
        Calls the base class methods:

        _extract_intensities_and_calibrations_from_datacube,
        _compute_center_of_mass(),
        _solve_CoM_rotation(),
        _normalize_diffraction_intensities()
        _calculate_scan_positions_in_px()

        Additionally, it initializes an (Px,Py) array of 1.0j
        and a complex probe using the specified polar parameters.

        Parameters
        ----------
        diffraction_intensities_shape: Tuple[int,int], optional
            Pixel dimensions (Qx',Qy') of the resampled diffraction intensities
            If None, no resampling of diffraction intenstities is performed
        reshaping_method: str, optional
            Method to use for reshaping, either 'bin, 'bilinear', or 'fourier' (default)
        shifting_interpolation_order: int
            Spline interpolation order used in shifting DPs to origin. Default is bi-cubic.
        padded_diffraction_intensities_shape: (int,int), optional
            Padded diffraction intensities shape.
            If None, no padding is performed
        region_of_interest_shape: (int,int), optional
            If not None, explicitly sets region_of_interest_shape and resamples exit_waves
            at the diffraction plane to allow comparison with experimental data
        dp_mask: ndarray, optional
            Mask for datacube intensities (Qx,Qy)
        in_place_datacube_modification: bool, optional
            If True, the datacube will be preprocessed in-place. Note this is not possible
            when either crop_patterns or positions_mask are used.
        fit_function: str, optional
            2D fitting function for CoM fitting. One of 'plane','parabola','bezier_two'
        plot_rotation: bool, optional
            If True, the CoM curl minimization search result will be displayed
        maximize_divergence: bool, optional
            If True, the divergence of the CoM gradient vector field is maximized
        rotation_angles_deg: np.darray, optional
            Array of angles in degrees to perform curl minimization over
        plot_probe_overlaps: bool, optional
            If True, initial probe overlaps scanned over the object will be displayed
        force_com_rotation: float (degrees), optional
            Force relative rotation angle between real and reciprocal space
        force_com_transpose: bool, optional
            Force whether diffraction intensities need to be transposed.
        force_com_shifts: sequence of tuples of ndarrays (CoMx, CoMy)
            Amplitudes come from diffraction patterns shifted with
            the CoM in the upper left corner for each probe unless
            shift is overwritten.
        force_com_measured: tuple of ndarrays (CoMx measured, CoMy measured)
            Force CoM measured shifts
        vectorized_com_calculation: bool, optional
            If True (default), the memory-intensive CoM calculation is vectorized
        force_scan_sampling: float, optional
            Override DataCube real space scan pixel size calibrations, in Angstrom
        force_angular_sampling: float, optional
            Override DataCube reciprocal pixel size calibration, in mrad
        force_reciprocal_sampling: float, optional
            Override DataCube reciprocal pixel size calibration, in A^-1
        object_fov_mask: np.ndarray (boolean)
            Boolean mask of FOV. Used to calculate additional shrinkage of object
            If None, probe_overlap intensity is thresholded
        crop_patterns: bool
            if True, crop patterns to avoid wrap around of patterns when centering
        center_positions_in_fov: bool
            If True (default), probe positions are centered in the fov.
        store_initial_arrays: bool
            If True, preprocesed object and probe arrays are stored allowing reset=True in reconstruct.
        device: str, optional
            if not none, overwrites self._device to set device preprocess will be perfomed on.
        clear_fft_cache: bool, optional
            if true, and device = 'gpu', clears the cached fft plan at the end of function calls
        max_batch_size: int, optional
            Max number of probes to use at once in computing probe overlaps

        Returns
        --------
        self: PtychographicReconstruction
            Self to accommodate chaining
        """
        # handle device/storage
        self.set_device(device, clear_fft_cache)

        xp = self._xp
        device = self._device
        xp_storage = self._xp_storage
        storage = self._storage
        asnumpy = self._asnumpy

        # set additional metadata
        self._diffraction_intensities_shape = diffraction_intensities_shape
        self._reshaping_method = reshaping_method
        self._padded_diffraction_intensities_shape = (
            padded_diffraction_intensities_shape
        )
        self._dp_mask = dp_mask

        if self._datacube is None:
            raise ValueError(
                (
                    "The preprocess() method requires a DataCube. "
                    "Please run ptycho.attach_datacube(DataCube) first."
                )
            )

        if self._magnetic_contribution_sign == "-+":
            self._recon_mode = 0
            self._num_measurements = 2
            magnetic_contribution_msg = (
                "Magnetic contribution sign in first meaurement assumed to be negative.\n"
                "Magnetic contribution sign in second meaurement assumed to be positive."
            )

        elif self._magnetic_contribution_sign == "-0+":
            self._recon_mode = 1
            self._num_measurements = 3
            magnetic_contribution_msg = (
                "Magnetic contribution sign in first meaurement assumed to be negative.\n"
                "Magnetic contribution assumed to be zero in second meaurement.\n"
                "Magnetic contribution sign in third meaurement assumed to be positive."
            )

        elif self._magnetic_contribution_sign == "0+":
            self._recon_mode = 2
            self._num_measurements = 2
            magnetic_contribution_msg = (
                "Magnetic contribution assumed to be zero in first meaurement.\n"
                "Magnetic contribution sign in second meaurement assumed to be positive."
            )
        else:
            raise ValueError(
                f"magnetic_contribution_sign must be either '-+', '-0+', or '0+', not {self._magnetic_contribution_sign}"
            )

        if self._verbose:
            warnings.warn(
                magnetic_contribution_msg,
                UserWarning,
            )

        if len(self._datacube) != self._num_measurements:
            raise ValueError(
                f"datacube must be the same length as magnetic_contribution_sign, not length {len(self._datacube)}."
            )

        if self._positions_mask is not None:
            self._positions_mask = np.asarray(self._positions_mask, dtype="bool")

            if self._positions_mask.ndim == 2:
                warnings.warn(
                    "2D `positions_mask` assumed the same for all measurements.",
                    UserWarning,
                )
                self._positions_mask = np.tile(
                    self._positions_mask, (self._num_measurements, 1, 1)
                )

            num_probes_per_measurement = np.insert(
                self._positions_mask.sum(axis=(-2, -1)), 0, 0
            )

        else:
            self._positions_mask = [None] * self._num_measurements
            num_probes_per_measurement = [0] + [dc.R_N for dc in self._datacube]
            num_probes_per_measurement = np.array(num_probes_per_measurement)

        # prepopulate relevant arrays
        self._mean_diffraction_intensity = []
        self._num_diffraction_patterns = num_probes_per_measurement.sum()
        self._cum_probes_per_measurement = np.cumsum(num_probes_per_measurement)
        self._positions_px_all = np.empty((self._num_diffraction_patterns, 2))

        # calculate roi_shape
        roi_shape = self._datacube[0].Qshape
        if diffraction_intensities_shape is not None:
            roi_shape = diffraction_intensities_shape
        if padded_diffraction_intensities_shape is not None:
            roi_shape = tuple(
                max(q, s)
                for q, s in zip(roi_shape, padded_diffraction_intensities_shape)
            )

        self._amplitudes = xp_storage.empty(
            (self._num_diffraction_patterns,) + roi_shape
        )

        self._amplitudes_shape = np.array(self._amplitudes.shape[-2:])
        if region_of_interest_shape is not None:
            self._resample_exit_waves = True
            self._region_of_interest_shape = np.array(region_of_interest_shape)
        else:
            self._resample_exit_waves = False
            self._region_of_interest_shape = np.array(self._amplitudes.shape[-2:])

        # TO-DO: generalize this
        if force_com_shifts is None:
            force_com_shifts = [None] * self._num_measurements

        if force_com_measured is None:
            force_com_measured = [None] * self._num_measurements

        if self._scan_positions is None:
            self._scan_positions = [None] * self._num_measurements

        if self._positions_offset_ang is None:
            self._positions_offset_ang = [None] * self._num_measurements

        # Ensure plot_center_of_mass is not in kwargs
        kwargs.pop("plot_center_of_mass", None)

        if progress_bar:
            # turn off verbosity to play nice with tqdm
            verbose = self._verbose
            self._verbose = False

        # loop over DPs for preprocessing
        for index in tqdmnd(
            self._num_measurements,
            desc="Preprocessing data",
            unit="measurement",
            disable=not progress_bar,
        ):
            # preprocess datacube, vacuum and masks only for first measurement
            if index == 0:
                (
                    self._datacube[index],
                    self._vacuum_probe_intensity,
                    self._dp_mask,
                    force_com_shifts[index],
                    force_com_measured[index],
                ) = self._preprocess_datacube_and_vacuum_probe(
                    self._datacube[index],
                    diffraction_intensities_shape=self._diffraction_intensities_shape,
                    reshaping_method=self._reshaping_method,
                    padded_diffraction_intensities_shape=self._padded_diffraction_intensities_shape,
                    vacuum_probe_intensity=self._vacuum_probe_intensity,
                    dp_mask=self._dp_mask,
                    com_shifts=force_com_shifts[index],
                    com_measured=force_com_measured[index],
                )

            else:
                (
                    self._datacube[index],
                    _,
                    _,
                    force_com_shifts[index],
                    force_com_measured[index],
                ) = self._preprocess_datacube_and_vacuum_probe(
                    self._datacube[index],
                    diffraction_intensities_shape=self._diffraction_intensities_shape,
                    reshaping_method=self._reshaping_method,
                    padded_diffraction_intensities_shape=self._padded_diffraction_intensities_shape,
                    vacuum_probe_intensity=None,
                    dp_mask=None,
                    com_shifts=force_com_shifts[index],
                    com_measured=force_com_measured[index],
                )

            # calibrations
            intensities = self._extract_intensities_and_calibrations_from_datacube(
                self._datacube[index],
                require_calibrations=True,
                force_scan_sampling=force_scan_sampling,
                force_angular_sampling=force_angular_sampling,
                force_reciprocal_sampling=force_reciprocal_sampling,
            )

            # calculate CoM
            (
                com_measured_x,
                com_measured_y,
                com_fitted_x,
                com_fitted_y,
                com_normalized_x,
                com_normalized_y,
            ) = self._calculate_intensities_center_of_mass(
                intensities,
                dp_mask=self._dp_mask,
                fit_function=fit_function,
                com_shifts=force_com_shifts[index],
                vectorized_calculation=vectorized_com_calculation,
                com_measured=force_com_measured[index],
            )

            # estimate rotation / transpose using first measurement
            if index == 0:
                # silence warnings to play nice with progress bar
                verbose = self._verbose
                self._verbose = False

                (
                    self._rotation_best_rad,
                    self._rotation_best_transpose,
                    _com_x,
                    _com_y,
                ) = self._solve_for_center_of_mass_relative_rotation(
                    com_measured_x,
                    com_measured_y,
                    com_normalized_x,
                    com_normalized_y,
                    rotation_angles_deg=rotation_angles_deg,
                    plot_rotation=plot_rotation,
                    plot_center_of_mass=False,
                    maximize_divergence=maximize_divergence,
                    force_com_rotation=force_com_rotation,
                    force_com_transpose=force_com_transpose,
                    **kwargs,
                )
                self._verbose = verbose

            # corner-center amplitudes
            idx_start = self._cum_probes_per_measurement[index]
            idx_end = self._cum_probes_per_measurement[index + 1]

            (
                amplitudes,
                mean_diffraction_intensity_temp,
                self._crop_mask,
                self._crop_mask_shape,
            ) = self._normalize_diffraction_intensities(
                intensities,
                com_fitted_x,
                com_fitted_y,
                self._positions_mask[index],
                crop_patterns,
                in_place_datacube_modification,
                shifting_interpolation_order=shifting_interpolation_order,
            )

            self._mean_diffraction_intensity.append(mean_diffraction_intensity_temp)

            # explicitly transfer arrays to storage
            self._amplitudes[idx_start:idx_end] = copy_to_device(amplitudes, storage)

            del (
                intensities,
                amplitudes,
                com_measured_x,
                com_measured_y,
                com_fitted_x,
                com_fitted_y,
                com_normalized_x,
                com_normalized_y,
            )

            # initialize probe positions
            (
                self._positions_px_all[idx_start:idx_end],
                self._object_padding_px,
            ) = self._calculate_scan_positions_in_pixels(
                self._scan_positions[index],
                self._positions_mask[index],
                self._object_padding_px,
                self._positions_offset_ang[index],
            )

        if progress_bar:
            # reset verbosity
            self._verbose = verbose

        # handle semiangle specified in pixels
        if self._semiangle_cutoff_pixels:
            self._semiangle_cutoff = (
                self._semiangle_cutoff_pixels * self._angular_sampling[0]
            )

        # Object Initialization
        obj = self._initialize_object(
            self._object,
            self._positions_px_all,
            self._object_type,
        )

        if self._object is None:
            # complex zeros instead of ones, since we store pre-exponential terms
            self._object = xp.zeros((2,) + obj.shape, dtype=obj.dtype)
        else:
            self._object = obj

        if store_initial_arrays:
            self._object_initial = self._object.copy()
            self._object_type_initial = self._object_type
        self._object_shape = self._object.shape[-2:]

        # center probe positions
        self._positions_px_all = xp_storage.asarray(
            self._positions_px_all, dtype=xp_storage.float32
        )

        if center_positions_in_fov:
            for index in range(self._num_measurements):
                idx_start = self._cum_probes_per_measurement[index]
                idx_end = self._cum_probes_per_measurement[index + 1]

                positions_px = self._positions_px_all[idx_start:idx_end]
                positions_px_com = positions_px.mean(0)
                positions_px -= (
                    positions_px_com - xp_storage.array(self._object_shape) / 2
                )
                self._positions_px_all[idx_start:idx_end] = positions_px.copy()

        self._positions_px_initial_all = self._positions_px_all.copy()
        self._positions_initial_all = self._positions_px_initial_all.copy()
        self._positions_initial_all[:, 0] *= self.sampling[0]
        self._positions_initial_all[:, 1] *= self.sampling[1]

        self._positions_initial = self._return_average_positions()
        if self._positions_initial is not None:
            self._positions_initial[:, 0] *= self.sampling[0]
            self._positions_initial[:, 1] *= self.sampling[1]

        # initialize probe
        self._probes_all = []
        list_Q = isinstance(self._probe_init, (list, tuple))

        if store_initial_arrays:
            self._probes_all_initial = []
            self._probes_all_initial_aperture = []
        else:
            self._probes_all_initial_aperture = [None] * self._num_measurements

        for index in range(self._num_measurements):
            _probe, self._semiangle_cutoff = self._initialize_probe(
                self._probe_init[index] if list_Q else self._probe_init,
                self._vacuum_probe_intensity,
                self._mean_diffraction_intensity[index],
                self._semiangle_cutoff,
                crop_patterns,
            )

            self._probes_all.append(_probe)
            if store_initial_arrays:
                self._probes_all_initial.append(_probe.copy())
                self._probes_all_initial_aperture.append(xp.abs(xp.fft.fft2(_probe)))

        del self._probe_init

        # initialize aberrations
        self._known_aberrations_array = ComplexProbe(
            energy=self._energy,
            gpts=self._region_of_interest_shape,
            sampling=self.sampling,
            parameters=self._polar_parameters,
            device=self._device,
        )._evaluate_ctf()

        if object_fov_mask is None or plot_probe_overlaps:
            # overlaps
            if max_batch_size is None:
                max_batch_size = self._num_diffraction_patterns

            probe_overlap = xp.zeros(self._object_shape, dtype=xp.float32)

            for start, end in generate_batches(
                self._cum_probes_per_measurement[1], max_batch=max_batch_size
            ):
                # batch indices
                positions_px = self._positions_px_all[start:end]
                positions_px_fractional = positions_px - xp_storage.round(positions_px)

                shifted_probes = fft_shift(
                    self._probes_all[0], positions_px_fractional, xp
                )
                probe_overlap += self._sum_overlapping_patches_bincounts(
                    xp.abs(shifted_probes) ** 2, positions_px
                )

            del shifted_probes

        # initialize object_fov_mask
        if object_fov_mask is None:
            gaussian_filter = self._scipy.ndimage.gaussian_filter
            probe_overlap_blurred = gaussian_filter(probe_overlap, 1.0)
            self._object_fov_mask = asnumpy(
                probe_overlap_blurred > 0.25 * probe_overlap_blurred.max()
            )
            del probe_overlap_blurred
        elif object_fov_mask is True:
            self._object_fov_mask = np.full(self._object_shape, True)
        else:
            self._object_fov_mask = np.asarray(object_fov_mask)
        self._object_fov_mask_inverse = np.invert(self._object_fov_mask)

        # plot probe overlaps
        if plot_probe_overlaps:
            probe_overlap = asnumpy(probe_overlap)
            figsize = kwargs.pop("figsize", (9, 4))
            chroma_boost = kwargs.pop("chroma_boost", 1)
            power = kwargs.pop("power", 2)

            # initial probe
            complex_probe_rgb = Complex2RGB(
                self.probe_centered[0],
                power=power,
                chroma_boost=chroma_boost,
            )

            extent = [
                0,
                self.sampling[1] * self._object_shape[1],
                self.sampling[0] * self._object_shape[0],
                0,
            ]

            probe_extent = [
                0,
                self.sampling[1] * self._region_of_interest_shape[1],
                self.sampling[0] * self._region_of_interest_shape[0],
                0,
            ]

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

            ax1.imshow(
                complex_probe_rgb,
                extent=probe_extent,
            )

            divider = make_axes_locatable(ax1)
            cax1 = divider.append_axes("right", size="5%", pad="2.5%")
            add_colorbar_arg(cax1, chroma_boost=chroma_boost)
            ax1.set_ylabel("x [A]")
            ax1.set_xlabel("y [A]")
            ax1.set_title("Initial probe intensity")

            ax2.imshow(
                probe_overlap,
                extent=extent,
                cmap="gray",
            )
            ax2.scatter(
                self.positions[0, :, 1],
                self.positions[0, :, 0],
                s=2.5,
                color=(1, 0, 0, 1),
            )
            ax2.set_ylabel("x [A]")
            ax2.set_xlabel("y [A]")
            ax2.set_xlim((extent[0], extent[1]))
            ax2.set_ylim((extent[2], extent[3]))
            ax2.set_title("Object field of view")

            fig.tight_layout()

        self._preprocessed = True
        self.clear_device_mem(self._device, self._clear_fft_cache)

        return self

    def _overlap_projection(
        self,
        current_object,
        vectorized_patch_indices_row,
        vectorized_patch_indices_col,
        shifted_probes,
    ):
        """
        Ptychographic overlap projection method.

        Parameters
        --------
        current_object: np.ndarray
            Current object estimate
        current_probe: np.ndarray
            Current probe estimate

        Returns
        --------
        shifted_probes:np.ndarray
            fractionally-shifted probes
        object_patches: np.ndarray
            Patched object view
        overlap: np.ndarray
            shifted_probes * object_patches
        """

        xp = self._xp

        object_patches = xp.empty(
            (self._num_measurements,) + shifted_probes.shape, dtype=current_object.dtype
        )
        object_patches[0] = current_object[
            0, vectorized_patch_indices_row, vectorized_patch_indices_col
        ]
        object_patches[1] = current_object[
            1, vectorized_patch_indices_row, vectorized_patch_indices_col
        ]

        overlap_base = shifted_probes * xp.exp(1.0j * object_patches[0])

        match (self._recon_mode, self._active_measurement_index):
            case (0, 0) | (1, 0):  # reverse
                overlap = overlap_base * xp.exp(-1.0j * object_patches[1])
            case (0, 1) | (1, 2) | (2, 1):  # forward
                overlap = overlap_base * xp.exp(1.0j * object_patches[1])
            case (1, 1) | (2, 0):  # neutral
                overlap = overlap_base
            case _:
                raise ValueError()

        return shifted_probes, object_patches, overlap

    def _gradient_descent_adjoint(
        self,
        current_object,
        current_probe,
        object_patches,
        shifted_probes,
        positions_px,
        exit_waves,
        step_size,
        normalization_min,
        fix_probe,
    ):
        """
        Ptychographic adjoint operator for GD method.
        Computes object and probe update steps.

        Parameters
        --------
        current_object: np.ndarray
            Current object estimate
        current_probe: np.ndarray
            Current probe estimate
        object_patches: np.ndarray
            Patched object view
        shifted_probes:np.ndarray
            fractionally-shifted probes
        exit_waves:np.ndarray
            Updated exit_waves
        step_size: float, optional
            Update step size
        normalization_min: float, optional
            Probe normalization minimum as a fraction of the maximum overlap intensity
        fix_probe: bool, optional
            If True, probe will not be updated

        Returns
        --------
        updated_object: np.ndarray
            Updated object estimate
        updated_probe: np.ndarray
            Updated probe estimate
        """
        xp = self._xp

        probe_conj = xp.conj(shifted_probes)  # P*
        electrostatic_conj = xp.exp(-1.0j * xp.conj(object_patches[0]))  # exp[-i c]

        probe_electrostatic_abs = xp.abs(probe_conj * electrostatic_conj)
        probe_electrostatic_normalization = self._sum_overlapping_patches_bincounts(
            probe_electrostatic_abs**2,
            positions_px,
        )
        probe_electrostatic_normalization = 1 / xp.sqrt(
            1e-16
            + ((1 - normalization_min) * probe_electrostatic_normalization) ** 2
            + (normalization_min * xp.max(probe_electrostatic_normalization)) ** 2
        )

        match (self._recon_mode, self._active_measurement_index):
            case (0, 0) | (1, 0):  # reverse
                magnetic_conj = xp.exp(1.0j * xp.conj(object_patches[1]))

                probe_magnetic_abs = xp.abs(shifted_probes * magnetic_conj)
                probe_magnetic_normalization = self._sum_overlapping_patches_bincounts(
                    probe_magnetic_abs**2,
                    positions_px,
                )
                probe_magnetic_normalization = 1 / xp.sqrt(
                    1e-16
                    + ((1 - normalization_min) * probe_magnetic_normalization) ** 2
                    + (normalization_min * xp.max(probe_magnetic_normalization)) ** 2
                )

                # - i * exp(i m*) * exp(-i c*) * P
                electrostatic_update = self._sum_overlapping_patches_bincounts(
                    -1.0j
                    * magnetic_conj
                    * electrostatic_conj
                    * probe_conj
                    * exit_waves,
                    positions_px,
                )

                # i * exp(i m*) * exp(-i c*) * P
                magnetic_update = self._sum_overlapping_patches_bincounts(
                    1.0j * magnetic_conj * electrostatic_conj * probe_conj * exit_waves,
                    positions_px,
                )

                current_object[0] += (
                    step_size * electrostatic_update * probe_magnetic_normalization
                )
                current_object[1] += (
                    step_size * magnetic_update * probe_electrostatic_normalization
                )

                if not fix_probe:
                    electrostatic_magnetic_abs = xp.abs(
                        electrostatic_conj * magnetic_conj
                    )
                    electrostatic_magnetic_normalization = xp.sum(
                        electrostatic_magnetic_abs**2,
                        axis=0,
                    )
                    electrostatic_magnetic_normalization = 1 / xp.sqrt(
                        1e-16
                        + (
                            (1 - normalization_min)
                            * electrostatic_magnetic_normalization
                        )
                        ** 2
                        + (
                            normalization_min
                            * xp.max(electrostatic_magnetic_normalization)
                        )
                        ** 2
                    )

                    # exp(i m*) * exp(-i c*)
                    current_probe += step_size * (
                        xp.sum(
                            magnetic_conj * electrostatic_conj * exit_waves,
                            axis=0,
                        )
                        * electrostatic_magnetic_normalization
                    )

            case (0, 1) | (1, 2) | (2, 1):  # forward
                magnetic_conj = xp.exp(-1.0j * xp.conj(object_patches[1]))

                probe_magnetic_abs = xp.abs(shifted_probes * magnetic_conj)
                probe_magnetic_normalization = self._sum_overlapping_patches_bincounts(
                    probe_magnetic_abs**2,
                    positions_px,
                )
                probe_magnetic_normalization = 1 / xp.sqrt(
                    1e-16
                    + ((1 - normalization_min) * probe_magnetic_normalization) ** 2
                    + (normalization_min * xp.max(probe_magnetic_normalization)) ** 2
                )

                # - i * exp(-i m*) * exp(-i c*) * P
                update = self._sum_overlapping_patches_bincounts(
                    -1.0j
                    * magnetic_conj
                    * electrostatic_conj
                    * probe_conj
                    * exit_waves,
                    positions_px,
                )

                current_object[0] += step_size * update * probe_magnetic_normalization
                current_object[1] += (
                    step_size * update * probe_electrostatic_normalization
                )

                if not fix_probe:
                    electrostatic_magnetic_abs = xp.abs(
                        electrostatic_conj * magnetic_conj
                    )
                    electrostatic_magnetic_normalization = xp.sum(
                        electrostatic_magnetic_abs**2,
                        axis=0,
                    )
                    electrostatic_magnetic_normalization = 1 / xp.sqrt(
                        1e-16
                        + (
                            (1 - normalization_min)
                            * electrostatic_magnetic_normalization
                        )
                        ** 2
                        + (
                            normalization_min
                            * xp.max(electrostatic_magnetic_normalization)
                        )
                        ** 2
                    )

                    # exp(i m*) * exp(-i c*)
                    current_probe += step_size * (
                        xp.sum(
                            magnetic_conj * electrostatic_conj * exit_waves,
                            axis=0,
                        )
                        * electrostatic_magnetic_normalization
                    )

            case (1, 1) | (2, 0):  # neutral
                probe_abs = xp.abs(shifted_probes)
                probe_normalization = self._sum_overlapping_patches_bincounts(
                    probe_abs**2,
                    positions_px,
                )
                probe_normalization = 1 / xp.sqrt(
                    1e-16
                    + ((1 - normalization_min) * probe_normalization) ** 2
                    + (normalization_min * xp.max(probe_normalization)) ** 2
                )

                # -i exp(-i c*) * P*
                electrostatic_update = self._sum_overlapping_patches_bincounts(
                    -1.0j * electrostatic_conj * probe_conj * exit_waves,
                    positions_px,
                )

                current_object[0] += (
                    step_size * electrostatic_update * probe_normalization
                )

                if not fix_probe:
                    electrostatic_abs = xp.abs(electrostatic_conj)
                    electrostatic_normalization = xp.sum(
                        electrostatic_abs**2,
                        axis=0,
                    )
                    electrostatic_normalization = 1 / xp.sqrt(
                        1e-16
                        + ((1 - normalization_min) * electrostatic_normalization) ** 2
                        + (normalization_min * xp.max(electrostatic_normalization)) ** 2
                    )

                    # exp(-i c*)
                    current_probe += step_size * (
                        xp.sum(
                            electrostatic_conj * exit_waves,
                            axis=0,
                        )
                        * electrostatic_normalization
                    )

            case _:
                raise ValueError()

        return current_object, current_probe

    def _object_constraints(
        self,
        current_object,
        gaussian_filter,
        gaussian_filter_sigma_e,
        gaussian_filter_sigma_m,
        butterworth_filter,
        butterworth_order,
        q_lowpass_e,
        q_lowpass_m,
        q_highpass_e,
        q_highpass_m,
        tv_denoise,
        tv_denoise_weight,
        tv_denoise_inner_iter,
        **kwargs,
    ):
        """MagneticObjectNDConstraints wrapper function"""

        # smoothness
        if gaussian_filter:
            current_object[0] = self._object_gaussian_constraint(
                current_object[0], gaussian_filter_sigma_e, False
            )
            current_object[1] = self._object_gaussian_constraint(
                current_object[1], gaussian_filter_sigma_m, False
            )
        if butterworth_filter:
            current_object[0] = self._object_butterworth_constraint(
                current_object[0],
                q_lowpass_e,
                q_highpass_e,
                butterworth_order,
            )
            current_object[1] = self._object_butterworth_constraint(
                current_object[1],
                q_lowpass_m,
                q_highpass_m,
                butterworth_order,
            )
        if tv_denoise:
            current_object[0] = self._object_denoise_tv_pylops(
                current_object[0], tv_denoise_weight, tv_denoise_inner_iter
            )

        return current_object

    def reconstruct(
        self,
        num_iter: int = 8,
        reconstruction_method: str = "gradient-descent",
        reconstruction_parameter: float = 1.0,
        reconstruction_parameter_a: float = None,
        reconstruction_parameter_b: float = None,
        reconstruction_parameter_c: float = None,
        max_batch_size: int = None,
        seed_random: int = None,
        step_size: float = 0.5,
        normalization_min: float = 1,
        positions_step_size: float = 0.9,
        fix_probe_com: bool = True,
        fix_probe: bool = False,
        fix_probe_aperture: bool = False,
        constrain_probe_amplitude: bool = False,
        constrain_probe_amplitude_relative_radius: float = 0.5,
        constrain_probe_amplitude_relative_width: float = 0.05,
        constrain_probe_fourier_amplitude: bool = False,
        constrain_probe_fourier_amplitude_max_width_pixels: float = 3.0,
        constrain_probe_fourier_amplitude_constant_intensity: bool = False,
        fix_positions: bool = True,
        fix_positions_com: bool = True,
        max_position_update_distance: float = None,
        max_position_total_distance: float = None,
        global_affine_transformation: bool = False,
        gaussian_filter_sigma_e: float = None,
        gaussian_filter_sigma_m: float = None,
        gaussian_filter: bool = True,
        fit_probe_aberrations: bool = False,
        fit_probe_aberrations_max_angular_order: int = 4,
        fit_probe_aberrations_max_radial_order: int = 4,
        fit_probe_aberrations_remove_initial: bool = False,
        fit_probe_aberrations_using_scikit_image: bool = True,
        butterworth_filter: bool = True,
        q_lowpass_e: float = None,
        q_lowpass_m: float = None,
        q_highpass_e: float = None,
        q_highpass_m: float = None,
        butterworth_order: float = 2,
        tv_denoise: bool = True,
        tv_denoise_weight: float = None,
        tv_denoise_inner_iter: float = 40,
        detector_fourier_mask: np.ndarray = None,
        virtual_detector_masks: Sequence[np.ndarray] = None,
        probe_real_space_support_mask: np.ndarray = None,
        store_iterations: bool = False,
        collective_measurement_updates: bool = True,
        progress_bar: bool = True,
        reset: bool = None,
        device: str = None,
        clear_fft_cache: bool = None,
        object_type: str = None,
    ):
        """
        Ptychographic reconstruction main method.

        Parameters
        --------
        num_iter: int, optional
            Number of iterations to run
        reconstruction_method: str, optional
            Specifies which reconstruction algorithm to use, one of:
            "generalized-projections",
            "DM_AP" (or "difference-map_alternating-projections"),
            "RAAR" (or "relaxed-averaged-alternating-reflections"),
            "RRR" (or "relax-reflect-reflect"),
            "SUPERFLIP" (or "charge-flipping"), or
            "GD" (or "gradient_descent")
        reconstruction_parameter: float, optional
            Reconstruction parameter for various reconstruction methods above.
        reconstruction_parameter_a: float, optional
            Reconstruction parameter a for reconstruction_method='generalized-projections'.
        reconstruction_parameter_b: float, optional
            Reconstruction parameter b for reconstruction_method='generalized-projections'.
        reconstruction_parameter_c: float, optional
            Reconstruction parameter c for reconstruction_method='generalized-projections'.
        max_batch_size: int, optional
            Max number of probes to update at once
        seed_random: int, optional
            Seeds the random number generator, only applicable when max_batch_size is not None
        step_size: float, optional
            Update step size
        normalization_min: float, optional
            Probe normalization minimum as a fraction of the maximum overlap intensity
        positions_step_size: float, optional
            Positions update step size
        pure_phase_object: bool, optional
            If True, object amplitude is set to unity
        fix_probe_com: bool, optional
            If True, fixes center of mass of probe
        fix_probe: bool, optional
            If True, probe is fixed
        fix_probe_aperture: bool, optional
            If True, vaccum probe is used to fix Fourier amplitude
        constrain_probe_amplitude: bool, optional
            If True, real-space probe is constrained with a top-hat support.
        constrain_probe_amplitude_relative_radius: float
            Relative location of top-hat inflection point, between 0 and 0.5
        constrain_probe_amplitude_relative_width: float
            Relative width of top-hat sigmoid, between 0 and 0.5
        constrain_probe_fourier_amplitude: bool, optional
            If True, Fourier-probe is constrained by fitting a sigmoid for each angular frequency
        constrain_probe_fourier_amplitude_max_width_pixels: float
            Maximum pixel width of fitted sigmoid functions.
        constrain_probe_fourier_amplitude_constant_intensity: bool
            If True, the probe aperture is additionally constrained to a constant intensity.
        fix_positions: bool, optional
            If True, probe-positions are fixed
        fix_positions_com: bool, optional
            If True, fixes the positions CoM to the middle of the fov
        max_position_update_distance: float, optional
            Maximum allowed distance for update in A
        max_position_total_distance: float, optional
            Maximum allowed distance from initial positions
        global_affine_transformation: bool, optional
            If True, positions are assumed to be a global affine transform from initial scan
        gaussian_filter_sigma_e: float
            Standard deviation of gaussian kernel for electrostatic object in A
        gaussian_filter_sigma_m: float
            Standard deviation of gaussian kernel for magnetic object in A
        gaussian_filter: bool, optional
            If True and gaussian_filter_sigma is not None, object is smoothed using gaussian filtering
        fit_probe_aberrations: bool, optional
            If True, probe aberrations are fitted to a low-order expansion
        fit_probe_aberrations_max_angular_order: bool
            Max angular order of probe aberrations basis functions
        fit_probe_aberrations_max_radial_order: bool
            Max radial order of probe aberrations basis functions
        fit_probe_aberrations_remove_initial: bool
            If true, initial probe aberrations are removed before fitting
        fit_probe_aberrations_using_scikit_image: bool
            If true, the necessary phase unwrapping is performed using scikit-image. This is more stable, but occasionally leads
            to a documented bug where the kernel hangs..
            If false, a poisson-based solver is used for phase unwrapping. This won't hang, but tends to underestimate aberrations.
        butterworth_filter: bool, optional
            If True and q_lowpass or q_highpass is not None, object is smoothed using butterworth filtering
        q_lowpass_e: float
            Cut-off frequency in A^-1 for low-pass filtering electrostatic object
        q_lowpass_m: float
            Cut-off frequency in A^-1 for low-pass filtering magnetic object
        q_highpass_e: float
            Cut-off frequency in A^-1 for high-pass filtering electrostatic object
        q_highpass_m: float
            Cut-off frequency in A^-1 for high-pass filtering magnetic object
        butterworth_order: float
            Butterworth filter order. Smaller gives a smoother filter
        tv_denoise: bool, optional
            If True and tv_denoise_weight is not None, object is smoothed using TV denoising
        tv_denoise_weight: float
            Denoising weight. The greater `weight`, the more denoising.
        tv_denoise_inner_iter: float
            Number of iterations to run in inner loop of TV denoising
        object_positivity: bool, optional
            If True, forces object to be positive
        shrinkage_rad: float
            Phase shift in radians to be subtracted from the potential at each iteration
        fix_potential_baseline: bool
            If true, the potential mean outside the FOV is forced to zero at each iteration
        detector_fourier_mask: np.ndarray
            Corner-centered mask to multiply the detector-plane gradients with (a value of zero supresses those pixels).
            Useful when detector has artifacts such as dead-pixels. Usually binary.
        virtual_detector_masks: np.ndarray
            List of corner-centered boolean masks for binning forward model exit waves,
            to allow comparison with arbitrary geometry detector datasets.
        probe_real_space_support_mask: np.ndarray
            Corner-centered boolean mask, outside of which the probe amplitude will be set to zero.
        store_iterations: bool, optional
            If True, reconstructed objects and probes are stored at each iteration
        collective_measurement_updates: bool
            if True perform collective updates for all measurements
        progress_bar: bool, optional
            If True, reconstruction progress is displayed
        reset: bool, optional
            If True, previous reconstructions are ignored
        device: str, optional
            if not none, overwrites self._device to set device preprocess will be perfomed on.
        clear_fft_cache: bool, optional
            if true, and device = 'gpu', clears the cached fft plan at the end of function calls
        object_type: str, optional
            Overwrites self._object_type

        Returns
        --------
        self: PtychographicReconstruction
            Self to accommodate chaining
        """
        # handle device/storage
        self.set_device(device, clear_fft_cache)

        if device is not None:
            attrs = [
                "_known_aberrations_array",
                "_object",
                "_object_initial",
                "_probes_all",
                "_probes_all_initial",
                "_probes_all_initial_aperture",
            ]
            self.copy_attributes_to_device(attrs, device)

        xp = self._xp
        xp_storage = self._xp_storage
        device = self._device
        asnumpy = self._asnumpy

        if not collective_measurement_updates and self._verbose:
            warnings.warn(
                "Magnetic ptychography is much more robust with `collective_measurement_updates=True`.",
                UserWarning,
            )

        # set and report reconstruction method
        (
            use_projection_scheme,
            projection_a,
            projection_b,
            projection_c,
            reconstruction_parameter,
            step_size,
        ) = self._set_reconstruction_method_parameters(
            reconstruction_method,
            reconstruction_parameter,
            reconstruction_parameter_a,
            reconstruction_parameter_b,
            reconstruction_parameter_c,
            step_size,
        )

        if use_projection_scheme:
            raise NotImplementedError(
                "Magnetic ptychography is currently only implemented for gradient descent."
            )

        # initialization
        self._reset_reconstruction(store_iterations, reset, use_projection_scheme)

        if object_type is not None:
            self._switch_object_type(object_type)

        if self._verbose:
            self._report_reconstruction_summary(
                num_iter,
                use_projection_scheme,
                reconstruction_method,
                reconstruction_parameter,
                projection_a,
                projection_b,
                projection_c,
                normalization_min,
                step_size,
                max_batch_size,
            )

        if max_batch_size is not None:
            np.random.seed(seed_random)
        else:
            max_batch_size = self._num_diffraction_patterns

        if detector_fourier_mask is not None:
            detector_fourier_mask = xp.asarray(detector_fourier_mask)

        if virtual_detector_masks is not None:
            virtual_detector_masks = xp.asarray(virtual_detector_masks).astype(xp.bool_)

        if gaussian_filter_sigma_m is None:
            gaussian_filter_sigma_m = gaussian_filter_sigma_e

        if q_lowpass_m is None:
            q_lowpass_m = q_lowpass_e

        # main loop
        for a0 in tqdmnd(
            num_iter,
            desc="Reconstructing object and probe",
            unit=" iter",
            disable=not progress_bar,
        ):
            error = 0.0

            if collective_measurement_updates:
                collective_object = xp.zeros_like(self._object)

            # randomize
            measurement_indices = np.arange(self._num_measurements)
            np.random.shuffle(measurement_indices)

            for measurement_index in measurement_indices:
                self._active_measurement_index = measurement_index

                measurement_error = 0.0

                _probe = self._probes_all[self._active_measurement_index]
                _probe_initial_aperture = self._probes_all_initial_aperture[
                    self._active_measurement_index
                ]

                start_idx = self._cum_probes_per_measurement[
                    self._active_measurement_index
                ]
                end_idx = self._cum_probes_per_measurement[
                    self._active_measurement_index + 1
                ]

                num_diffraction_patterns = end_idx - start_idx
                shuffled_indices = np.arange(start_idx, end_idx)

                # randomize
                if not use_projection_scheme:
                    np.random.shuffle(shuffled_indices)

                for start, end in generate_batches(
                    num_diffraction_patterns, max_batch=max_batch_size
                ):
                    # batch indices
                    batch_indices = shuffled_indices[start:end]
                    positions_px = self._positions_px_all[batch_indices]
                    positions_px_initial = self._positions_px_initial_all[batch_indices]
                    positions_px_fractional = positions_px - xp_storage.round(
                        positions_px
                    )

                    (
                        vectorized_patch_indices_row,
                        vectorized_patch_indices_col,
                    ) = self._extract_vectorized_patch_indices(positions_px)

                    amplitudes_device = copy_to_device(
                        self._amplitudes[batch_indices], device
                    )

                    # forward operator
                    (
                        shifted_probes,
                        object_patches,
                        overlap,
                        self._exit_waves,
                        batch_error,
                    ) = self._forward(
                        self._object,
                        vectorized_patch_indices_row,
                        vectorized_patch_indices_col,
                        _probe,
                        positions_px_fractional,
                        amplitudes_device,
                        self._exit_waves,
                        detector_fourier_mask,
                        virtual_detector_masks,
                        use_projection_scheme=use_projection_scheme,
                        projection_a=projection_a,
                        projection_b=projection_b,
                        projection_c=projection_c,
                    )

                    # adjoint operator
                    object_update, _probe = self._adjoint(
                        self._object.copy(),
                        _probe,
                        object_patches,
                        shifted_probes,
                        positions_px,
                        self._exit_waves,
                        use_projection_scheme=use_projection_scheme,
                        step_size=step_size,
                        normalization_min=normalization_min,
                        fix_probe=fix_probe,
                    )

                    object_update -= self._object

                    # position correction
                    if not fix_positions and a0 > 0:
                        self._positions_px_all[batch_indices] = (
                            self._position_correction(
                                self._object,
                                vectorized_patch_indices_row,
                                vectorized_patch_indices_col,
                                shifted_probes,
                                overlap,
                                amplitudes_device,
                                positions_px,
                                positions_px_initial,
                                positions_step_size,
                                max_position_update_distance,
                                max_position_total_distance,
                            )
                        )

                    measurement_error += batch_error

                if collective_measurement_updates:
                    collective_object += object_update
                else:
                    self._object += object_update

                # Normalize Error
                measurement_error /= (
                    self._mean_diffraction_intensity[self._active_measurement_index]
                    * num_diffraction_patterns
                )
                error += measurement_error

                # constraints

                if collective_measurement_updates:
                    # probe and positions
                    _probe = self._probe_constraints(
                        _probe,
                        fix_probe_com=fix_probe_com and not fix_probe,
                        constrain_probe_amplitude=constrain_probe_amplitude
                        and not fix_probe,
                        constrain_probe_amplitude_relative_radius=constrain_probe_amplitude_relative_radius,
                        constrain_probe_amplitude_relative_width=constrain_probe_amplitude_relative_width,
                        constrain_probe_fourier_amplitude=constrain_probe_fourier_amplitude
                        and not fix_probe,
                        constrain_probe_fourier_amplitude_max_width_pixels=constrain_probe_fourier_amplitude_max_width_pixels,
                        constrain_probe_fourier_amplitude_constant_intensity=constrain_probe_fourier_amplitude_constant_intensity,
                        fit_probe_aberrations=fit_probe_aberrations and not fix_probe,
                        fit_probe_aberrations_max_angular_order=fit_probe_aberrations_max_angular_order,
                        fit_probe_aberrations_max_radial_order=fit_probe_aberrations_max_radial_order,
                        fit_probe_aberrations_remove_initial=fit_probe_aberrations_remove_initial,
                        fit_probe_aberrations_using_scikit_image=fit_probe_aberrations_using_scikit_image,
                        fix_probe_aperture=fix_probe_aperture and not fix_probe,
                        initial_probe_aperture=_probe_initial_aperture,
                        probe_real_space_support_mask=probe_real_space_support_mask,
                    )

                    self._positions_px_all[batch_indices] = self._positions_constraints(
                        self._positions_px_all[batch_indices],
                        self._positions_px_initial_all[batch_indices],
                        fix_positions=fix_positions,
                        fix_positions_com=fix_positions_com and not fix_positions,
                        global_affine_transformation=global_affine_transformation,
                    )

                else:
                    # object, probe, and positions
                    (
                        self._object,
                        _probe,
                        self._positions_px_all[batch_indices],
                    ) = self._constraints(
                        self._object,
                        _probe,
                        self._positions_px_all[batch_indices],
                        self._positions_px_initial_all[batch_indices],
                        fix_probe_com=fix_probe_com and not fix_probe,
                        constrain_probe_amplitude=constrain_probe_amplitude
                        and not fix_probe,
                        constrain_probe_amplitude_relative_radius=constrain_probe_amplitude_relative_radius,
                        constrain_probe_amplitude_relative_width=constrain_probe_amplitude_relative_width,
                        constrain_probe_fourier_amplitude=constrain_probe_fourier_amplitude
                        and not fix_probe,
                        constrain_probe_fourier_amplitude_max_width_pixels=constrain_probe_fourier_amplitude_max_width_pixels,
                        constrain_probe_fourier_amplitude_constant_intensity=constrain_probe_fourier_amplitude_constant_intensity,
                        fit_probe_aberrations=fit_probe_aberrations and not fix_probe,
                        fit_probe_aberrations_max_angular_order=fit_probe_aberrations_max_angular_order,
                        fit_probe_aberrations_max_radial_order=fit_probe_aberrations_max_radial_order,
                        fit_probe_aberrations_remove_initial=fit_probe_aberrations_remove_initial,
                        fit_probe_aberrations_using_scikit_image=fit_probe_aberrations_using_scikit_image,
                        fix_probe_aperture=fix_probe_aperture and not fix_probe,
                        initial_probe_aperture=_probe_initial_aperture,
                        probe_real_space_support_mask=probe_real_space_support_mask,
                        fix_positions=fix_positions,
                        fix_positions_com=fix_positions_com and not fix_positions,
                        global_affine_transformation=global_affine_transformation,
                        gaussian_filter=gaussian_filter
                        and gaussian_filter_sigma_m is not None,
                        gaussian_filter_sigma_e=gaussian_filter_sigma_e,
                        gaussian_filter_sigma_m=gaussian_filter_sigma_m,
                        butterworth_filter=butterworth_filter
                        and (q_lowpass_m is not None or q_highpass_m is not None),
                        q_lowpass_e=q_lowpass_e,
                        q_lowpass_m=q_lowpass_m,
                        q_highpass_e=q_highpass_e,
                        q_highpass_m=q_highpass_m,
                        butterworth_order=butterworth_order,
                        tv_denoise=tv_denoise and tv_denoise_weight is not None,
                        tv_denoise_weight=tv_denoise_weight,
                        tv_denoise_inner_iter=tv_denoise_inner_iter,
                    )

            # Normalize Error Over Tilts
            error /= self._num_measurements

            if collective_measurement_updates:
                self._object += collective_object / self._num_measurements

                # object only
                self._object = self._object_constraints(
                    self._object,
                    gaussian_filter=gaussian_filter
                    and gaussian_filter_sigma_m is not None,
                    gaussian_filter_sigma_e=gaussian_filter_sigma_e,
                    gaussian_filter_sigma_m=gaussian_filter_sigma_m,
                    butterworth_filter=butterworth_filter
                    and (q_lowpass_m is not None or q_highpass_m is not None),
                    q_lowpass_e=q_lowpass_e,
                    q_lowpass_m=q_lowpass_m,
                    q_highpass_e=q_highpass_e,
                    q_highpass_m=q_highpass_m,
                    butterworth_order=butterworth_order,
                    tv_denoise=tv_denoise and tv_denoise_weight is not None,
                    tv_denoise_weight=tv_denoise_weight,
                    tv_denoise_inner_iter=tv_denoise_inner_iter,
                )

            self.error_iterations.append(error.item())

            if store_iterations:
                self.object_iterations.append(asnumpy(self._object.copy()))
                self.probe_iterations.append(self.probe_centered)

        # store result
        self.object = asnumpy(self._object)
        self.probe = self.probe_centered
        self.error = error.item()

        # remove _exit_waves attr from self for GD
        if not use_projection_scheme:
            self._exit_waves = None

        self.clear_device_mem(self._device, self._clear_fft_cache)

        return self

    def _visualize_all_iterations(self, **kwargs):
        raise NotImplementedError()

    def _visualize_last_iteration(
        self,
        fig,
        cbar: bool,
        plot_convergence: bool,
        plot_probe: bool,
        plot_fourier_probe: bool,
        remove_initial_probe_aberrations: bool,
        **kwargs,
    ):
        """
        Displays last reconstructed object and probe iterations.

        Parameters
        --------
        fig: Figure
            Matplotlib figure to place Gridspec in
        plot_convergence: bool, optional
            If true, the normalized mean squared error (NMSE) plot is displayed
        cbar: bool, optional
            If true, displays a colorbar
        plot_probe: bool, optional
            If true, the reconstructed complex probe is displayed
        remove_initial_probe_aberrations: bool, optional
            If true, when plotting fourier probe, removes initial probe
            to visualize changes
        """

        asnumpy = self._asnumpy

        figsize = kwargs.pop("figsize", (12, 8))
        cmap_e_real = kwargs.pop("cmap_e_real", "cividis")
        cmap_e_imag = kwargs.pop("cmap_e_imag", "magma")
        cmap_m_real = kwargs.pop("cmap_m_real", "PuOr")
        cmap_m_imag = kwargs.pop("cmap_m_imag", "PiYG")
        chroma_boost = kwargs.pop("chroma_boost", 1)

        # get scaled arrays
        obj = self.object_cropped

        vmin_e_real = kwargs.pop("vmin_e_real", None)
        vmax_e_real = kwargs.pop("vmax_e_real", None)
        vmin_e_imag = kwargs.pop("vmin_e_imag", None)
        vmax_e_imag = kwargs.pop("vmax_e_imag", None)
        _, vmin_e_real, vmax_e_real = return_scaled_histogram_ordering(
            obj[0].real, vmin_e_real, vmax_e_real
        )
        _, vmin_e_imag, vmax_e_iamg = return_scaled_histogram_ordering(
            obj[0].imag, vmin_e_imag, vmax_e_imag
        )

        _, _, _vmax_m_real = return_scaled_histogram_ordering(obj[1].real)
        vmin_m_real = kwargs.pop("vmin_m_real", -_vmax_m_real)
        vmax_m_real = kwargs.pop("vmax_m_real", _vmax_m_real)

        _, _, _vmax_m_imag = return_scaled_histogram_ordering(obj[1].imag)
        vmin_m_imag = kwargs.pop("vmin_m_imag", -_vmax_m_imag)
        vmax_m_imag = kwargs.pop("vmax_m_imag", _vmax_m_imag)

        extent = [
            0,
            self.sampling[1] * obj.shape[2],
            self.sampling[0] * obj.shape[1],
            0,
        ]

        if plot_fourier_probe:
            probe_extent = [
                -self.angular_sampling[1] * self._region_of_interest_shape[1] / 2,
                self.angular_sampling[1] * self._region_of_interest_shape[1] / 2,
                self.angular_sampling[0] * self._region_of_interest_shape[0] / 2,
                -self.angular_sampling[0] * self._region_of_interest_shape[0] / 2,
            ]
        elif plot_probe:
            probe_extent = [
                0,
                self.sampling[1] * self._region_of_interest_shape[1],
                self.sampling[0] * self._region_of_interest_shape[0],
                0,
            ]

        if plot_convergence:
            if plot_probe:
                spec = GridSpec(
                    ncols=3,
                    nrows=3,
                    height_ratios=[4, 4, 1],
                    hspace=0.15,
                    width_ratios=[
                        (extent[1] / extent[2]) / (probe_extent[1] / probe_extent[2]),
                        (extent[1] / extent[2]) / (probe_extent[1] / probe_extent[2]),
                        1,
                    ],
                    wspace=0.35,
                )

            else:
                spec = GridSpec(ncols=2, nrows=3, height_ratios=[4, 4, 1], hspace=0.15)

        else:
            if plot_probe:
                spec = GridSpec(
                    ncols=3,
                    nrows=2,
                    width_ratios=[
                        (extent[1] / extent[2]) / (probe_extent[1] / probe_extent[2]),
                        (extent[1] / extent[2]) / (probe_extent[1] / probe_extent[2]),
                        1,
                    ],
                    wspace=0.35,
                )

            else:
                spec = GridSpec(ncols=2, nrows=2, wspace=0.35)

        if fig is None:
            fig = plt.figure(figsize=figsize)

        # Electronic real
        ax = fig.add_subplot(spec[0, 0])
        im = ax.imshow(
            obj[0].real,
            extent=extent,
            cmap=cmap_e_real,
            vmin=vmin_e_real,
            vmax=vmax_e_real,
            **kwargs,
        )
        ax.set_ylabel("x [A]")
        ax.set_xlabel("y [A]")
        ax.set_title("Real elec. optical index")

        if cbar:
            divider = make_axes_locatable(ax)
            ax_cb = divider.append_axes("right", size="5%", pad="2.5%")
            fig.add_axes(ax_cb)
            fig.colorbar(im, cax=ax_cb)

        # Electronic imag
        ax = fig.add_subplot(spec[0, 1])
        im = ax.imshow(
            obj[0].imag,
            extent=extent,
            cmap=cmap_e_imag,
            vmin=vmin_e_imag,
            vmax=vmax_e_imag,
            **kwargs,
        )
        ax.set_ylabel("x [A]")
        ax.set_xlabel("y [A]")
        ax.set_title("Imag elec. optical index")

        if cbar:
            divider = make_axes_locatable(ax)
            ax_cb = divider.append_axes("right", size="5%", pad="2.5%")
            fig.add_axes(ax_cb)
            fig.colorbar(im, cax=ax_cb)

        # Magnetic real
        ax = fig.add_subplot(spec[1, 0])
        im = ax.imshow(
            obj[1].real,
            extent=extent,
            cmap=cmap_m_real,
            vmin=vmin_m_real,
            vmax=vmax_m_real,
            **kwargs,
        )
        ax.set_ylabel("x [A]")
        ax.set_xlabel("y [A]")
        ax.set_title("Real mag. optical index")

        if cbar:
            divider = make_axes_locatable(ax)
            ax_cb = divider.append_axes("right", size="5%", pad="2.5%")
            fig.add_axes(ax_cb)
            fig.colorbar(im, cax=ax_cb)

        # Magnetic imag
        ax = fig.add_subplot(spec[1, 1])
        im = ax.imshow(
            obj[1].imag,
            extent=extent,
            cmap=cmap_m_imag,
            vmin=vmin_m_imag,
            vmax=vmax_m_imag,
            **kwargs,
        )
        ax.set_ylabel("x [A]")
        ax.set_xlabel("y [A]")
        ax.set_title("Imag mag. optical index")

        if cbar:
            divider = make_axes_locatable(ax)
            ax_cb = divider.append_axes("right", size="5%", pad="2.5%")
            fig.add_axes(ax_cb)
            fig.colorbar(im, cax=ax_cb)

        if plot_fourier_probe:
            # Fourier probe
            intensities = self._return_probe_intensities(None)
            titles = [
                f"{sign}ve Fourier probe: {ratio*100:.1f}%"
                for sign, ratio in zip(self._magnetic_contribution_sign, intensities)
            ]
            ax = fig.add_subplot(spec[0, 2])

            probe_fourier = asnumpy(
                self._return_fourier_probe(
                    self._probes_all[0],
                    remove_initial_probe_aberrations=remove_initial_probe_aberrations,
                )
            )

            probe_array = Complex2RGB(
                probe_fourier,
                chroma_boost=chroma_boost,
            )

            ax.set_title(titles[0])
            ax.set_ylabel("kx [mrad]")
            ax.set_xlabel("ky [mrad]")

            im = ax.imshow(
                probe_array,
                extent=probe_extent,
            )

            if cbar:
                divider = make_axes_locatable(ax)
                ax_cb = divider.append_axes("right", size="5%", pad="2.5%")
                add_colorbar_arg(ax_cb, chroma_boost=chroma_boost)

            ax = fig.add_subplot(spec[1, 2])

            probe_fourier = asnumpy(
                self._return_fourier_probe(
                    self._probes_all[-1],
                    remove_initial_probe_aberrations=remove_initial_probe_aberrations,
                )
            )

            probe_array = Complex2RGB(
                probe_fourier,
                chroma_boost=chroma_boost,
            )

            ax.set_title(titles[-1])
            ax.set_ylabel("kx [mrad]")
            ax.set_xlabel("ky [mrad]")

            im = ax.imshow(
                probe_array,
                extent=probe_extent,
            )

            if cbar:
                divider = make_axes_locatable(ax)
                ax_cb = divider.append_axes("right", size="5%", pad="2.5%")
                add_colorbar_arg(ax_cb, chroma_boost=chroma_boost)

        elif plot_probe:
            # Real probe
            intensities = self._return_probe_intensities(None)
            titles = [
                f"{sign}ve probe intensity: {ratio*100:.1f}%"
                for sign, ratio in zip(self._magnetic_contribution_sign, intensities)
            ]
            ax = fig.add_subplot(spec[0, 2])

            probe_array = Complex2RGB(
                asnumpy(self._return_centered_probe(self._probes_all[0])),
                power=2,
                chroma_boost=chroma_boost,
            )
            ax.set_title(titles[0])
            ax.set_ylabel("x [A]")
            ax.set_xlabel("y [A]")

            im = ax.imshow(
                probe_array,
                extent=probe_extent,
            )

            if cbar:
                divider = make_axes_locatable(ax)
                ax_cb = divider.append_axes("right", size="5%", pad="2.5%")
                add_colorbar_arg(ax_cb, chroma_boost=chroma_boost)

            ax = fig.add_subplot(spec[1, 2])

            probe_array = Complex2RGB(
                asnumpy(self._return_centered_probe(self._probes_all[-1])),
                power=2,
                chroma_boost=chroma_boost,
            )
            ax.set_title(titles[-1])
            ax.set_ylabel("x [A]")
            ax.set_xlabel("y [A]")

            im = ax.imshow(
                probe_array,
                extent=probe_extent,
            )

            if cbar:
                divider = make_axes_locatable(ax)
                ax_cb = divider.append_axes("right", size="5%", pad="2.5%")
                add_colorbar_arg(ax_cb, chroma_boost=chroma_boost)

        if plot_convergence and hasattr(self, "error_iterations"):
            errors = np.array(self.error_iterations)

            ax = fig.add_subplot(spec[2, :])
            ax.semilogy(np.arange(errors.shape[0]), errors, **kwargs)
            ax.set_ylabel("NMSE")
            ax.set_xlabel("Iteration number")
            ax.yaxis.tick_right()

        fig.suptitle(f"Normalized mean squared error: {self.error:.3e}")
        spec.tight_layout(fig)

    @property
    def object_cropped(self):
        """Cropped and rotated object"""
        avg_pos = self._return_average_positions()
        cropped_e = self._crop_rotate_object_fov(self._object[0], positions_px=avg_pos)
        cropped_m = self._crop_rotate_object_fov(self._object[1], positions_px=avg_pos)

        return np.array([cropped_e, cropped_m])
