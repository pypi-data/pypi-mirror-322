import cv2
import random
import pyvips

import numpy as np

from typing import Any
from collections.abc import Sequence


from ..functional.blur import blur, gaussian_blur, median_blur
from albumentationsxl import random_utils
from albumentationsxl.core.transforms_interface import (
    ImageOnlyTransform,
    ScaleFloatType,
    ScaleIntType,
    to_tuple,
)


__all__ = ["Blur", "MotionBlur", "MedianBlur", "GaussianBlur", "AdvancedBlur"]


class Blur(ImageOnlyTransform):
    """Blur the input image using a random-sized kernel.

    Args:
        blur_limit (int, (int, int)): maximum kernel size for blurring the input image.
            Should be in range [3, inf). Default: (3, 7).
        p (float): probability of applying the transform. Default: 0.5.

    Targets:
        image

    Image types:
        uint8, float32
    """

    def __init__(self, blur_limit: ScaleIntType = 7, always_apply: bool = False, p: float = 0.5):
        super().__init__(always_apply, p)
        self.blur_limit = to_tuple(blur_limit, 3)

    def apply(self, img: pyvips.Image, ksize: int = 3, **params) -> pyvips.Image:
        return blur(img, ksize)

    def get_params(self) -> dict[str, Any]:
        return {"ksize": int(random.choice(list(range(self.blur_limit[0], self.blur_limit[1] + 1, 2))))}

    def get_transform_init_args_names(self) -> tuple[str, ...]:
        return ("blur_limit",)


class MotionBlur(Blur):
    """Apply motion blur to the input image using a random-sized kernel.

    Args:
        blur_limit (int): maximum kernel size for blurring the input image.
            Should be in range [3, inf). Default: (3, 7).
        allow_shifted (bool): if set to true creates non shifted kernels only,
            otherwise creates randomly shifted kernels. Default: True.
        p (float): probability of applying the transform. Default: 0.5.

    Targets:
        image

    Image types:
        uint8, float32
    """

    def __init__(
        self,
        blur_limit: ScaleIntType = 7,
        allow_shifted: bool = True,
        always_apply: bool = False,
        p: float = 0.5,
    ):
        super().__init__(blur_limit=blur_limit, always_apply=always_apply, p=p)
        self.allow_shifted = allow_shifted

        if not allow_shifted and self.blur_limit[0] % 2 != 1 or self.blur_limit[1] % 2 != 1:
            raise ValueError(f"Blur limit must be odd when centered=True. Got: {self.blur_limit}")

    def get_transform_init_args_names(self) -> tuple[str, ...]:
        return super().get_transform_init_args_names() + ("allow_shifted",)

    def apply(self, img: pyvips.Image, kernel: pyvips.Image = None, **params) -> pyvips.Image:  # type: ignore
        return img.conv(kernel, precision="integer")

    def get_params(self) -> dict[str, Any]:
        ksize = random.choice(list(range(self.blur_limit[0], self.blur_limit[1] + 1, 2)))
        if ksize <= 2:
            raise ValueError("ksize must be > 2. Got: {}".format(ksize))
        kernel = np.zeros((ksize, ksize), dtype=np.uint8)
        x1, x2 = random.randint(0, ksize - 1), random.randint(0, ksize - 1)
        if x1 == x2:
            y1, y2 = random.sample(range(ksize), 2)
        else:
            y1, y2 = random.randint(0, ksize - 1), random.randint(0, ksize - 1)

        def make_odd_val(v1, v2):
            len_v = abs(v1 - v2) + 1
            if len_v % 2 != 1:
                if v2 > v1:
                    v2 -= 1
                else:
                    v1 -= 1
            return v1, v2

        if not self.allow_shifted:
            x1, x2 = make_odd_val(x1, x2)
            y1, y2 = make_odd_val(y1, y2)

            xc = (x1 + x2) / 2
            yc = (y1 + y2) / 2

            center = ksize / 2 - 0.5
            dx = xc - center
            dy = yc - center
            x1, x2 = [int(i - dx) for i in [x1, x2]]
            y1, y2 = [int(i - dy) for i in [y1, y2]]

        cv2.line(kernel, (x1, y1), (x2, y2), 1, thickness=1)
        kernel = kernel.astype(np.uint8)
        kernel = pyvips.Image.new_from_list(kernel.tolist(), scale=np.sum(kernel))
        return {"kernel": kernel}


class MedianBlur(Blur):
    """Blur the input image using a median filter with a random aperture linear size.

    Args:
        blur_limit (int): maximum aperture linear size for blurring the input image.
            Must be odd and in range [3, inf). Default: (3, 7).
        p (float): probability of applying the transform. Default: 0.5.

    Targets:
        image

    Image types:
        uint8, float32
    """

    def __init__(self, blur_limit: ScaleIntType = 7, always_apply: bool = False, p: float = 0.5):
        super().__init__(blur_limit, always_apply, p)

        if self.blur_limit[0] % 2 != 1 or self.blur_limit[1] % 2 != 1:
            raise ValueError("MedianBlur supports only odd blur limits.")

    def apply(self, img: pyvips.Image, ksize: int = 3, **params) -> pyvips.Image:
        return median_blur(img, ksize)


class GaussianBlur(ImageOnlyTransform):
    """Blur the input image using a Gaussian filter with a random kernel size.

    This implementation is not faithful to albumentation's gaussian blur. CV2 libraries have a predefined kernel
    or sigma, or calculate either the radius/sigma from the given kernel size. Pyvips defines an amplitude that
    determines the accuracy of the mask: Given a certain accuracy, the kernel size may change given varying levels
    of sigma

    In short: opencv sets the speed of the algorithm with a predefined kernel size, and the accuracy of the mask
    differs with sigma. Pyvips sets the accuracy, and the kernel size will change with varying sigma.

    Reference: https://github.com/libvips/libvips/discussions/3038

    Args:
        sigma_limit (float, (float, float)): Gaussian kernel standard deviation. Must be in range [0, inf).
            If set single value `sigma_limit` will be in range (0, sigma_limit).
            If set to 0 sigma will be computed as `sigma = 0.3*((ksize-1)*0.5 - 1) + 0.8`. Default: 0.
        min_amplitude (float): must be in range [0,inf)
            accuracy of the mask, implicitly determines radius/kernel size. Lower values typically lead to higher accuracy
            and larger kernels, at the cost of speed. Recommended to keep this at default of 0.2
        p (float): probability of applying the transform. Default: 0.5.

    Targets:
        image

    Image types:
        uint8, float32
    """

    def __init__(
        self,
        sigma_limit: ScaleFloatType = 0,
        min_amplitude: float = 0.2,
        always_apply: bool = False,
        p: float = 0.5,
    ):
        super().__init__(always_apply, p)
        self.sigma_limit = to_tuple(sigma_limit if sigma_limit is not None else 0, 0)
        self.min_amplitude = min_amplitude

    def apply(self, img: pyvips.Image, min_amplitude: float = 0.2, sigma: float = 0, **params) -> pyvips.Image:
        return gaussian_blur(img, sigma=sigma, min_amplitude=self.min_amplitude)

    def get_params(self) -> dict[str, float]:
        return {"sigma": random.uniform(*self.sigma_limit)}

    def get_transform_init_args_names(self) -> tuple[str, str]:
        return "sigma_limit", "min_amplitude"


class AdvancedBlur(ImageOnlyTransform):
    """Blur the input image using a Generalized Normal filter with a randomly selected parameters.
        This transform also adds multiplicative noise to generated kernel before convolution.

    Args:
        blur_limit: maximum Gaussian kernel size for blurring the input image.
            Must be zero or odd and in range [0, inf). If set to 0 it will be computed from sigma
            as `round(sigma * (3 if img.dtype == np.uint8 else 4) * 2 + 1) + 1`.
            If set single value `blur_limit` will be in range (0, blur_limit).
            Default: (3, 7).
        sigmaX_limit: Gaussian kernel standard deviation. Must be in range [0, inf).
            If set single value `sigmaX_limit` will be in range (0, sigma_limit).
            If set to 0 sigma will be computed as `sigma = 0.3*((ksize-1)*0.5 - 1) + 0.8`. Default: 0.
        sigmaY_limit: Same as `sigmaY_limit` for another dimension.
        rotate_limit: Range from which a random angle used to rotate Gaussian kernel is picked.
            If limit is a single int an angle is picked from (-rotate_limit, rotate_limit). Default: (-90, 90).
        beta_limit: Distribution shape parameter, 1 is the normal distribution. Values below 1.0 make distribution
            tails heavier than normal, values above 1.0 make it lighter than normal. Default: (0.5, 8.0).
        noise_limit: Multiplicative factor that control strength of kernel noise. Must be positive and preferably
            centered around 1.0. If set single value `noise_limit` will be in range (0, noise_limit).
            Default: (0.75, 1.25).
        p (float): probability of applying the transform. Default: 0.5.

    Reference:
        https://arxiv.org/abs/2107.10833

    Targets:
        image
    Image types:
        uint8, float32
    """

    def __init__(
        self,
        blur_limit: ScaleIntType = (3, 7),
        sigmaX_limit: ScaleFloatType = (0.2, 1.0),
        sigmaY_limit: ScaleFloatType = (0.2, 1.0),
        rotate_limit: ScaleIntType = 90,
        beta_limit: ScaleFloatType = (0.5, 8.0),
        noise_limit: ScaleFloatType = (0.9, 1.1),
        always_apply: bool = False,
        p: float = 0.5,
    ):
        super().__init__(always_apply, p)
        self.blur_limit = to_tuple(blur_limit, 3)
        self.sigmaX_limit = self.__check_values(to_tuple(sigmaX_limit, 0.0), name="sigmaX_limit")
        self.sigmaY_limit = self.__check_values(to_tuple(sigmaY_limit, 0.0), name="sigmaY_limit")
        self.rotate_limit = to_tuple(rotate_limit)
        self.beta_limit = to_tuple(beta_limit, low=0.0)
        self.noise_limit = self.__check_values(to_tuple(noise_limit, 0.0), name="noise_limit")

        if (self.blur_limit[0] != 0 and self.blur_limit[0] % 2 != 1) or (
            self.blur_limit[1] != 0 and self.blur_limit[1] % 2 != 1
        ):
            raise ValueError("AdvancedBlur supports only odd blur limits.")

        if self.sigmaX_limit[0] == 0 and self.sigmaY_limit[0] == 0:
            raise ValueError("sigmaX_limit and sigmaY_limit minimum value can not be both equal to 0.")

        if not (self.beta_limit[0] < 1.0 < self.beta_limit[1]):
            raise ValueError("Beta limit is expected to include 1.0")

    @staticmethod
    def __check_values(
        value: Sequence[float], name: str, bounds: tuple[float, float] = (0, float("inf"))
    ) -> Sequence[float]:
        if not bounds[0] <= value[0] <= value[1] <= bounds[1]:
            raise ValueError(f"{name} values should be between {bounds}")
        return value

    def apply(self, img: pyvips.Image, kernel: pyvips.Image, **params) -> pyvips.Image:
        return img.conv(kernel, precision="integer")

    def get_params(self) -> dict[str, np.ndarray]:
        ksize = random.randrange(self.blur_limit[0], self.blur_limit[1] + 1, 2)
        sigmaX = random.uniform(*self.sigmaX_limit)
        sigmaY = random.uniform(*self.sigmaY_limit)
        angle = np.deg2rad(random.uniform(*self.rotate_limit))

        # Split into 2 cases to avoid selection of narrow kernels (beta > 1) too often.
        if random.random() < 0.5:
            beta = random.uniform(self.beta_limit[0], 1)
        else:
            beta = random.uniform(1, self.beta_limit[1])

        noise_matrix = random_utils.uniform(self.noise_limit[0], self.noise_limit[1], size=[ksize, ksize])

        # Generate mesh grid centered at zero.
        ax = np.arange(-ksize // 2 + 1.0, ksize // 2 + 1.0)
        # Shape (ksize, ksize, 2)
        grid = np.stack(np.meshgrid(ax, ax), axis=-1)

        # Calculate rotated sigma matrix
        d_matrix = np.array([[sigmaX**2, 0], [0, sigmaY**2]])
        u_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        sigma_matrix = np.dot(u_matrix, np.dot(d_matrix, u_matrix.T))

        inverse_sigma = np.linalg.inv(sigma_matrix)
        # Described in "Parameter Estimation For Multivariate Generalized Gaussian Distributions"
        kernel = np.exp(-0.5 * np.power(np.sum(np.dot(grid, inverse_sigma) * grid, 2), beta))
        # Add noise
        kernel = kernel * noise_matrix

        # Normalize kernel
        kernel = (kernel * 255).astype(np.uint8)

        kernel = pyvips.Image.new_from_list(kernel.tolist(), scale=np.sum(kernel))
        return {"kernel": kernel}

    def get_transform_init_args_names(self) -> tuple[str, str, str, str, str, str]:
        return (
            "blur_limit",
            "sigmaX_limit",
            "sigmaY_limit",
            "rotate_limit",
            "beta_limit",
            "noise_limit",
        )
