import numpy as np
import cv2 as cv
from colorama import Fore, Style, init as colorama_init  # , Back

colorama_init(autoreset=True)


def disparity_map_normalize(
        disparityMap: np.ndarray,
        normalizeDisparityMapRange: str = "8-bit"
) -> np.ndarray:
    """
    Normalize disparity map to a specified range.

    :param np.ndarray disparityMap: Disparity map
    :param str normalizeDisparityMapRange: Range to normalize disparity map to (e.g. "8-bit", "16-bit", "24-bit", "32-bit")

    :raises ValueError: Raises ValueError if:
        - **`disparityMap`** is not a numpy array
        - **`normalizeDisparityMapRange`** is not a string

    :raises TypeError: Raises TypeError if:
        - **`normalizeDisparityMapRange`** is not a string

    :raises RuntimeError: Raises RuntimeError if:
        - **`disparityMap`** is None

    :return: Normalized disparity map as a numpy array
    """
    if disparityMap is None or not isinstance(disparityMap, np.ndarray):
        raise ValueError(Fore.RED + "\nDisparity map must be provided!\n")

    if normalizeDisparityMapRange is None or not isinstance(normalizeDisparityMapRange, str):
        raise TypeError(Fore.RED + "\n`normalizeDisparityMapRange` must be a string!\n")

    disparityMapNormalized = None

    if normalizeDisparityMapRange == "8-bit":
        # Normalize disparity map to 8-bit grayscale (0-255)
        disparityMapNormalized = cv.normalize(disparityMap, None, 0, 255, cv.NORM_MINMAX)
        disparityMapNormalized = disparityMapNormalized.astype(np.uint8)

    elif normalizeDisparityMapRange == "16-bit":
        # Normalize disparity map to 16-bit grayscale (0-65535)
        disparityMapNormalized = cv.normalize(disparityMap, None, 0, 65535, cv.NORM_MINMAX)
        disparityMapNormalized = disparityMapNormalized.astype(np.uint16)

    elif normalizeDisparityMapRange == "24-bit":
        # Normalize disparity map to 24-bit RGB (0-255, 0-255, 0-255)
        disparityMapNormalized = cv.normalize(disparityMap, None, 0, 255, cv.NORM_MINMAX)
        disparityMapNormalized = cv.cvtColor(disparityMapNormalized, cv.COLOR_GRAY2RGB)

    elif normalizeDisparityMapRange == "32-bit":
        # Normalize disparity map to 32-bit RGB (0-255, 0-255, 0-255)
        disparityMapNormalized = cv.normalize(disparityMap, None, 0, 255, cv.NORM_MINMAX)
        disparityMapNormalized = cv.cvtColor(disparityMapNormalized, cv.COLOR_GRAY2RGB)

    else:
        raise ValueError(Fore.RED + "\nInvalid range for disparity map normalization!\n")

    if disparityMapNormalized is None:
        raise RuntimeError(Fore.RED + "\nFailed to normalize disparity map!\n")

    else:
        print(Fore.GREEN + "\nDisparity map normalized successfully")

    return disparityMapNormalized