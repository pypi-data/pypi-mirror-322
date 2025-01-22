import numpy as np
from .disparity_map_normalize import disparity_map_normalize
from colorama import Fore, Style, init as colorama_init  # , Back

colorama_init(autoreset=True)

def depth_to_disparity_map(
        depthMap: np.ndarray,
        baseline: float,
        focalLength: float,
        minDepth: float = 0.001,
        normalizeDisparityMapRange: str = "8-bit"
) -> np.ndarray:
    """
    Convert depth map to disparity map.

    :param np.ndarray depthMap: Depth map
    :param float baseline: Baseline
    :param float focalLength: Focal length
    :param float minDepth: Minimum depth
    :param str normalizeDisparityMapRange: Range to normalize disparity map to (e.g. "8-bit", "16-bit", "24-bit", "32-bit")

    :raises ValueError: Raises ValueError if:
        - **`depthMap`** is not a numpy array
        - **`baseline`** is not a positive number
        - **`focalLength`** is not a positive number
        - **`minDepth`** is not a positive number

    :raises TypeError: Raises TypeError if:
        - **`baseline`** or **`focalLength`** or **`minDepth`** are not floats or **`normalizeDisparityMapRange`** is not a string

    :raises RuntimeError: Raises RuntimeError if:
        - **`disparityMapNormalized`** is None

    :return: Disparity map as a numpy array
    """
    if normalizeDisparityMapRange is None or not isinstance(normalizeDisparityMapRange, str):
        raise TypeError(Fore.RED + "\n`normalizeDisparityMapRange` must be a string!\n")

    if not isinstance(baseline, float) or not isinstance(focalLength, float) or not isinstance(minDepth, float):
        raise TypeError(Fore.RED + "\n`baseline`, `focalLength` and `minDepth` must be floats!\n")

    if normalizeDisparityMapRange not in ["8-bit", "16-bit", "24-bit", "32-bit"]:
        raise ValueError(Fore.RED + "\n`normalizeDisparityMapRange` must be one of the following: 8-bit, 16-bit, 24-bit or 32-bit!\n")

    if depthMap is None or not isinstance(depthMap, np.ndarray):
        raise ValueError(Fore.RED + "\nDepth map must be provided as a numpy array!\n")

    if baseline is None or baseline <= 0.0:
        raise ValueError(Fore.RED + "\nBaseline must be provided as a positive number!\n")

    if focalLength is None or focalLength <= 0.0:
        raise ValueError(Fore.RED + "\nFocal length must be provided as a positive number!\n")

    if minDepth is None or minDepth < 0.0:
        raise ValueError(Fore.RED + "\nMinimum depth must be provided as a positive number!\n")

    # depthMap = np.nan_to_num(depthMap)
    depthMap = np.maximum(depthMap, minDepth)

    disparityMap = (baseline * focalLength) / depthMap
    disparityMapNormalized = disparity_map_normalize(disparityMap, normalizeDisparityMapRange)

    if disparityMapNormalized is None:
        raise RuntimeError(Fore.RED + "\nDisparity map could not be normalized!\n")

    else:
        print(Fore.GREEN + "\nDepth map successfully converted to disparity map")

    return disparityMapNormalized