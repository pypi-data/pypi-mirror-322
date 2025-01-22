import numpy as np
from colorama import Fore, Style, init as colorama_init  # , Back

colorama_init(autoreset=True)

def disparity_to_depth_map(
        disparityMap: np.ndarray,
        baseline: float,
        focalLength: float,
        doffs: float = 0.0,
        aspect: float = 1000.0
) -> np.ndarray:
    """
    Convert disparity map to depth map.

    :param np.ndarray disparityMap: Disparity map
    :param float baseline: Baseline
    :param float focalLength: Focal length
    :param float doffs: Disparity offset
    :param float aspect: Aspect ratio. Default value is 1000 which returns the depth in meters.


    :raises ValueError: Raises ValueError if:
        - **`disparityMap`** is not a numpy array
        - **`baseline`** is not a positive number
        - **`focalLength`** is not a positive number

    :raises TypeError: Raises TypeError if:
        - **`baseline`** or **`focalLength`** or **`doffs`** or **`aspect`** is not a float

    :raises RuntimeError: Raises RuntimeError if:
        - **`depthMap`** is None

    :return: Depth map as a numpy array
    """
    if disparityMap is None or not isinstance(disparityMap, np.ndarray):
        raise ValueError(Fore.RED + "\nDisparity map must be provided!\n")

    if baseline is None or baseline <= 0.0:
        raise ValueError(Fore.RED + "\nBaseline must be provided!\n")

    if focalLength is None or focalLength <= 0.0:
        raise ValueError(Fore.RED + "\nFocal length must be provided!\n")

    if not isinstance(baseline, float) or not isinstance(focalLength, float) or not isinstance(aspect, float) or not isinstance(doffs, float):
        raise TypeError(Fore.RED + "\nBaseline, focal length, doffs and aspect ratio must be floats!\n")

    # Convert disparity to depth
    disparityMap = np.float32(disparityMap)

    # Adjust disparity with offset
    validDisparity = disparityMap > 0  # Only consider valid disparity values
    adjustedDisparity = disparityMap
    depthMap = np.zeros_like(disparityMap)
    depthMap[validDisparity] = baseline * focalLength / (adjustedDisparity[validDisparity] + doffs)

    depthMap = depthMap / aspect # to meters

    if depthMap is None:
        raise RuntimeError(Fore.RED + "\nDepth map is None!\n")

    else:
        print(Fore.GREEN + "\nDisparity map successfully converted to depth map")

    return depthMap