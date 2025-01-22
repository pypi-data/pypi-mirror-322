import functools
import itertools
from collections import defaultdict
from typing import Mapping, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import dctn, idctn
from scipy.ndimage import gaussian_filter, uniform_filter1d, zoom
from scipy.optimize import curve_fit
from scipy.spatial.transform import Rotation

try:
    import cupy as cp
    from cupyx.scipy.ndimage import zoom as zoom_cp

    get_array_module = cp.get_array_module
except (ImportError, ModuleNotFoundError):
    cp = None

    def get_array_module(*args):
        return np


from py4DSTEM.process.utils import get_CoM, get_shifted_ar
from py4DSTEM.process.utils.cross_correlate import align_and_shift_images
from py4DSTEM.process.utils.utils import electron_wavelength_angstrom

# fmt: off

#: Symbols for the polar representation of all optical aberrations up to the fifth order.
polar_symbols = (
        "C10", "C12", "phi12",
        "C21", "phi21", "C23", "phi23",
        "C30", "C32", "phi32", "C34", "phi34",
        "C41", "phi41", "C43", "phi43", "C45", "phi45",
        "C50", "C52", "phi52", "C54", "phi54", "C56", "phi56",
)

#: Aliases for the most commonly used optical aberrations.
polar_aliases = {
        "defocus": "C10", "astigmatism": "C12", "astigmatism_angle": "phi12",
        "coma": "C21", "coma_angle": "phi21",
        "Cs": "C30",
        "C5": "C50",
}

# fmt: on

### Probe functions


class ComplexProbe:
    """
    Complex Probe Class.

    Simplified version of CTF and Probe from abTEM:
    https://github.com/abTEM/abTEM/blob/master/abtem/transfer.py
    https://github.com/abTEM/abTEM/blob/master/abtem/waves.py

    Parameters
    ----------
    energy: float
        The electron energy of the wave functions this contrast transfer function will be applied to [eV].
    semiangle_cutoff: float
        The semiangle cutoff describes the sharp Fourier space cutoff due to the objective aperture [mrad].
    gpts : Tuple[int,int]
        Number of grid points describing the wave functions.
    sampling : Tuple[float,float]
        Lateral sampling of wave functions in Å
    device: str, optional
        Device to perform calculations on. Must be either 'cpu' or 'gpu'
    rolloff: float, optional
        Tapers the cutoff edge over the given angular range [mrad].
    vacuum_probe_intensity: np.ndarray, optional
        Squared of corner-centered aperture amplitude to use, instead of semiangle_cutoff + rolloff
    force_spatial_frequencies: np.ndarray, optional
        Corner-centered spatial frequencies. Useful for creating shifted probes necessary in direct ptychography.
    focal_spread: float, optional
        The 1/e width of the focal spread due to chromatic aberration and lens current instability [Å].
    angular_spread: float, optional
        The 1/e width of the angular deviations due to source size [mrad].
    gaussian_spread: float, optional
        The 1/e width image deflections due to vibrations and thermal magnetic noise [Å].
    phase_shift : float, optional
        A constant phase shift [radians].
    parameters: dict, optional
        Mapping from aberration symbols to their corresponding values. All aberration magnitudes should be given in Å
        and angles should be given in radians.
    kwargs:
        Provide the aberration coefficients as keyword arguments.
    """

    def __init__(
        self,
        energy: float,
        gpts: Tuple[int, int],
        sampling: Tuple[float, float],
        semiangle_cutoff: float = np.inf,
        rolloff: float = 2.0,
        vacuum_probe_intensity: np.ndarray = None,
        force_spatial_frequencies: Tuple[np.ndarray, np.ndarray] = None,
        device: str = "cpu",
        focal_spread: float = 0.0,
        angular_spread: float = 0.0,
        gaussian_spread: float = 0.0,
        phase_shift: float = 0.0,
        parameters: Mapping[str, float] = None,
        **kwargs,
    ):
        if device == "cpu":
            self._xp = np
            self._asnumpy = np.asarray
        elif device == "gpu":
            self._xp = cp
            self._asnumpy = cp.asnumpy
        else:
            raise ValueError(f"device must be either 'cpu' or 'gpu', not {device}")

        for key in kwargs.keys():
            if (key not in polar_symbols) and (key not in polar_aliases.keys()):
                raise ValueError("{} not a recognized parameter".format(key))

        self._vacuum_probe_intensity = vacuum_probe_intensity
        self._force_spatial_frequencies = force_spatial_frequencies
        self._semiangle_cutoff = semiangle_cutoff
        self._rolloff = rolloff
        self._focal_spread = focal_spread
        self._angular_spread = angular_spread
        self._gaussian_spread = gaussian_spread
        self._phase_shift = phase_shift
        self._energy = energy
        self._wavelength = electron_wavelength_angstrom(energy)
        self._gpts = gpts
        self._sampling = sampling
        self._device = device

        self._parameters = dict(zip(polar_symbols, [0.0] * len(polar_symbols)))

        if parameters is None:
            parameters = {}

        parameters.update(kwargs)
        self.set_parameters(parameters)

    def set_parameters(self, parameters: dict):
        """
        Set the phase of the phase aberration.
        Parameters
        ----------
        parameters: dict
            Mapping from aberration symbols to their corresponding values.
        """

        for symbol, value in parameters.items():
            if symbol in self._parameters.keys():
                self._parameters[symbol] = value

            elif symbol == "defocus":
                self._parameters[polar_aliases[symbol]] = -value

            elif symbol in polar_aliases.keys():
                self._parameters[polar_aliases[symbol]] = value

            else:
                raise ValueError("{} not a recognized parameter".format(symbol))

        return parameters

    def evaluate_aperture(
        self, alpha: Union[float, np.ndarray], phi: Union[float, np.ndarray] = None
    ) -> Union[float, np.ndarray]:
        xp = self._xp
        semiangle_cutoff = self._semiangle_cutoff / 1000

        if self._vacuum_probe_intensity is not None:
            if self._force_spatial_frequencies is not None:
                vacuum_probe_intensity = get_shifted_ar(
                    xp.asarray(self._vacuum_probe_intensity, dtype=xp.float32),
                    self._origin[0],
                    self._origin[1],
                    bilinear=True,
                    device=self._device,
                )
            else:
                vacuum_probe_intensity = xp.asarray(
                    self._vacuum_probe_intensity, dtype=xp.float32
                )
            vacuum_probe_amplitude = xp.sqrt(xp.maximum(vacuum_probe_intensity, 0))
            return vacuum_probe_amplitude

        if self._semiangle_cutoff == xp.inf:
            return xp.ones_like(alpha)

        if self._rolloff > 0.0:
            rolloff = self._rolloff / 1000.0  # * semiangle_cutoff
            array = 0.5 * (
                1 + xp.cos(np.pi * (alpha - semiangle_cutoff + rolloff) / rolloff)
            )
            array[alpha > semiangle_cutoff] = 0.0
            array = xp.where(
                alpha > semiangle_cutoff - rolloff,
                array,
                xp.ones_like(alpha, dtype=xp.float32),
            )
        else:
            array = xp.array(alpha < semiangle_cutoff).astype(xp.float32)
        return array

    def evaluate_temporal_envelope(
        self, alpha: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        xp = self._xp
        return xp.exp(
            -((0.5 * xp.pi / self._wavelength * self._focal_spread * alpha**2) ** 2)
        ).astype(xp.float32)

    def evaluate_gaussian_envelope(
        self, alpha: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        xp = self._xp
        return xp.exp(-0.5 * self._gaussian_spread**2 * alpha**2 / self._wavelength**2)

    def evaluate_spatial_envelope(
        self, alpha: Union[float, np.ndarray], phi: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        xp = self._xp
        p = self._parameters
        dchi_dk = (
            2
            * xp.pi
            / self._wavelength
            * (
                (p["C12"] * xp.cos(2.0 * (phi - p["phi12"])) + p["C10"]) * alpha
                + (
                    p["C23"] * xp.cos(3.0 * (phi - p["phi23"]))
                    + p["C21"] * xp.cos(1.0 * (phi - p["phi21"]))
                )
                * alpha**2
                + (
                    p["C34"] * xp.cos(4.0 * (phi - p["phi34"]))
                    + p["C32"] * xp.cos(2.0 * (phi - p["phi32"]))
                    + p["C30"]
                )
                * alpha**3
                + (
                    p["C45"] * xp.cos(5.0 * (phi - p["phi45"]))
                    + p["C43"] * xp.cos(3.0 * (phi - p["phi43"]))
                    + p["C41"] * xp.cos(1.0 * (phi - p["phi41"]))
                )
                * alpha**4
                + (
                    p["C56"] * xp.cos(6.0 * (phi - p["phi56"]))
                    + p["C54"] * xp.cos(4.0 * (phi - p["phi54"]))
                    + p["C52"] * xp.cos(2.0 * (phi - p["phi52"]))
                    + p["C50"]
                )
                * alpha**5
            )
        )

        dchi_dphi = (
            -2
            * xp.pi
            / self._wavelength
            * (
                1 / 2.0 * (2.0 * p["C12"] * xp.sin(2.0 * (phi - p["phi12"]))) * alpha
                + 1
                / 3.0
                * (
                    3.0 * p["C23"] * xp.sin(3.0 * (phi - p["phi23"]))
                    + 1.0 * p["C21"] * xp.sin(1.0 * (phi - p["phi21"]))
                )
                * alpha**2
                + 1
                / 4.0
                * (
                    4.0 * p["C34"] * xp.sin(4.0 * (phi - p["phi34"]))
                    + 2.0 * p["C32"] * xp.sin(2.0 * (phi - p["phi32"]))
                )
                * alpha**3
                + 1
                / 5.0
                * (
                    5.0 * p["C45"] * xp.sin(5.0 * (phi - p["phi45"]))
                    + 3.0 * p["C43"] * xp.sin(3.0 * (phi - p["phi43"]))
                    + 1.0 * p["C41"] * xp.sin(1.0 * (phi - p["phi41"]))
                )
                * alpha**4
                + 1
                / 6.0
                * (
                    6.0 * p["C56"] * xp.sin(6.0 * (phi - p["phi56"]))
                    + 4.0 * p["C54"] * xp.sin(4.0 * (phi - p["phi54"]))
                    + 2.0 * p["C52"] * xp.sin(2.0 * (phi - p["phi52"]))
                )
                * alpha**5
            )
        )

        return xp.exp(
            -xp.sign(self._angular_spread)
            * (self._angular_spread / 2 / 1000) ** 2
            * (dchi_dk**2 + dchi_dphi**2)
        )

    def evaluate_chi(
        self, alpha: Union[float, np.ndarray], phi: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        xp = self._xp
        p = self._parameters

        alpha2 = alpha**2
        alpha = xp.array(alpha)

        array = xp.zeros(alpha.shape, dtype=np.float32)
        if any([p[symbol] != 0.0 for symbol in ("C10", "C12", "phi12")]):
            array += (
                1 / 2 * alpha2 * (p["C10"] + p["C12"] * xp.cos(2 * (phi - p["phi12"])))
            )

        if any([p[symbol] != 0.0 for symbol in ("C21", "phi21", "C23", "phi23")]):
            array += (
                1
                / 3
                * alpha2
                * alpha
                * (
                    p["C21"] * xp.cos(phi - p["phi21"])
                    + p["C23"] * xp.cos(3 * (phi - p["phi23"]))
                )
            )

        if any(
            [p[symbol] != 0.0 for symbol in ("C30", "C32", "phi32", "C34", "phi34")]
        ):
            array += (
                1
                / 4
                * alpha2**2
                * (
                    p["C30"]
                    + p["C32"] * xp.cos(2 * (phi - p["phi32"]))
                    + p["C34"] * xp.cos(4 * (phi - p["phi34"]))
                )
            )

        if any(
            [
                p[symbol] != 0.0
                for symbol in ("C41", "phi41", "C43", "phi43", "C45", "phi41")
            ]
        ):
            array += (
                1
                / 5
                * alpha2**2
                * alpha
                * (
                    p["C41"] * xp.cos((phi - p["phi41"]))
                    + p["C43"] * xp.cos(3 * (phi - p["phi43"]))
                    + p["C45"] * xp.cos(5 * (phi - p["phi45"]))
                )
            )

        if any(
            [
                p[symbol] != 0.0
                for symbol in ("C50", "C52", "phi52", "C54", "phi54", "C56", "phi56")
            ]
        ):
            array += (
                1
                / 6
                * alpha2**3
                * (
                    p["C50"]
                    + p["C52"] * xp.cos(2 * (phi - p["phi52"]))
                    + p["C54"] * xp.cos(4 * (phi - p["phi54"]))
                    + p["C56"] * xp.cos(6 * (phi - p["phi56"]))
                )
            )

        array = 2 * xp.pi / self._wavelength * array + self._phase_shift
        return array

    def evaluate_aberrations(
        self, alpha: Union[float, np.ndarray], phi: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        xp = self._xp
        return xp.exp(-1.0j * self.evaluate_chi(alpha, phi))

    def evaluate(
        self, alpha: Union[float, np.ndarray], phi: Union[float, np.ndarray]
    ) -> Union[float, np.ndarray]:
        array = self.evaluate_aberrations(alpha, phi)

        if self._semiangle_cutoff < np.inf or self._vacuum_probe_intensity is not None:
            array *= self.evaluate_aperture(alpha, phi)

        if self._focal_spread > 0.0:
            array *= self.evaluate_temporal_envelope(alpha)

        if self._angular_spread > 0.0:
            array *= self.evaluate_spatial_envelope(alpha, phi)

        if self._gaussian_spread > 0.0:
            array *= self.evaluate_gaussian_envelope(alpha)

        return array

    def _evaluate_ctf(self):
        alpha, phi = self.get_scattering_angles()

        array = self.evaluate(alpha, phi)
        return array

    def get_scattering_angles(self):
        kx, ky = self.get_spatial_frequencies()
        alpha, phi = self.polar_coordinates(
            kx * self._wavelength, ky * self._wavelength
        )
        return alpha, phi

    def get_spatial_frequencies(self):
        xp = self._xp
        if self._force_spatial_frequencies is None:
            kx, ky = spatial_frequencies(self._gpts, self._sampling, xp)
        else:
            kx, ky = self._force_spatial_frequencies
            kx = xp.asarray(kx).astype(xp.float32)
            ky = xp.asarray(ky).astype(xp.float32)

            def find_zero_crossing(x):
                n = x.shape[0]
                y0, y1 = np.argsort(np.abs(x))[:2]
                x0, x1 = x[y0], x[y1]
                y = (y0 * x1 - y1 * x0) / (x1 - x0)
                dy = np.mod(y + n / 2, n) - n / 2
                return dy

            self._origin = tuple(find_zero_crossing(k) for k in [kx, ky])

        return kx, ky

    def polar_coordinates(self, x, y):
        """Calculate a polar grid for a given Cartesian grid."""
        xp = self._xp
        alpha = xp.sqrt(x[:, None] ** 2 + y[None, :] ** 2)
        phi = xp.arctan2(y[None, :], x[:, None])
        return alpha, phi

    def build(self):
        """Builds corner-centered complex probe in the center of the region of interest."""
        xp = self._xp
        array = xp.fft.ifft2(self._evaluate_ctf())
        array = array / xp.sqrt((xp.abs(array) ** 2).sum())
        self._array = array
        return self

    def visualize(self, **kwargs):
        """Plots the probe intensity."""
        xp = self._xp
        asnumpy = self._asnumpy

        cmap = kwargs.get("cmap", "Greys_r")
        kwargs.pop("cmap", None)

        plt.imshow(
            asnumpy(xp.abs(xp.fft.ifftshift(self._array)) ** 2),
            cmap=cmap,
            **kwargs,
        )
        return self


def spatial_frequencies(gpts: Tuple[int, int], sampling: Tuple[float, float], xp=np):
    """
    Calculate spatial frequencies of a grid.

    Parameters
    ----------
    gpts: tuple of int
        Number of grid points.
    sampling: tuple of float
        Sampling of the potential [1 / Å].

    Returns
    -------
    tuple of arrays
    """

    return tuple(
        xp.fft.fftfreq(n, d).astype(xp.float32) for n, d in zip(gpts, sampling)
    )


### FFT-shift functions


def fourier_translation_operator(
    positions: np.ndarray, shape: tuple, xp=np
) -> np.ndarray:
    """
    Create an array representing one or more phase ramp(s) for shifting another array.

    Parameters
    ----------
    positions : array of xy-positions
        Positions to calculate fourier translation operators for
    shape : two int
        Array dimensions to be fourier-shifted
    xp: Callable
        Array computing module

    Returns
    -------
    Fourier translation operators
    """

    positions_shape = positions.shape

    if len(positions_shape) == 1:
        positions = positions[None]

    kx, ky = spatial_frequencies(shape, (1.0, 1.0), xp=xp)
    positions = xp.asarray(positions, dtype=xp.float32)
    x = positions[:, 0].ravel()[:, None, None]
    y = positions[:, 1].ravel()[:, None, None]

    result = xp.exp(-2.0j * np.pi * kx[None, :, None] * x) * xp.exp(
        -2.0j * np.pi * ky[None, None, :] * y
    )

    if len(positions_shape) == 1:
        return result[0]
    else:
        return result


def fft_shift(array, positions, xp=np):
    """
    Fourier-shift array using positions.

    Parameters
    ----------
    array: np.ndarray
        Array to be shifted
    positions: array of xy-positions
        Positions to fourier-shift array with
    xp: Callable
        Array computing module

    Returns
    -------
        Fourier-shifted array
    """
    translation_operator = fourier_translation_operator(positions, array.shape[-2:], xp)
    fourier_array = xp.fft.fft2(array)

    if len(translation_operator.shape) == 3 and len(fourier_array.shape) == 3:
        shifted_fourier_array = fourier_array[None] * translation_operator[:, None]
    else:
        shifted_fourier_array = fourier_array * translation_operator

    return xp.fft.ifft2(shifted_fourier_array)


### Batching functions


def subdivide_into_batches(
    num_items: int, num_batches: int = None, max_batch: int = None
):
    """
    Split an n integer into m (almost) equal integers, such that the sum of smaller integers equals n.

    Parameters
    ----------
    n: int
        The integer to split.
    m: int
        The number integers n will be split into.

    Returns
    -------
    list of int
    """
    if (num_batches is not None) & (max_batch is not None):
        raise RuntimeError()

    if num_batches is None:
        if max_batch is not None:
            num_batches = (num_items + (-num_items % max_batch)) // max_batch
        else:
            raise RuntimeError()

    if num_items < num_batches:
        raise RuntimeError("num_batches may not be larger than num_items")

    elif num_items % num_batches == 0:
        return [num_items // num_batches] * num_batches
    else:
        v = []
        zp = num_batches - (num_items % num_batches)
        pp = num_items // num_batches
        for i in range(num_batches):
            if i >= zp:
                v = [pp + 1] + v
            else:
                v = [pp] + v
        return v


def generate_batches(
    num_items: int, num_batches: int = None, max_batch: int = None, start=0
):
    for batch in subdivide_into_batches(num_items, num_batches, max_batch):
        end = start + batch
        yield start, end

        start = end


#### Affine transformation functions


class AffineTransform:
    """
    Affine Transform Class.

    Simplified version of AffineTransform from tike:
    https://github.com/AdvancedPhotonSource/tike/blob/f9004a32fda5e49fa63b987e9ffe3c8447d59950/src/tike/ptycho/position.py

    AffineTransform() -> Identity

    Parameters
    ----------
    scale0: float
        x-scaling
    scale1: float
        y-scaling
    shear1: float
        \\gamma shear
    angle: float
        \\theta rotation angle
    t0: float
        x-translation
    t1: float
        y-translation
    dilation: float
        Isotropic expansion (multiplies scale0 and scale1)
    """

    def __init__(
        self,
        scale0: float = 1.0,
        scale1: float = 1.0,
        shear1: float = 0.0,
        angle: float = 0.0,
        t0: float = 0.0,
        t1: float = 0.0,
        dilation: float = 1.0,
    ):
        self.scale0 = scale0 * dilation
        self.scale1 = scale1 * dilation
        self.shear1 = shear1
        self.angle = angle
        self.t0 = t0
        self.t1 = t1

    @classmethod
    def fromarray(self, T: np.ndarray):
        """
        Return an Affine Transfrom from a 2x2 matrix.
        Use decomposition method from Graphics Gems 2 Section 7.1
        """
        R = T[:2, :2].copy()
        scale0 = np.linalg.norm(R[0])
        if scale0 <= 0:
            return AffineTransform()
        R[0] /= scale0
        shear1 = R[0] @ R[1]
        R[1] -= shear1 * R[0]
        scale1 = np.linalg.norm(R[1])
        if scale1 <= 0:
            return AffineTransform()
        R[1] /= scale1
        shear1 /= scale1
        angle = np.arccos(R[0, 0])

        if T.shape[0] > 2:
            t0, t1 = T[2]
        else:
            t0 = t1 = 0.0

        return AffineTransform(
            scale0=float(scale0),
            scale1=float(scale1),
            shear1=float(shear1),
            angle=float(angle),
            t0=t0,
            t1=t1,
        )

    def asarray(self):
        """
        Return an 2x2 matrix of scale, shear, rotation.
        This matrix is scale @ shear @ rotate from left to right.
        """
        cosx = np.cos(self.angle)
        sinx = np.sin(self.angle)
        return (
            np.array(
                [
                    [self.scale0, 0.0],
                    [0.0, self.scale1],
                ],
                dtype="float32",
            )
            @ np.array(
                [
                    [1.0, 0.0],
                    [self.shear1, 1.0],
                ],
                dtype="float32",
            )
            @ np.array(
                [
                    [+cosx, -sinx],
                    [+sinx, +cosx],
                ],
                dtype="float32",
            )
        )

    def asarray3(self):
        """
        Return an 3x2 matrix of scale, shear, rotation, translation.
        This matrix is scale @ shear @ rotate from left to right.
        Expects a homogenous (z) coordinate of 1.
        """
        T = np.empty((3, 2), dtype="float32")
        T[2] = (self.t0, self.t1)
        T[:2, :2] = self.asarray()
        return T

    def astuple(self):
        """Return the constructor parameters in a tuple."""
        return (
            self.scale0,
            self.scale1,
            self.shear1,
            self.angle,
            self.t0,
            self.t1,
        )

    def __call__(self, x: np.ndarray, origin=(0, 0), xp=np):
        origin = xp.asarray(origin, dtype=xp.float32)
        tf_matrix = self.asarray()
        tf_matrix = xp.asarray(tf_matrix, dtype=xp.float32)
        tf_translation = xp.array((self.t0, self.t1)) + origin
        return ((x - origin) @ tf_matrix) + tf_translation

    def __str__(self):
        return (
            "AffineTransform( \n"
            f"  scale0 = {self.scale0:.4f}, scale1 = {self.scale1:.4f}, \n"
            f"  shear1 = {self.shear1:.4f}, angle = {self.angle:.4f}, \n"
            f"  t0 = {self.t0:.4f}, t1 = {self.t1:.4f}, \n"
            ")"
        )


def estimate_global_transformation(
    positions0: np.ndarray,
    positions1: np.ndarray,
    origin: Tuple[int, int] = (0, 0),
    translation_allowed: bool = True,
    xp=np,
):
    """Use least squares to estimate the global affine transformation."""
    origin = xp.asarray(origin, dtype=xp.float32)

    try:
        if translation_allowed:
            a = xp.pad(positions0 - origin, ((0, 0), (0, 1)), constant_values=1)
        else:
            a = positions0 - origin

        b = positions1 - origin
        aT = a.conj().swapaxes(-1, -2)
        x = xp.linalg.inv(aT @ a) @ aT @ b

        tf = AffineTransform.fromarray(x)

    except xp.linalg.LinAlgError:
        tf = AffineTransform()

    error = xp.linalg.norm(tf(positions0, origin=origin, xp=xp) - positions1)

    return tf, error


def estimate_global_transformation_ransac(
    positions0: np.ndarray,
    positions1: np.ndarray,
    origin: Tuple[int, int] = (0, 0),
    translation_allowed: bool = True,
    min_sample: int = 64,
    max_error: float = 16,
    min_consensus: float = 0.75,
    max_iter: int = 20,
    xp=np,
):
    """Use RANSAC to estimate the global affine transformation."""
    best_fitness = np.inf  # small fitness is good
    transform = AffineTransform()

    # Choose a subset
    for subset in np.random.choice(
        a=len(positions0),
        size=(max_iter, min_sample),
        replace=True,
    ):
        # Fit to subset
        subset = np.unique(subset)
        candidate_model, _ = estimate_global_transformation(
            positions0=positions0[subset],
            positions1=positions1[subset],
            origin=origin,
            translation_allowed=translation_allowed,
            xp=xp,
        )

        # Determine inliars and outliars
        position_error = xp.linalg.norm(
            candidate_model(positions0, origin=origin, xp=xp) - positions1,
            axis=-1,
        )
        inliars = position_error <= max_error

        # Check if consensus reached
        if xp.sum(inliars) / len(inliars) >= min_consensus:
            # Refit with consensus inliars
            candidate_model, fitness = estimate_global_transformation(
                positions0=positions0[inliars],
                positions1=positions1[inliars],
                origin=origin,
                translation_allowed=translation_allowed,
                xp=xp,
            )
            if fitness < best_fitness:
                best_fitness = fitness
                transform = candidate_model

    return transform, best_fitness


def fourier_ring_correlation(
    image_1,
    image_2,
    pixel_size=None,
    bin_size=None,
    sigma=None,
    align_images=False,
    upsample_factor=8,
    device="cpu",
    plot_frc=True,
    frc_color="red",
    half_bit_color="blue",
):
    """
    Computes fourier ring correlation (FRC) of 2 arrays.
    Arrays must bet the same size.

    Parameters
     ----------
    image1: ndarray
        first image for FRC
    image2: ndarray
        second image for FRC
    pixel_size: tuple
        size of pixels in A (x,y)
    bin_size: float, optional
        size of bins for ring profile
    sigma: float, optional
        standard deviation for Gaussian kernel
    align_images: bool
        if True, aligns images using DFT upsampling of cross correlation.
    upsample factor: int
        if align_images, upsampling for correlation. Must be greater than 2.
    device: str, optional
        calculation device will be perfomed on. Must be 'cpu' or 'gpu'
    plot_frc: bool, optional
        if True, plots frc
    frc_color: str, optional
        color of FRC line in plot
    half_bit_color: str, optional
        color of half-bit line

    Returns
    --------
    q_frc: ndarray
        spatial frequencies of FRC
    frc: ndarray
        fourier ring correlation
    half_bit: ndarray
        half-bit criteria
    """
    if device == "cpu":
        xp = np
    elif device == "gpu":
        xp = cp

    if align_images:
        image_2 = align_and_shift_images(
            image_1,
            image_2,
            upsample_factor=upsample_factor,
            device=device,
        )

    fft_image_1 = xp.fft.fft2(image_1)
    fft_image_2 = xp.fft.fft2(image_2)

    cc_mixed = xp.real(fft_image_1 * xp.conj(fft_image_2))
    cc_image_1 = xp.abs(fft_image_1) ** 2
    cc_image_2 = xp.abs(fft_image_2) ** 2

    # take 1D profile
    q_frc, cc_mixed_1D, n = return_1D_profile(
        cc_mixed,
        pixel_size=pixel_size,
        sigma=sigma,
        bin_size=bin_size,
        device=device,
    )
    _, cc_image_1_1D, _ = return_1D_profile(
        cc_image_1, pixel_size=pixel_size, sigma=sigma, bin_size=bin_size, device=device
    )
    _, cc_image_2_1D, _ = return_1D_profile(
        cc_image_2,
        pixel_size=pixel_size,
        sigma=sigma,
        bin_size=bin_size,
        device=device,
    )

    frc = cc_mixed_1D / ((cc_image_1_1D * cc_image_2_1D) ** 0.5)
    half_bit = 2 / xp.sqrt(n / 2)

    ind_max = xp.argmax(n)
    q_frc = q_frc[1:ind_max]
    frc = frc[1:ind_max]
    half_bit = half_bit[1:ind_max]

    if plot_frc:
        fig, ax = plt.subplots()
        if device == "gpu":
            ax.plot(q_frc.get(), frc.get(), label="FRC", color=frc_color)
            ax.plot(q_frc.get(), half_bit.get(), label="half bit", color=half_bit_color)
            ax.set_xlim([0, q_frc.get().max()])
        else:
            ax.plot(q_frc, frc, label="FRC", color=frc_color)
            ax.plot(q_frc, half_bit, label="half bit", color=half_bit_color)
            ax.set_xlim([0, q_frc.max()])
        ax.legend()
        ax.set_ylim([0, 1])

        if pixel_size is None:
            ax.set_xlabel(r"Spatial frequency (pixels)")
        else:
            ax.set_xlabel(r"Spatial frequency ($\AA$)")
        ax.set_ylabel("FRC")

    return q_frc, frc, half_bit


def return_1D_profile(
    intensity, pixel_size=None, bin_size=None, sigma=None, device="cpu"
):
    """
    Return 1D radial profile from corner centered array

    Parameters
     ----------
    intensity: ndarray
        Array for computing 1D profile
    pixel_size: tuple
        Size of pixels in A (x,y)
    bin_size: float, optional
        Size of bins for ring profile
    sigma: float, optional
        standard deviation for Gaussian kernel
    device: str, optional
        calculation device will be perfomed on. Must be 'cpu' or 'gpu'

    Returns
    --------
    q_bins: ndarray
        spatial frequencies of bins
    I_bins: ndarray
        Intensity of bins
    n: ndarray
        Number of pixels in each bin
    """
    if device == "cpu":
        xp = np
    elif device == "gpu":
        xp = cp

    if pixel_size is None:
        pixel_size = (1, 1)

    x = xp.fft.fftfreq(intensity.shape[0], pixel_size[0]).astype(xp.float32)
    y = xp.fft.fftfreq(intensity.shape[1], pixel_size[1]).astype(xp.float32)
    q = xp.sqrt(x[:, None] ** 2 + y[None, :] ** 2)
    q = q.ravel()

    intensity = intensity.ravel()

    if bin_size is None:
        bin_size = q[1] - q[0]

    q_bins = xp.arange(0, q.max() + bin_size, bin_size)

    inds = q / bin_size
    inds_f = xp.floor(inds).astype("int")
    d_ind = inds - inds_f

    nf = xp.bincount(inds_f, weights=(1 - d_ind), minlength=q_bins.shape[0])
    nc = xp.bincount(inds_f + 1, weights=(d_ind), minlength=q_bins.shape[0])
    n = nf + nc

    I_bins0 = xp.bincount(
        inds_f, weights=intensity * (1 - d_ind), minlength=q_bins.shape[0]
    )
    I_bins1 = xp.bincount(
        inds_f + 1, weights=intensity * (d_ind), minlength=q_bins.shape[0]
    )

    I_bins = (I_bins0 + I_bins1) / n
    if sigma is not None:
        I_bins = gaussian_filter(I_bins, sigma)

    return q_bins, I_bins, n


def fourier_rotate_real_volume(array, angle, axes=(0, 1), xp=np):
    """
    Rotates a 3D array using three Fourier-based shear operators.

    Parameters
     ----------
    array: ndarray
        3D array to rotate
    angle: float
        Angle in deg to rotate array by
    axes: tuple, Optional
        Axes defining plane in which to rotate about
    xp: Callable, optional
        Array computing module

    Returns
    --------
    output_arr: ndarray
        Fourier-rotated array
    """
    input_arr = xp.asarray(array, dtype=array.dtype)
    array_shape = np.array(input_arr.shape)
    ndim = input_arr.ndim

    if ndim != 3:
        raise ValueError("input array should be 3D")

    axes = list(axes)

    if len(axes) != 2:
        raise ValueError("axes should contain exactly two values")

    if not all([float(ax).is_integer() for ax in axes]):
        raise ValueError("axes should contain only integer values")

    if axes[0] < 0:
        axes[0] += ndim
    if axes[1] < 0:
        axes[1] += ndim
    if axes[0] < 0 or axes[1] < 0 or axes[0] >= ndim or axes[1] >= ndim:
        raise ValueError("invalid rotation plane specified")

    axes.sort()
    rotation_ax = np.setdiff1d([0, 1, 2], axes)[0]
    plane_dims = array_shape[axes]

    qx = xp.fft.fftfreq(plane_dims[0], 1).astype(xp.float32)
    qy = xp.fft.fftfreq(plane_dims[1], 1).astype(xp.float32)
    qxa, qya = xp.meshgrid(qx, qy, indexing="ij")

    x = xp.arange(plane_dims[0]) - plane_dims[0] / 2
    y = xp.arange(plane_dims[1]) - plane_dims[1] / 2
    xa, ya = xp.meshgrid(x, y, indexing="ij")

    theta_90 = round(angle / 90)
    theta_rest = (angle + 45) % 90 - 45

    theta = np.deg2rad(theta_rest)
    a = np.tan(-theta / 2)
    b = np.sin(theta)

    xOp = xp.exp(-2j * np.pi * qxa * ya * a)
    yOp = xp.exp(-2j * np.pi * qya * xa * b)

    output_arr = input_arr.copy()

    # 90 degree rotation
    if abs(theta_90) > 0:
        if plane_dims[0] == plane_dims[1]:
            output_arr = xp.rot90(output_arr, theta_90, axes=axes)
        else:
            if plane_dims[0] > plane_dims[1]:
                xx = np.arange(plane_dims[1]) + (plane_dims[0] - plane_dims[1]) // 2
                if rotation_ax == 0:
                    output_arr[:, xx, :] = xp.rot90(
                        output_arr[:, xx, :], theta_90, axes=axes
                    )
                    output_arr[:, : xx[0], :] = 0
                    output_arr[:, xx[-1] :, :] = 0
                else:
                    output_arr[xx, :, :] = xp.rot90(
                        output_arr[xx, :, :], theta_90, axes=axes
                    )
                    output_arr[: xx[0], :, :] = 0
                    output_arr[xx[-1] :, :, :] = 0
            else:
                yy = np.arange(plane_dims[0]) + (plane_dims[1] - plane_dims[0]) // 2
                if rotation_ax == 2:
                    output_arr[:, yy, :] = xp.rot90(
                        output_arr[:, yy, :], theta_90, axes=axes
                    )
                    output_arr[:, : yy[0], :] = 0
                    output_arr[:, yy[-1] :, :] = 0
                else:
                    output_arr[:, :, yy] = xp.rot90(
                        output_arr[:, :, yy], theta_90, axes=axes
                    )
                    output_arr[:, :, : yy[0]] = 0
                    output_arr[:, :, yy[-1] :] = 0

    # small rotation
    if rotation_ax == 0:
        output_arr = xp.fft.ifft(xp.fft.fft(output_arr, axis=1) * xOp[None, :], axis=1)
        output_arr = xp.fft.ifft(xp.fft.fft(output_arr, axis=2) * yOp[None, :], axis=2)
        output_arr = xp.fft.ifft(xp.fft.fft(output_arr, axis=1) * xOp[None, :], axis=1)
        output_arr = xp.real(output_arr)

    elif rotation_ax == 1:
        output_arr = xp.fft.ifft(
            xp.fft.fft(output_arr, axis=0) * xOp[:, None, :], axis=0
        )
        output_arr = xp.fft.ifft(
            xp.fft.fft(output_arr, axis=2) * yOp[:, None, :], axis=2
        )
        output_arr = xp.fft.ifft(
            xp.fft.fft(output_arr, axis=0) * xOp[:, None, :], axis=0
        )
        output_arr = np.real(output_arr)

    else:
        output_arr = xp.fft.ifft(
            xp.fft.fft(output_arr, axis=0) * xOp[:, :, None], axis=0
        )
        output_arr = xp.fft.ifft(
            xp.fft.fft(output_arr, axis=1) * yOp[:, :, None], axis=1
        )
        output_arr = xp.fft.ifft(
            xp.fft.fft(output_arr, axis=0) * xOp[:, :, None], axis=0
        )
        output_arr = xp.real(output_arr)

    return output_arr


def array_slice(axis, ndim, start, end, step=1):
    """Returns array slice along dynamic axis"""
    return (slice(None),) * (axis % ndim) + (slice(start, end, step),)


### Divergence Projection Functions


def periodic_centered_difference(array, spacing, axis, xp=np):
    """Computes second-order centered difference with periodic BCs"""
    return (xp.roll(array, -1, axis=axis) - xp.roll(array, 1, axis=axis)) / (
        2 * spacing
    )


def compute_divergence_periodic(vector_field, spacings, xp=np):
    """Computes divergence of vector_field"""
    num_dims = len(spacings)
    div = xp.zeros_like(vector_field[0])

    for i in range(num_dims):
        div += periodic_centered_difference(vector_field[i], spacings[i], axis=i, xp=xp)

    return div


def compute_gradient_periodic(scalar_field, spacings, xp=np):
    """Computes gradient of scalar_field"""
    num_dims = len(spacings)
    grad = xp.zeros((num_dims,) + scalar_field.shape)

    for i in range(num_dims):
        grad[i] = periodic_centered_difference(scalar_field, spacings[i], axis=i, xp=xp)

    return grad


def preconditioned_laplacian_periodic_3D(shape, xp=np):
    """FFT eigenvalues"""
    n, m, p = shape
    i, j, k = xp.ogrid[0:n, 0:m, 0:p]

    op = 6 - 2 * xp.cos(2 * np.pi * i / n) * xp.cos(2 * np.pi * j / m) * xp.cos(
        2 * np.pi * k / p
    )
    op[0, 0, 0] = 1  # gauge invariance
    return -op


def preconditioned_poisson_solver_periodic_3D(rhs, gauge=None, xp=np):
    """FFT based poisson solver"""
    op = preconditioned_laplacian_periodic_3D(rhs.shape, xp=xp)

    if gauge is None:
        gauge = xp.mean(rhs)

    fft_rhs = xp.fft.fftn(rhs)
    fft_rhs[0, 0, 0] = gauge  # gauge invariance
    sol = xp.fft.ifftn(fft_rhs / op).real
    return sol


def project_vector_field_divergence_periodic_3D(vector_field, xp=np):
    """
    Returns solenoidal part of vector field using projection:

    f - \\grad{p}
    s.t. \\laplacian{p} = \\div{f}
    """
    spacings = (1, 1, 1)
    div_v = compute_divergence_periodic(vector_field, spacings, xp=xp)
    p = preconditioned_poisson_solver_periodic_3D(div_v, xp=xp)
    grad_p = compute_gradient_periodic(p, spacings, xp=xp)
    return vector_field - grad_p


# Nesterov acceleration functions
# https://blogs.princeton.edu/imabandit/2013/04/01/acceleratedgradientdescent/


@functools.cache
def nesterov_lambda(one_indexed_iter_num):
    if one_indexed_iter_num == 0:
        return 0
    return (1 + np.sqrt(1 + 4 * nesterov_lambda(one_indexed_iter_num - 1) ** 2)) / 2


def nesterov_gamma(zero_indexed_iter_num):
    one_indexed_iter_num = zero_indexed_iter_num + 1
    return (1 - nesterov_lambda(one_indexed_iter_num)) / nesterov_lambda(
        one_indexed_iter_num + 1
    )


def cartesian_to_polar_transform_2Ddata(
    im_cart,
    xy_center,
    num_theta_bins=90,
    radius_max=None,
    corner_centered=False,
    xp=np,
):
    """
    Quick cartesian to polar conversion.
    """

    # coordinates
    if radius_max is None:
        if corner_centered:
            radius_max = np.min(np.array(im_cart.shape) // 2)
        else:
            radius_max = np.sqrt(np.sum(np.array(im_cart.shape) ** 2)) // 2

    r = xp.arange(radius_max)
    t = xp.linspace(
        0,
        2.0 * np.pi,
        num_theta_bins,
        endpoint=False,
    )
    ra, ta = xp.meshgrid(r, t)

    # resampling coordinates
    x = ra * xp.cos(ta) + xy_center[0]
    y = ra * xp.sin(ta) + xy_center[1]

    xf = xp.floor(x).astype("int")
    yf = xp.floor(y).astype("int")
    dx = x - xf
    dy = y - yf

    mode = "wrap" if corner_centered else "clip"

    # resample image
    im_polar = (
        im_cart.ravel()[
            xp.ravel_multi_index(
                (xf, yf),
                im_cart.shape,
                mode=mode,
            )
        ]
        * (1 - dx)
        * (1 - dy)
        + im_cart.ravel()[
            xp.ravel_multi_index(
                (xf + 1, yf),
                im_cart.shape,
                mode=mode,
            )
        ]
        * (dx)
        * (1 - dy)
        + im_cart.ravel()[
            xp.ravel_multi_index(
                (xf, yf + 1),
                im_cart.shape,
                mode=mode,
            )
        ]
        * (1 - dx)
        * (dy)
        + im_cart.ravel()[
            xp.ravel_multi_index(
                (xf + 1, yf + 1),
                im_cart.shape,
                mode=mode,
            )
        ]
        * (dx)
        * (dy)
    )

    return im_polar


def polar_to_cartesian_transform_2Ddata(
    im_polar,
    xy_size,
    xy_center,
    corner_centered=False,
    xp=np,
):
    """
    Quick polar to cartesian conversion.
    """

    # coordinates
    sx, sy = xy_size
    cx, cy = xy_center

    if corner_centered:
        x = xp.fft.fftfreq(sx, d=1 / sx).astype(xp.float32)
        y = xp.fft.fftfreq(sy, d=1 / sy).astype(xp.float32)
    else:
        x = xp.arange(sx, dtype=xp.float32)
        y = xp.arange(sy, dtype=xp.float32)

    xa, ya = xp.meshgrid(x, y, indexing="ij")
    ra = xp.hypot(xa - cx, ya - cy)
    ta = xp.arctan2(ya - cy, xa - cx)

    t = xp.linspace(0, 2 * np.pi, im_polar.shape[0], endpoint=False)
    t_step = t[1] - t[0]

    # resampling coordinates
    t_ind = ta / t_step
    r_ind = ra.copy()
    tf = xp.floor(t_ind).astype("int")
    rf = xp.floor(r_ind).astype("int")

    # resample image
    im_cart = im_polar.ravel()[
        xp.ravel_multi_index(
            (tf, rf),
            im_polar.shape,
            mode=("wrap", "clip"),
        )
    ]

    return im_cart


def regularize_probe_amplitude(
    probe_init,
    width_max_pixels=2.0,
    nearest_angular_neighbor_averaging=5,
    enforce_constant_intensity=True,
    corner_centered=False,
):
    """
    Fits sigmoid for each angular direction.

    Parameters
    --------
    probe_init: np.array
        2D complex image of the probe in Fourier space.
    width_max_pixels: float
        Maximum edge width of the probe in pixels.
    nearest_angular_neighbor_averaging: int
        Number of nearest angular neighbor pixels to average to make aperture less jagged.
    enforce_constant_intensity: bool
        Set to true to make intensity inside the aperture constant.
    corner_centered: bool
        If True, the probe is assumed to be corner-centered

    Returns
    --------
    probe_corr: np.ndarray
        2D complex image of the corrected probe in Fourier space.
    coefs_all: np.ndarray
        coefficients for the sigmoid fits
    """

    # Get probe intensity
    probe_amp = np.abs(probe_init)
    probe_angle = np.angle(probe_init)
    probe_int = probe_amp**2

    # Center of mass for probe intensity
    xy_center = get_CoM(probe_int, device="cpu", corner_centered=corner_centered)

    # Convert intensity to polar coordinates
    polar_int = cartesian_to_polar_transform_2Ddata(
        probe_int,
        xy_center=xy_center,
        corner_centered=corner_centered,
        xp=np,
    )

    # Fit corrected probe intensity
    radius = np.arange(polar_int.shape[1])

    # estimate initial parameters
    sub = polar_int > (np.max(polar_int) * 0.5)
    sig_0 = np.mean(polar_int[sub])
    rad_0 = np.max(np.argwhere(np.sum(sub, axis=0)))
    width = width_max_pixels * 0.5

    # init
    def step_model(radius, sig_0, rad_0, width):
        return sig_0 * np.clip((rad_0 - radius) / width, 0.0, 1.0)

    coefs_all = np.zeros((polar_int.shape[0], 3))
    coefs_all[:, 0] = sig_0
    coefs_all[:, 1] = rad_0
    coefs_all[:, 2] = width

    # bounds
    lb = (0.0, 0.0, 1e-4)
    ub = (np.inf, np.inf, width_max_pixels)

    # refine parameters, generate polar image
    polar_fit = np.zeros_like(polar_int)
    for a0 in range(polar_int.shape[0]):
        coefs_all[a0, :] = curve_fit(
            step_model,
            radius,
            polar_int[a0, :],
            p0=coefs_all[a0, :],
            xtol=1e-12,
            bounds=(lb, ub),
        )[0]
        polar_fit[a0, :] = step_model(radius, *coefs_all[a0, :])

    # Compute best-fit constant intensity inside probe, update bounds
    sig_0 = np.median(coefs_all[:, 0])
    coefs_all[:, 0] = sig_0
    lb = (sig_0 - 1e-8, 0.0, 1e-4)
    ub = (sig_0 + 1e-8, np.inf, width_max_pixels)

    # refine parameters, generate polar image
    polar_int_corr = np.zeros_like(polar_int)
    for a0 in range(polar_int.shape[0]):
        coefs_all[a0, :] = curve_fit(
            step_model,
            radius,
            polar_int[a0, :],
            p0=coefs_all[a0, :],
            xtol=1e-12,
            bounds=(lb, ub),
        )[0]
        # polar_int_corr[a0, :] = step_model(radius, *coefs_all[a0, :])

    # make aperture less jagged, using moving mean
    coefs_all = np.apply_along_axis(
        uniform_filter1d,
        0,
        coefs_all,
        size=nearest_angular_neighbor_averaging,
        mode="wrap",
    )
    for a0 in range(polar_int.shape[0]):
        polar_int_corr[a0, :] = step_model(radius, *coefs_all[a0, :])

    # Convert back to cartesian coordinates
    int_corr = polar_to_cartesian_transform_2Ddata(
        polar_int_corr,
        xy_size=probe_init.shape,
        xy_center=xy_center,
        corner_centered=corner_centered,
    )

    amp_corr = np.sqrt(np.maximum(int_corr, 0))

    # Assemble output probe
    if not enforce_constant_intensity:
        max_coeff = np.sqrt(coefs_all[:, 0]).max()
        amp_corr = amp_corr / max_coeff * probe_amp

    probe_corr = amp_corr * np.exp(1j * probe_angle)

    return probe_corr, polar_int, polar_int_corr, coefs_all


def calculate_aberration_gradient_basis(
    aberrations_mn,
    sampling,
    gpts,
    wavelength,
    rotation_angle=0,
    xp=np,
):
    """ """
    sx, sy = sampling
    nx, ny = gpts
    qx = xp.fft.fftfreq(nx, sx).astype(xp.float32)
    qy = xp.fft.fftfreq(ny, sy).astype(xp.float32)
    qx, qy = xp.meshgrid(qx, qy, indexing="ij")

    # passive rotation
    qx, qy = qx * xp.cos(-rotation_angle) + qy * xp.sin(-rotation_angle), -qx * xp.sin(
        -rotation_angle
    ) + qy * xp.cos(-rotation_angle)

    # coordinate system
    qr2 = qx**2 + qy**2
    u = qx * wavelength
    v = qy * wavelength
    alpha = xp.sqrt(qr2) * wavelength
    theta = xp.arctan2(qy, qx)

    _aberrations_n = len(aberrations_mn)
    _aberrations_basis = xp.zeros((alpha.size, _aberrations_n))
    _aberrations_basis_du = xp.zeros((alpha.size, _aberrations_n))
    _aberrations_basis_dv = xp.zeros((alpha.size, _aberrations_n))

    for a0 in range(_aberrations_n):
        m, n, a = aberrations_mn[a0]

        if n == 0:
            # Radially symmetric basis
            _aberrations_basis[:, a0] = (alpha ** (m + 1) / (m + 1)).ravel()
            _aberrations_basis_du[:, a0] = (u * alpha ** (m - 1)).ravel()
            _aberrations_basis_dv[:, a0] = (v * alpha ** (m - 1)).ravel()

        elif a == 0:
            # cos coef
            _aberrations_basis[:, a0] = (
                alpha ** (m + 1) * xp.cos(n * theta) / (m + 1)
            ).ravel()
            _aberrations_basis_du[:, a0] = (
                alpha ** (m - 1)
                * ((m + 1) * u * xp.cos(n * theta) + n * v * xp.sin(n * theta))
                / (m + 1)
            ).ravel()
            _aberrations_basis_dv[:, a0] = (
                alpha ** (m - 1)
                * ((m + 1) * v * xp.cos(n * theta) - n * u * xp.sin(n * theta))
                / (m + 1)
            ).ravel()

        else:
            # sin coef
            _aberrations_basis[:, a0] = (
                alpha ** (m + 1) * xp.sin(n * theta) / (m + 1)
            ).ravel()
            _aberrations_basis_du[:, a0] = (
                alpha ** (m - 1)
                * ((m + 1) * u * xp.sin(n * theta) - n * v * xp.cos(n * theta))
                / (m + 1)
            ).ravel()
            _aberrations_basis_dv[:, a0] = (
                alpha ** (m - 1)
                * ((m + 1) * v * xp.sin(n * theta) + n * u * xp.cos(n * theta))
                / (m + 1)
            ).ravel()

    # global scaling
    _aberrations_basis *= 2 * np.pi / wavelength

    return _aberrations_basis, _aberrations_basis_du, _aberrations_basis_dv


def aberrations_basis_function(
    probe_size,
    probe_sampling,
    energy,
    max_angular_order,
    max_radial_order,
    xp=np,
):
    """ """

    # Add constant phase shift in basis
    mn = [[-1, 0, 0]]

    for m in range(1, max_radial_order):
        n_max = np.minimum(max_angular_order, m + 1)
        for n in range(0, n_max + 1):
            if (m + n) % 2:
                mn.append([m, n, 0])
                if n > 0:
                    mn.append([m, n, 1])

    aberrations_mn = np.array(mn)
    aberrations_mn = aberrations_mn[np.argsort(aberrations_mn[:, 1]), :]

    sub = aberrations_mn[:, 1] > 0
    aberrations_mn[sub, :] = aberrations_mn[sub, :][
        np.argsort(aberrations_mn[sub, 0]), :
    ]
    aberrations_mn[~sub, :] = aberrations_mn[~sub, :][
        np.argsort(aberrations_mn[~sub, 0]), :
    ]
    aberrations_num = aberrations_mn.shape[0]

    sx, sy = probe_size
    dx, dy = probe_sampling
    wavelength = electron_wavelength_angstrom(energy)

    qx = xp.fft.fftfreq(sx, dx).astype(xp.float32)
    qy = xp.fft.fftfreq(sy, dy).astype(xp.float32)
    qr2 = qx[:, None] ** 2 + qy[None, :] ** 2
    alpha = xp.sqrt(qr2) * wavelength
    theta = xp.arctan2(qy[None, :], qx[:, None])

    # Aberration basis
    aberrations_basis = xp.ones((alpha.size, aberrations_num))

    # Skip constant to avoid dividing by zero in normalization
    for a0 in range(1, aberrations_num):
        m, n, a = aberrations_mn[a0]
        if n == 0:
            # Radially symmetric basis
            aberrations_basis[:, a0] = (alpha ** (m + 1) / (m + 1)).ravel()

        elif a == 0:
            # cos coef
            aberrations_basis[:, a0] = (
                alpha ** (m + 1) * xp.cos(n * theta) / (m + 1)
            ).ravel()
        else:
            # sin coef
            aberrations_basis[:, a0] = (
                alpha ** (m + 1) * xp.sin(n * theta) / (m + 1)
            ).ravel()

    # global scaling
    aberrations_basis *= 2 * np.pi / wavelength

    return aberrations_basis, aberrations_mn


def interleave_ndarray_symmetrically(array_nd, axis, xp=np):
    """[a,b,c,d,e,f] -> [a,c,e,f,d,b]"""
    array_shape = np.array(array_nd.shape)
    d = array_nd.ndim
    n = array_shape[axis]

    array = xp.empty_like(array_nd)
    array[array_slice(axis, d, None, (n - 1) // 2 + 1)] = array_nd[
        array_slice(axis, d, None, None, 2)
    ]

    if n % 2:  # odd
        array[array_slice(axis, d, (n - 1) // 2 + 1, None)] = array_nd[
            array_slice(axis, d, -2, None, -2)
        ]
    else:  # even
        array[array_slice(axis, d, (n - 1) // 2 + 1, None)] = array_nd[
            array_slice(axis, d, None, None, -2)
        ]

    return array


def return_exp_factors(size, ndim, axis, xp=np):
    none_axes = [None] * ndim
    none_axes[axis] = slice(None)
    exp_factors = 2 * xp.exp(-1j * np.pi * xp.arange(size) / (2 * size))
    return exp_factors[tuple(none_axes)]


def dct_II_using_FFT_base(array_nd, xp=np):
    """FFT-based DCT-II"""
    d = array_nd.ndim

    for axis in range(d):
        n = array_nd.shape[axis]
        interleaved_array = interleave_ndarray_symmetrically(array_nd, axis=axis, xp=xp)
        exp_factors = return_exp_factors(n, d, axis, xp)
        interleaved_array = xp.fft.fft(interleaved_array, axis=axis)
        interleaved_array *= exp_factors
        array_nd = interleaved_array.real

    return array_nd


def dct_II_using_FFT(array_nd, xp=np):
    if xp.iscomplexobj(array_nd):
        real = dct_II_using_FFT_base(array_nd.real, xp=xp)
        imag = dct_II_using_FFT_base(array_nd.imag, xp=xp)
        return real + 1j * imag
    else:
        return dct_II_using_FFT_base(array_nd, xp=xp)


def interleave_ndarray_symmetrically_inverse(array_nd, axis, xp=np):
    """[a,c,e,f,d,b] -> [a,b,c,d,e,f]"""
    array_shape = np.array(array_nd.shape)
    d = array_nd.ndim
    n = array_shape[axis]

    array = xp.empty_like(array_nd)
    array[array_slice(axis, d, None, None, 2)] = array_nd[
        array_slice(axis, d, None, (n - 1) // 2 + 1)
    ]

    if n % 2:  # odd
        array[array_slice(axis, d, -2, None, -2)] = array_nd[
            array_slice(axis, d, (n - 1) // 2 + 1, None)
        ]
    else:  # even
        array[array_slice(axis, d, None, None, -2)] = array_nd[
            array_slice(axis, d, (n - 1) // 2 + 1, None)
        ]

    return array


def return_exp_factors_inverse(size, ndim, axis, xp=np):
    none_axes = [None] * ndim
    none_axes[axis] = slice(None)
    exp_factors = xp.exp(1j * np.pi * xp.arange(size) / (2 * size)) / 2
    return exp_factors[tuple(none_axes)]


def idct_II_using_FFT_base(array_nd, xp=np):
    """FFT-based IDCT-II"""
    d = array_nd.ndim

    for axis in range(d):
        n = array_nd.shape[axis]
        reversed_array = xp.roll(
            array_nd[array_slice(axis, d, None, None, -1)], 1, axis=axis
        )  # C(N-k)
        reversed_array[array_slice(axis, d, 0, 1)] = 0  # set C(N) = 0

        interleaved_array = array_nd - 1j * reversed_array
        exp_factors = return_exp_factors_inverse(n, d, axis, xp)
        interleaved_array *= exp_factors

        array_nd = xp.fft.ifft(interleaved_array, axis=axis).real
        array_nd = interleave_ndarray_symmetrically_inverse(array_nd, axis=axis, xp=xp)

    return array_nd


def idct_II_using_FFT(array_nd, xp=np):
    """FFT-based IDCT-II"""
    if xp.iscomplexobj(array_nd):
        real = idct_II_using_FFT_base(array_nd.real, xp=xp)
        imag = idct_II_using_FFT_base(array_nd.imag, xp=xp)
        return real + 1j * imag
    else:
        return idct_II_using_FFT_base(array_nd, xp=xp)


def preconditioned_laplacian_neumann_2D(shape, xp=np):
    """DCT eigenvalues"""
    n, m = shape
    i, j = xp.ogrid[0:n, 0:m]

    op = 4 - 2 * xp.cos(np.pi * i / n) - 2 * xp.cos(np.pi * j / m)
    op[0, 0] = 1  # gauge invariance
    return -op


def preconditioned_poisson_solver_neumann_2D(rhs, gauge=None, xp=np):
    """DCT based poisson solver"""
    op = preconditioned_laplacian_neumann_2D(rhs.shape, xp=xp)

    if gauge is None:
        gauge = xp.mean(rhs)

    if xp is np:
        fft_rhs = dctn(rhs, type=2)
        fft_rhs[0, 0] = gauge  # gauge invariance
        sol = idctn(fft_rhs / op, type=2).real
    else:
        fft_rhs = dct_II_using_FFT(rhs, xp)
        fft_rhs[0, 0] = gauge  # gauge invariance
        sol = idct_II_using_FFT(fft_rhs / op, xp)

    return sol


def unwrap_phase_2d(array, weights=None, gauge=None, corner_centered=True, xp=np):
    """Weigted phase unwrapping using DCT-based poisson solver"""

    if np.iscomplexobj(array):
        raise ValueError()

    if corner_centered:
        array = xp.fft.fftshift(array)
        if weights is not None:
            weights = xp.fft.fftshift(weights)

    dx = xp.mod(xp.diff(array, axis=0) + np.pi, 2 * np.pi) - np.pi
    dy = xp.mod(xp.diff(array, axis=1) + np.pi, 2 * np.pi) - np.pi

    if weights is not None:
        # normalize weights
        weights -= weights.min()
        weights /= weights.max()

        ww = weights**2
        dx *= xp.minimum(ww[:-1, :], ww[1:, :])
        dy *= xp.minimum(ww[:, :-1], ww[:, 1:])

    rho = xp.diff(dx, axis=0, prepend=0, append=0)
    rho += xp.diff(dy, axis=1, prepend=0, append=0)

    unwrapped_array = preconditioned_poisson_solver_neumann_2D(rho, gauge=gauge, xp=xp)
    unwrapped_array -= unwrapped_array.min()

    if corner_centered:
        unwrapped_array = xp.fft.ifftshift(unwrapped_array)

    return unwrapped_array


def unwrap_phase_2d_skimage(array, corner_centered=True, xp=np):
    from skimage.restoration import unwrap_phase

    if xp is np:
        array = array.astype(np.float64)
        unwrapped_array = unwrap_phase(array, wrap_around=corner_centered).astype(
            xp.float32
        )
    else:
        array = xp.asnumpy(array).astype(np.float64)
        unwrapped_array = unwrap_phase(array, wrap_around=corner_centered)
        unwrapped_array = xp.asarray(unwrapped_array).astype(xp.float32)

    return unwrapped_array


def fit_aberration_surface(
    complex_probe,
    probe_sampling,
    energy,
    max_angular_order,
    max_radial_order,
    use_scikit_image,
    xp=np,
):
    """ """
    probe_amp = xp.abs(complex_probe)
    probe_angle = -xp.angle(complex_probe)

    if use_scikit_image:
        unwrapped_angle = unwrap_phase_2d_skimage(
            probe_angle,
            corner_centered=True,
            xp=xp,
        )

    else:
        unwrapped_angle = unwrap_phase_2d(
            probe_angle,
            weights=probe_amp,
            corner_centered=True,
            xp=xp,
        )

    raveled_basis, _ = aberrations_basis_function(
        complex_probe.shape,
        probe_sampling,
        energy,
        max_angular_order,
        max_radial_order,
        xp=xp,
    )

    raveled_weights = probe_amp.ravel()

    Aw = raveled_basis * raveled_weights[:, None]
    bw = unwrapped_angle.ravel() * raveled_weights
    coeff = xp.linalg.lstsq(Aw, bw, rcond=None)[0]

    fitted_angle = xp.tensordot(raveled_basis, coeff, axes=1).reshape(probe_angle.shape)
    angle_offset = fitted_angle[0, 0] - probe_angle[0, 0]
    fitted_angle -= angle_offset

    return fitted_angle, coeff


def rotate_point(origin, point, angle):
    """
    Rotate a point (x1, y1) counterclockwise by a given angle around
    a given origin (x0, y0).

    Parameters
    --------
    origin: 2-tuple of floats
        (x0, y0)
    point: 2-tuple of floats
        (x1, y1)
    angle: float (radians)

    Returns
    --------
    rotated points (2-tuple)

    """
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return qx, qy


def bilinearly_interpolate_array(
    image,
    xa,
    ya,
    xp=np,
    max_batch_size=None,
):
    """
    Bilinear sampling of intensities from an image array and pixel positions.

    Parameters
    ----------
    image: np.ndarray
        Image array to sample from
    xa: np.ndarray
        Vertical interpolation sampling positions of image array in pixels
    ya: np.ndarray
        Horizontal interpolation sampling positions of image array in pixels

    Returns
    -------
    intensities: np.ndarray
        Bilinearly-sampled intensities of array at (xa,ya) positions

    """

    xF = xp.floor(xa.ravel()).astype("int")
    yF = xp.floor(ya.ravel()).astype("int")
    dx = xa.ravel() - xF
    dy = ya.ravel() - yF

    raveled_image = image.ravel()
    intensities = xp.zeros(xF.shape, dtype=xp.float32)

    if max_batch_size is None:
        max_batch_size = xF.shape[0]

    for start, end in generate_batches(xF.shape[0], max_batch=max_batch_size):
        for basis_index in range(4):
            match basis_index:
                case 0:
                    inds = [xF[start:end], yF[start:end]]
                    weights = (1 - dx[start:end]) * (1 - dy[start:end])
                case 1:
                    inds = [xF[start:end] + 1, yF[start:end]]
                    weights = (dx[start:end]) * (1 - dy[start:end])
                case 2:
                    inds = [xF[start:end], yF[start:end] + 1]
                    weights = (1 - dx[start:end]) * (dy[start:end])
                case 3:
                    inds = [xF[start:end] + 1, yF[start:end] + 1]
                    weights = (dx[start:end]) * (dy[start:end])

            inds_1D = xp.ravel_multi_index(
                inds,
                image.shape,
                mode=["wrap", "wrap"],
            )

            intensities[start:end] += raveled_image[inds_1D] * weights

    intensities = xp.reshape(
        intensities,
        xa.shape,
    )

    return intensities


def lanczos_interpolate_array(
    image,
    xa,
    ya,
    alpha,
    xp=np,
    max_batch_size=None,
):
    """
    Lanczos sampling of intensities from an image array and pixel positions.

    Parameters
    ----------
    image: np.ndarray
        Image array to sample from
    xa: np.ndarray
        Vertical Interpolation sampling positions of image array in pixels
    ya: np.ndarray
        Horizontal interpolation sampling positions of image array in pixels
    alpha: int
        Lanczos kernel order

    Returns
    -------
    intensities: np.ndarray
        Lanczos-sampled intensities of array at (xa,ya) positions

    """
    xF = xp.floor(xa.ravel()).astype("int")
    yF = xp.floor(ya.ravel()).astype("int")
    dx = xa.ravel() - xF
    dy = ya.ravel() - yF

    raveled_image = image.ravel()
    intensities = xp.zeros(xF.shape, dtype=xp.float32)
    filter_weights = xp.zeros(xF.shape, dtype=xp.float32)

    if max_batch_size is None:
        max_batch_size = xF.shape[0]

    for start, end in generate_batches(xF.shape[0], max_batch=max_batch_size):
        for i in range(-alpha + 1, alpha + 1):
            for j in range(-alpha + 1, alpha + 1):
                inds = [xF[start:end] + i, yF[start:end] + j]
                weights = (
                    xp.sinc(i - dx[start:end]) * xp.sinc((i - dx[start:end]) / alpha)
                ) * (xp.sinc(j - dy[start:end]) * xp.sinc((i - dy[start:end]) / alpha))

                inds_1D = xp.ravel_multi_index(
                    inds,
                    image.shape,
                    mode=["wrap", "wrap"],
                )
                intensities[start:end] += raveled_image[inds_1D] * weights
                filter_weights[start:end] += weights

    intensities = xp.reshape(
        intensities,
        xa.shape,
    )

    filter_weights = xp.reshape(
        filter_weights,
        xa.shape,
    )
    return intensities / filter_weights


def pixel_rolling_kernel_density_estimate(
    stack,
    shifts,
    upsampling_factor,
    kde_sigma,
    lowpass_filter=False,
    xp=np,
    gaussian_filter=gaussian_filter,
):
    """
    kernel density estimate from a set coordinates (xa,ya) and intensity weights.

    Parameters
    ----------
    stack: np.ndarray
        Unshifted image stack, shape (N,P,S)
    shifts: np.ndarray
        Shifts for each image in stack, shape: (N,2)
    upsampling_factor: int
        Upsampling factor
    kde_sigma: float
        KDE gaussian kernel bandwidth in upsampled pixels
    lowpass_filter: bool, optional
        If True, the resulting KDE upsampled image is lowpass-filtered using a sinc-function

    Returns
    -------
    pix_output: np.ndarray
        Upsampled intensity image
    """
    upsampled_shape = np.array(stack.shape[-2:])
    upsampled_shape *= upsampling_factor

    upsampled_shifts = shifts * upsampling_factor
    upsampled_shifts_int = xp.modf(upsampled_shifts)[-1].astype("int")

    pix_output = xp.zeros(upsampled_shape, dtype=xp.float32)
    pix_count = xp.zeros(upsampled_shape, dtype=xp.float32)
    upsampled_stack = xp.zeros(upsampled_shape, dtype=xp.float32)

    for BF_index in range(stack.shape[0]):
        shift = upsampled_shifts_int[BF_index]

        # values
        upsampled_stack[::upsampling_factor, ::upsampling_factor] = stack[BF_index]
        pix_output += xp.roll(upsampled_stack, shift, axis=(0, 1))

        # counts
        upsampled_stack[::upsampling_factor, ::upsampling_factor] = 1
        pix_count += xp.roll(upsampled_stack, shift, axis=(0, 1))

    # kernel density estimate
    pix_count = gaussian_filter(pix_count, kde_sigma)
    pix_output = gaussian_filter(pix_output, kde_sigma)

    sub = pix_count > 1e-3
    pix_output[sub] /= pix_count[sub]
    pix_output[np.logical_not(sub)] = 1

    if lowpass_filter:
        pix_fft = xp.fft.fft2(pix_output)
        pix_fft /= xp.sinc(
            xp.fft.fftfreq(pix_output.shape[0], d=1.0).astype(xp.float32)
        )[:, None]
        pix_fft /= xp.sinc(
            xp.fft.fftfreq(pix_output.shape[1], d=1.0).astype(xp.float32)
        )[None]
        pix_output = xp.real(xp.fft.ifft2(pix_fft))

    return pix_output


def bilinear_kernel_density_estimate(
    xa,
    ya,
    intensities,
    output_shape,
    kde_sigma,
    lowpass_filter=False,
    xp=np,
    gaussian_filter=gaussian_filter,
    max_batch_size=None,
):
    """
    kernel density estimate from a set coordinates (xa,ya) and intensity weights.

    Parameters
    ----------
    xa: np.ndarray
        Vertical positions of intensity array in pixels
    ya: np.ndarray
        Horizontal positions of intensity array in pixels
    intensities: np.ndarray
        Intensity array weights
    output_shape: (int,int)
        Upsampled intensities shape
    kde_sigma: float
        KDE gaussian kernel bandwidth in upsampled pixels
    lowpass_filter: bool, optional
        If True, the resulting KDE upsampled image is lowpass-filtered using a sinc-function

    Returns
    -------
    pix_output: np.ndarray
        Upsampled intensity image
    """

    # interpolation
    xF = xp.floor(xa.ravel()).astype("int")
    yF = xp.floor(ya.ravel()).astype("int")
    dx = xa.ravel() - xF
    dy = ya.ravel() - yF

    raveled_intensities = intensities.ravel()
    pix_count = xp.zeros(np.prod(output_shape), dtype=xp.float32)
    pix_output = xp.zeros(np.prod(output_shape), dtype=xp.float32)

    if max_batch_size is None:
        max_batch_size = xF.shape[0]

    for start, end in generate_batches(xF.shape[0], max_batch=max_batch_size):
        for basis_index in range(4):
            match basis_index:
                case 0:
                    inds = [xF[start:end], yF[start:end]]
                    weights = (1 - dx[start:end]) * (1 - dy[start:end])
                case 1:
                    inds = [xF[start:end] + 1, yF[start:end]]
                    weights = (dx[start:end]) * (1 - dy[start:end])
                case 2:
                    inds = [xF[start:end], yF[start:end] + 1]
                    weights = (1 - dx[start:end]) * (dy[start:end])
                case 3:
                    inds = [xF[start:end] + 1, yF[start:end] + 1]
                    weights = (dx[start:end]) * (dy[start:end])

            inds_1D = xp.ravel_multi_index(
                inds,
                output_shape,
                mode=["wrap", "wrap"],
            )

            pix_count += xp.bincount(
                inds_1D,
                weights=weights,
                minlength=np.prod(output_shape),
            )
            pix_output += xp.bincount(
                inds_1D,
                weights=weights * raveled_intensities[start:end],
                minlength=np.prod(output_shape),
            )

    # reshape 1D arrays to 2D
    pix_count = xp.reshape(
        pix_count,
        output_shape,
    )
    pix_output = xp.reshape(
        pix_output,
        output_shape,
    )

    # kernel density estimate
    pix_count = gaussian_filter(pix_count, kde_sigma)
    pix_output = gaussian_filter(pix_output, kde_sigma)
    sub = pix_count > 1e-3
    pix_output[sub] /= pix_count[sub]
    pix_output[np.logical_not(sub)] = 1

    if lowpass_filter:
        pix_fft = xp.fft.fft2(pix_output)
        pix_fft /= xp.sinc(
            xp.fft.fftfreq(pix_output.shape[0], d=1.0).astype(xp.float32)
        )[:, None]
        pix_fft /= xp.sinc(
            xp.fft.fftfreq(pix_output.shape[1], d=1.0).astype(xp.float32)
        )[None]
        pix_output = xp.real(xp.fft.ifft2(pix_fft))

    return pix_output


def lanczos_kernel_density_estimate(
    xa,
    ya,
    intensities,
    output_shape,
    kde_sigma,
    alpha,
    lowpass_filter=False,
    xp=np,
    gaussian_filter=gaussian_filter,
    max_batch_size=None,
):
    """
    kernel density estimate from a set coordinates (xa,ya) and intensity weights.

    Parameters
    ----------
    xa: np.ndarray
        Vertical positions of intensity array in pixels
    ya: np.ndarray
        Horizontal positions of intensity array in pixels
    intensities: np.ndarray
        Intensity array weights
    output_shape: (int,int)
        Upsampled intensities shape
    kde_sigma: float
        KDE gaussian kernel bandwidth in upsampled pixels
    alpha: int
        Lanczos kernel order
    lowpass_filter: bool, optional
        If True, the resulting KDE upsampled image is lowpass-filtered using a sinc-function

    Returns
    -------
    pix_output: np.ndarray
        Upsampled intensity image
    """

    # interpolation
    xF = xp.floor(xa.ravel()).astype("int")
    yF = xp.floor(ya.ravel()).astype("int")
    dx = xa.ravel() - xF
    dy = ya.ravel() - yF

    raveled_intensities = intensities.ravel()
    pix_count = xp.zeros(np.prod(output_shape), dtype=xp.float32)
    pix_output = xp.zeros(np.prod(output_shape), dtype=xp.float32)

    if max_batch_size is None:
        max_batch_size = xF.shape[0]

    for start, end in generate_batches(xF.shape[0], max_batch=max_batch_size):
        for i in range(-alpha + 1, alpha + 1):
            for j in range(-alpha + 1, alpha + 1):
                inds = [xF[start:end] + i, yF[start:end] + j]
                weights = (
                    xp.sinc(i - dx[start:end]) * xp.sinc((i - dx[start:end]) / alpha)
                ) * (xp.sinc(j - dy[start:end]) * xp.sinc((i - dy[start:end]) / alpha))

                inds_1D = xp.ravel_multi_index(
                    inds,
                    output_shape,
                    mode=["wrap", "wrap"],
                )

                pix_count += xp.bincount(
                    inds_1D,
                    weights=weights,
                    minlength=np.prod(output_shape),
                )
                pix_output += xp.bincount(
                    inds_1D,
                    weights=weights * raveled_intensities[start:end],
                    minlength=np.prod(output_shape),
                )

    # reshape 1D arrays to 2D
    pix_count = xp.reshape(
        pix_count,
        output_shape,
    )
    pix_output = xp.reshape(
        pix_output,
        output_shape,
    )

    # kernel density estimate
    pix_count = gaussian_filter(pix_count, kde_sigma)
    pix_output = gaussian_filter(pix_output, kde_sigma)
    sub = pix_count > 1e-3
    pix_output[sub] /= pix_count[sub]
    pix_output[np.logical_not(sub)] = 1

    if lowpass_filter:
        pix_fft = xp.fft.fft2(pix_output)
        pix_fft /= xp.sinc(
            xp.fft.fftfreq(pix_output.shape[0], d=1.0).astype(xp.float32)
        )[:, None]
        pix_fft /= xp.sinc(
            xp.fft.fftfreq(pix_output.shape[1], d=1.0).astype(xp.float32)
        )[None]
        pix_output = xp.real(xp.fft.ifft2(pix_fft))

    return pix_output


def bilinear_resample(
    array,
    scale=None,
    output_size=None,
    mode="grid-wrap",
    grid_mode=True,
    vectorized=True,
    conserve_array_sums=False,
    xp=np,
):
    """
    Resize an array along its final two axes.
    Note, this is vectorized by default and thus very memory-intensive.

    The scaling of the array can be specified by passing either `scale`, which sets
    the scaling factor along both axes to be scaled; or by passing `output_size`,
    which specifies the final dimensions of the scaled axes.

    Parameters
    ----------
    array: np.ndarray
        Input array to be resampled
    scale: float
        Scalar value giving the scaling factor for all dimensions
    output_size: (int,int)
        Tuple of two values giving the output size for the final two axes
    xp: Callable
        Array computing module

    Returns
    -------
    resampled_array: np.ndarray
        Resampled array
    """

    array_size = np.array(array.shape)
    input_size = array_size[-2:].copy()

    if scale is not None:
        scale = np.array(scale)
        if scale.size == 1:
            scale = np.tile(scale, 2)

        output_size = (input_size * scale).astype("int")
    else:
        if output_size is None:
            raise ValueError("One of `scale` or `output_size` must be provided.")
        output_size = np.array(output_size)
        if output_size.size != 2:
            raise ValueError("`output_size` must contain exactly two values.")
        output_size = np.array(output_size)

    scale_output = tuple(output_size / input_size)
    scale_output = (1,) * (array_size.size - input_size.size) + scale_output

    if xp is np:
        zoom_xp = zoom
    else:
        zoom_xp = zoom_cp

    if vectorized:
        array = zoom_xp(array, scale_output, order=1, mode=mode, grid_mode=grid_mode)
    else:
        flat_array = array.reshape((-1,) + tuple(input_size))
        out_array = xp.zeros(
            (flat_array.shape[0],) + tuple(output_size), flat_array.dtype
        )
        for idx in range(flat_array.shape[0]):
            out_array[idx] = zoom_xp(
                flat_array[idx],
                scale_output[-2:],
                order=1,
                mode=mode,
                grid_mode=grid_mode,
            )

        array = out_array.reshape(tuple(array_size[:-2]) + tuple(output_size))

    if conserve_array_sums:
        array = array / np.array(scale_output).prod()

    return array


def vectorized_fourier_resample(
    array,
    scale=None,
    output_size=None,
    conserve_array_sums=False,
    xp=np,
):
    """
    Resize a 2D array along any dimension, using Fourier interpolation.
    For 4D input arrays, only the final two axes can be resized.
    Note, this is vectorized and thus very memory-intensive.

    The scaling of the array can be specified by passing either `scale`, which sets
    the scaling factor along both axes to be scaled; or by passing `output_size`,
    which specifies the final dimensions of the scaled axes (and allows for different
    scaling along the x,y or kx,ky axes.)

    Parameters
    ----------
    array: np.ndarray
        Input 2D/4D array to be resampled
    scale: float
        Scalar value giving the scaling factor for all dimensions
    output_size: (int,int)
        Tuple of two values giving eith the (x,y) or (kx,ky) output size for 2D and 4D respectively.
    xp: Callable
        Array computing module

    Returns
    -------
    resampled_array: np.ndarray
        Resampled 2D/4D array
    """

    array_size = np.array(array.shape)
    input_size = array_size[-2:].copy()

    if scale is not None:
        scale = np.array(scale)
        if scale.size == 1:
            scale = np.tile(scale, 2)

        output_size = (input_size * scale).astype("int")
    else:
        if output_size is None:
            raise ValueError("One of `scale` or `output_size` must be provided.")
        output_size = np.array(output_size)
        if output_size.size != 2:
            raise ValueError("`output_size` must contain exactly two values.")
        output_size = np.array(output_size)

    scale_output = np.prod(output_size) / np.prod(input_size)

    # x slices
    if output_size[0] > input_size[0]:
        # x dimension increases
        x0 = (input_size[0] + 1) // 2
        x1 = input_size[0] // 2

        x_ul_out = slice(0, x0)
        x_ul_in_ = slice(0, x0)

        x_ll_out = slice(0 - x1 + output_size[0], output_size[0])
        x_ll_in_ = slice(0 - x1 + input_size[0], input_size[0])

        x_ur_out = slice(0, x0)
        x_ur_in_ = slice(0, x0)

        x_lr_out = slice(0 - x1 + output_size[0], output_size[0])
        x_lr_in_ = slice(0 - x1 + input_size[0], input_size[0])

    elif output_size[0] < input_size[0]:
        # x dimension decreases
        x0 = (output_size[0] + 1) // 2
        x1 = output_size[0] // 2

        x_ul_out = slice(0, x0)
        x_ul_in_ = slice(0, x0)

        x_ll_out = slice(0 - x1 + output_size[0], output_size[0])
        x_ll_in_ = slice(0 - x1 + input_size[0], input_size[0])

        x_ur_out = slice(0, x0)
        x_ur_in_ = slice(0, x0)

        x_lr_out = slice(0 - x1 + output_size[0], output_size[0])
        x_lr_in_ = slice(0 - x1 + input_size[0], input_size[0])

    else:
        # x dimension does not change
        x_ul_out = slice(None)
        x_ul_in_ = slice(None)

        x_ll_out = slice(None)
        x_ll_in_ = slice(None)

        x_ur_out = slice(None)
        x_ur_in_ = slice(None)

        x_lr_out = slice(None)
        x_lr_in_ = slice(None)

    # y slices
    if output_size[1] > input_size[1]:
        # y increases
        y0 = (input_size[1] + 1) // 2
        y1 = input_size[1] // 2

        y_ul_out = slice(0, y0)
        y_ul_in_ = slice(0, y0)

        y_ll_out = slice(0, y0)
        y_ll_in_ = slice(0, y0)

        y_ur_out = slice(0 - y1 + output_size[1], output_size[1])
        y_ur_in_ = slice(0 - y1 + input_size[1], input_size[1])

        y_lr_out = slice(0 - y1 + output_size[1], output_size[1])
        y_lr_in_ = slice(0 - y1 + input_size[1], input_size[1])

    elif output_size[1] < input_size[1]:
        # y decreases
        y0 = (output_size[1] + 1) // 2
        y1 = output_size[1] // 2

        y_ul_out = slice(0, y0)
        y_ul_in_ = slice(0, y0)

        y_ll_out = slice(0, y0)
        y_ll_in_ = slice(0, y0)

        y_ur_out = slice(0 - y1 + output_size[1], output_size[1])
        y_ur_in_ = slice(0 - y1 + input_size[1], input_size[1])

        y_lr_out = slice(0 - y1 + output_size[1], output_size[1])
        y_lr_in_ = slice(0 - y1 + input_size[1], input_size[1])

    else:
        # y dimension does not change
        y_ul_out = slice(None)
        y_ul_in_ = slice(None)

        y_ll_out = slice(None)
        y_ll_in_ = slice(None)

        y_ur_out = slice(None)
        y_ur_in_ = slice(None)

        y_lr_out = slice(None)
        y_lr_in_ = slice(None)

    # image array
    array_size[-2:] = output_size
    array_resize = xp.zeros(array_size, dtype=xp.complex64)
    array_fft = xp.fft.fft2(array)

    # copy each quadrant into the resize array
    array_resize[..., x_ul_out, y_ul_out] = array_fft[..., x_ul_in_, y_ul_in_]
    array_resize[..., x_ll_out, y_ll_out] = array_fft[..., x_ll_in_, y_ll_in_]
    array_resize[..., x_ur_out, y_ur_out] = array_fft[..., x_ur_in_, y_ur_in_]
    array_resize[..., x_lr_out, y_lr_out] = array_fft[..., x_lr_in_, y_lr_in_]

    # Back to real space
    array_resize = xp.real(xp.fft.ifft2(array_resize)).astype(xp.float32)

    # Normalization
    if not conserve_array_sums:
        array_resize = array_resize * scale_output

    return array_resize


def mask_array_using_virtual_detectors(
    corner_centered_array,
    corner_centered_masks,
    in_place=False,
):
    """ """
    xp = get_array_module(corner_centered_array)
    masks = xp.asarray(corner_centered_masks).astype(np.bool_)
    inverse_mask = (1 - masks.sum(0)).astype(np.bool_)

    if in_place:
        out_array = corner_centered_array
    else:
        out_array = corner_centered_array.copy()

    for mask in masks:
        val = xp.sum(out_array * mask, axis=(-1, -2)) / xp.sum(mask)
        out_array[..., mask] = val[..., None]
    out_array[..., inverse_mask] = 0.0

    return out_array


def partition_list(lst, size):
    """Partitions lst into chunks of size. Returns a generator."""
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def copy_to_device(array, device="cpu"):
    """Copies array to device. Default allows one to use this as asnumpy()"""
    xp = get_array_module(array)

    if xp is np:
        if device == "cpu":
            return np.asarray(array)
        elif device == "gpu":
            return cp.asarray(array)
        else:
            raise ValueError(f"device must be either 'cpu' or 'gpu', not {device}")
    else:
        if device == "cpu":
            return cp.asnumpy(array)
        elif device == "gpu":
            return cp.asarray(array)
        else:
            raise ValueError(f"device must be either 'cpu' or 'gpu', not {device}")


def polar_aberrations_to_cartesian(polar):
    """
    Convert between polar and Cartesian aberration coefficients.

    Parameters
    ----------
    polar: dict
        Mapping from polar aberration symbols to their corresponding values.

    Returns
    -------
    dict
        Mapping from cartesian aberration symbols to their corresponding values.
    """

    polar = defaultdict(lambda: 0.0, polar)

    max_order = 5
    cartesian = dict()
    for n in range(1, max_order + 1):
        for s in range(0, n + 2):
            m = 2 * s - n - 1
            if m < 0:
                continue

            modulus_name = "C" + str(n) + str(m)
            Ca_name = modulus_name + "a"
            Cb_name = modulus_name + "b"
            if m != 0:
                argument_name = "phi" + str(n) + str(m)
                cartesian[Ca_name] = polar[modulus_name] * np.cos(
                    polar[argument_name] * m
                )
                cartesian[Cb_name] = polar[modulus_name] * np.sin(
                    polar[argument_name] * m
                )
            else:
                cartesian[modulus_name] = polar[modulus_name]

    return cartesian


def cartesian_aberrations_to_polar(cartesian):
    """
    Convert between Cartesian and polar aberration coefficients.

    Parameters
    ----------
    cartesian: dict
        Mapping from Cartesian aberration symbols to their corresponding values.

    Returns
    -------
    dict
        Mapping from polar aberration symbols to their corresponding values.
    """

    cartesian = defaultdict(lambda: 0.0, cartesian)
    max_order = 5
    polar = dict()
    for n in range(1, max_order + 1):
        for s in range(0, n + 2):
            m = 2 * s - n - 1
            if m < 0:
                continue

            modulus_name = "C" + str(n) + str(m)
            Ca_name = modulus_name + "a"
            Cb_name = modulus_name + "b"
            if m != 0:
                argument_name = "phi" + str(n) + str(m)
                polar[modulus_name] = np.sqrt(
                    cartesian[Ca_name] ** 2 + cartesian[Cb_name] ** 2
                )
                polar[argument_name] = (
                    np.arctan2(cartesian[Cb_name], cartesian[Ca_name]) / m
                )
            else:
                polar[modulus_name] = cartesian[modulus_name]
    return polar


### 3D Fourier Rotation
@functools.cache
def compute_fourier_rotation_shear_coefficients(X, Y, Z, W):
    """
    Returns the a..h shear coefficients for the rotation decomposition:

        R(q(X,Y,Z,W)) = Sy(a,b)@Sz(c,d)@Sx(e,f)@Sy(g,h),

    where q(X,Y,Z,W) is the quaternion representation of a rotation.

    Reference: 10.1016/j.gmod.2005.11.004
    """
    # force scalars
    X, Y, Z, W = float(X), float(Y), float(Z), float(W)

    try:
        # special cases
        if X == 0.0:
            a = Y / Z
            b = (1 - W**2) / (W * Z)
            c = -2 * Y / W
            d = -2 * Y * Z
            e = -2 * W * Z
            f = 0
            g = -Y / Z
            h = (1 - W**2) / (W * Z)

        elif Y == 0.0:
            a = -X / W
            b = Z / W
            c = 0
            d = 2 * W * X
            e = -2 * W * Z
            f = 0
            g = -X / W
            h = Z / W

        elif Z == 0.0:
            a = (W**2 - 1) / (W * X)
            b = Y / X
            c = 0
            d = 2 * W * X
            e = 2 * X * Y
            f = 2 * Y / W
            g = (W**2 - 1) / (W * X)
            h = -Y / X

        # general case
        else:
            a = (X**2 + Y**2) / (Y * Z - X * W)
            b = (Y**2 - Z**2) / (X * Y - Z * W) - 2 * (
                Y * Z * (X**2 + Y**2)
            ) / ((X * Y - Z * W) * (Y * Z - X * W))
            c = 2 * Y * Z / (X * Y - Z * W)
            d = 2 * (X * W - Y * Z)
            e = 2 * (X * Y - Z * W)
            f = -2 * X * Y / (Y * Z - X * W)
            g = (X**2 - Y**2) / (Y * Z - X * W) + 2 * (
                X * Y * (Y**2 + Z**2)
            ) / ((X * Y - Z * W) * (Y * Z - X * W))
            h = (-1 + X**2 + W**2) / (X * Y - Z * W)

        return np.array([a, b, c, d, e, f, g, h]).reshape(4, 2)

    # singular
    except ZeroDivisionError:
        return np.full((4, 2), np.inf)


def compute_fourier_rotation_shears_combination(X, Y, Z, W):
    """
    Computes all six sets of shear coefficients for the combinations:
        SySzSxSy, SzSxSySz, SxSySzSx, SySxSzSy, SzSySxSz, SxSzSySx
    """
    all_coeffs = np.empty((6, 4, 2))

    for index in range(6):
        match index:
            case 0:  # SySzSxSy
                coeffs = compute_fourier_rotation_shear_coefficients(X, Y, Z, W)
            case 1:  # SzSxSySz
                coeffs = compute_fourier_rotation_shear_coefficients(Y, Z, X, W)
            case 2:  # SxSySzSx
                coeffs = compute_fourier_rotation_shear_coefficients(Z, X, Y, W)
            case 3:  # SySzSxSy complement
                coeffs = -np.flipud(
                    compute_fourier_rotation_shear_coefficients(X, Y, Z, -W)
                )
            case 4:  # SzSxSySz complement
                coeffs = -np.flipud(
                    compute_fourier_rotation_shear_coefficients(Y, Z, X, -W)
                )
            case 5:  # SxSySzSx complement
                coeffs = -np.flipud(
                    compute_fourier_rotation_shear_coefficients(Z, X, Y, -W)
                )

        all_coeffs[index] = coeffs

    return all_coeffs


def compute_fourier_rotation_best_shears_combination(X, Y, Z, W):
    """
    Computes all six sets of shear coefficients for the combinations:
        SySzSxSy, SzSxSySz, SxSySzSx, SySxSzSy, SzSySxSz, SxSzSySx
    and returns the one with the smallest squared coefficients.
    """
    all_coeffs = compute_fourier_rotation_shears_combination(X, Y, Z, W)
    all_orders = np.array(
        [
            [1, 2, 0, 1],
            [2, 0, 1, 2],
            [0, 1, 2, 0],
            [1, 0, 2, 1],
            [2, 1, 0, 2],
            [0, 2, 1, 0],
        ]
    )

    # ind = np.argmin(np.sum(all_coeffs**2, axis=(-1, -2)))

    flat_coeffs = all_coeffs.reshape((6, -1))
    metric = np.zeros(6)
    for indices in [[0, 6], [1, 7], [2], [3], [4], [5]]:  # |a+g| + |b+h| + |c| + ...
        metric += np.abs(flat_coeffs[:, indices].sum(-1))
    ind = np.argmin(metric)

    return all_orders[ind], all_coeffs[ind]


def fourier_rotation_best_shears_combination(tf):
    """Memoized version of function above which accepts tf matrices as input"""
    quaternion = Rotation.from_matrix(tf).as_quat()
    return compute_fourier_rotation_best_shears_combination(*quaternion)


def fourier_shear_Sx(array, a, b, xp=np):
    """ """
    Nx, Ny, Nz = array.shape
    nx = xp.arange(Nx, dtype=xp.float32) - (Nx - 1) / 2
    ny, nz = tuple(xp.fft.fftfreq(N, 1 / N).astype(xp.float32) for N in [Ny, Nz])
    nxa, nya, nza = xp.meshgrid(nx, ny, nz, indexing="ij")
    phase_shift = xp.exp(-2j * np.pi * (a * nya + b * nza) * nxa / Nx)

    array_fft = xp.fft.fft2(array, axes=(1, 2))
    return xp.fft.ifft2(array_fft * phase_shift, axes=(1, 2))


def fourier_shear_Sy(array, a, b, xp=np):
    """ """
    Nx, Ny, Nz = array.shape
    ny = xp.arange(Ny, dtype=xp.float32) - (Ny - 1) / 2
    nx, nz = tuple(xp.fft.fftfreq(N, 1 / N).astype(xp.float32) for N in [Nx, Nz])
    nxa, nya, nza = xp.meshgrid(nx, ny, nz, indexing="ij")
    phase_shift = xp.exp(-2j * np.pi * (a * nza + b * nxa) * nya / Ny)

    array_fft = xp.fft.fft2(array, axes=(0, 2))
    return xp.fft.ifft2(array_fft * phase_shift, axes=(0, 2))


def fourier_shear_Sz(array, a, b, xp=np):
    """ """
    Nx, Ny, Nz = array.shape
    nz = xp.arange(Nz, dtype=xp.float32) - (Nz - 1) / 2
    nx, ny = tuple(xp.fft.fftfreq(N, 1 / N).astype(xp.float32) for N in [Nx, Ny])
    nxa, nya, nza = xp.meshgrid(nx, ny, nz, indexing="ij")
    phase_shift = xp.exp(-2j * np.pi * (a * nxa + b * nya) * nza / Nz)

    array_fft = xp.fft.fft2(array, axes=(0, 1))
    return xp.fft.ifft2(array_fft * phase_shift, axes=(0, 1))


def fourier_rotate_volume_base(array, tf, xp=np):
    """ """
    order, coeffs = fourier_rotation_best_shears_combination(tf)
    ordered_fns = [fourier_shear_Sx, fourier_shear_Sy, fourier_shear_Sz]

    if np.all(np.isinf(coeffs)):
        coeffs = np.zeros_like(coeffs)

    out_array = xp.asarray(array)
    for j, index in enumerate(order):
        fn = ordered_fns[index]
        out_array = fn(out_array, *coeffs[j], xp=xp)

    return out_array


def fourier_rotate_volume(array, tf, angle_threshold=np.pi / 9, xp=np):
    """ """

    cmplx_obj = xp.iscomplexobj(array)

    rot_vec = Rotation.from_matrix(tf).as_rotvec()
    k_rotations = np.ceil(np.linalg.norm(rot_vec) / angle_threshold).astype("int")
    if k_rotations > 1:
        tf_prime = Rotation.from_rotvec(rot_vec / k_rotations).as_matrix()
        for k in range(k_rotations):
            array = fourier_rotate_volume_base(array, tf_prime, xp=xp)
    else:
        array = fourier_rotate_volume_base(array, tf, xp=xp)

    return array if cmplx_obj else array.real


def distance_bw_orientation_matrices(tf1, tf2):
    """ """
    tf = tf1 @ tf2.T
    return Rotation.from_matrix(tf).magnitude()


def return_tsp_and_edge_weighted_graph(old_graph):

    try:
        import networkx as nx
    except (ImportError, ModuleNotFoundError) as exc:
        raise Exception(
            "traveling salesman weighting requires package networkx"
        ) from exc

    # permute nodes
    nodes = old_graph.nodes()
    order = old_graph.order()
    nodes = np.roll(nodes, np.random.randint(order))

    # calculate tsp on weighted graph with permuted nodes
    tsp = nx.approximation.traveling_salesman_problem(
        old_graph, cycle=False, nodes=nodes, method=nx.approximation.greedy_tsp
    )

    # weight previously visited edges to add diversity
    graph = old_graph.copy(as_view=False)
    for u, v in nx.utils.pairwise(tsp):
        graph[u][v]["weight"] += 0.5
        graph[v][u]["weight"] += 0.5

    return tsp, graph


def calculate_orientation_matrices_tsp_ordering(
    orientation_matrices, num_iter, angle_threshold=np.pi / 9
):
    """ """
    try:
        import networkx as nx
    except (ImportError, ModuleNotFoundError) as exc:
        raise Exception(
            "traveling salesman weighting requires package networkx"
        ) from exc

    n = len(orientation_matrices)
    distance_matrix = np.zeros((n, n))

    # loop over upper-triangular
    for ind_x in range(n):
        tf1 = orientation_matrices[ind_x]
        for ind_y in range(ind_x, n):
            tf2 = orientation_matrices[ind_y]
            distance_matrix[ind_x, ind_y] = distance_bw_orientation_matrices(tf1, tf2)

    # symmetrize and remove self-loops
    distance_matrix += distance_matrix.T
    distance_matrix[distance_matrix == 0.0] = np.inf

    # build graph
    edges = np.stack(np.where(distance_matrix <= angle_threshold), -1)
    nodes = np.arange(n)

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges, weight=1)

    # compute nested tsp
    tsps = []
    for n in range(num_iter):
        tsp, graph = return_tsp_and_edge_weighted_graph(graph)
        tsps.append(tsp)

    return tsps


def calculate_orientation_matrices_serpentine_ordering(
    orientation_matrices,
    num_iter,
    collective_measurement_updates,
):
    """ """
    fwd = np.arange(len(orientation_matrices))
    rvs = fwd[::-1] if collective_measurement_updates else np.flip(fwd[1:-1])

    tsps = list(itertools.islice(itertools.cycle((fwd, rvs)), num_iter))
    return tsps
