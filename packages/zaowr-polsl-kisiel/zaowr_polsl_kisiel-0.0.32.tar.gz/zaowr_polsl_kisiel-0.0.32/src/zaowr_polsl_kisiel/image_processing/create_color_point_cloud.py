import os

import cv2
import numpy as np
from colorama import Fore, init as colorama_init

colorama_init(autoreset=True)

def create_color_point_cloud(
        colorImgPath: str,
        disparityMapPath: str,
        depthMapPath: str,
        focalLengthFactor: float = 0.8,
        maxDepth: float = 50.0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Create a color point cloud from a color image, disparity map, and depth map. The point cloud is limited to a maximum depth.

    :param str colorImgPath: The path to the color image.
    :param str disparityMapPath: The path to the disparity map.
    :param str depthMapPath: The path to the depth map.
    :param float focalLengthFactor: The focal length factor. Default is 0.8.
    :param float maxDepth: The maximum depth. Default is 50.0.

    :raises ValueError: Raises ValueError if:
        - **`colorImgPath`** or **`disparityMapPath`** or **`depthMapPath`** is None.
        - **`focalLengthFactor`** or **`maxDepth`** is not positive.

    :raises FileNotFoundError: Raises FileNotFoundError if:
        - **`colorImgPath`** or **`disparityMapPath`** or **`depthMapPath`** does not exist.
        - **`colorImgPath`** or **`disparityMapPath`** or **`depthMapPath`** is not a file.

    :raises TypeError: Raises TypeError if:
        - **`colorImgPath`** or **`disparityMapPath`** or **`depthMapPath`** is not a string.
        - **`focalLengthFactor`** or **`maxDepth`** is not a float.

    :raises IOError: Raises IOError if:
        - **`colorImgPath`** or **`disparityMapPath`** or **`depthMapPath`** could not be loaded.

    :raises RuntimeError: Raises RuntimeError if:
        - **`pointCloud`** or **`colors`** is None.


    :return: A tuple containing the point cloud and its corresponding colors.
    """
    if colorImgPath is None or disparityMapPath is None or depthMapPath is None:
        raise ValueError(Fore.RED + "\nColor image, disparity map and depth map paths must be specified!\n")

    if not isinstance(colorImgPath, str) or not isinstance(disparityMapPath, str) or not isinstance(depthMapPath, str):
        raise TypeError(Fore.RED + "\nColor image, disparity map and depth map paths must be strings!\n")

    if not os.path.exists(colorImgPath) or not os.path.exists(disparityMapPath) or not os.path.exists(depthMapPath) or not os.path.isfile(colorImgPath) or not os.path.isfile(disparityMapPath) or not os.path.isfile(depthMapPath):
        raise FileNotFoundError(Fore.RED + "\nColor image, disparity map and depth map paths must exist!\n")

    if not isinstance(focalLengthFactor, float) or not isinstance(maxDepth, float):
        raise TypeError(Fore.RED + "\nFocal length factor and max depth must be floats!\n")

    if focalLengthFactor <= 0 or maxDepth <= 0:
        raise ValueError(Fore.RED + "\nFocal length factor and max depth must be positive!\n")

    img = cv2.imread(colorImgPath, cv2.IMREAD_COLOR)
    disparityMap = cv2.imread(disparityMapPath, cv2.IMREAD_GRAYSCALE)
    depthMap = cv2.imread(depthMapPath, cv2.IMREAD_GRAYSCALE)

    if img is None or disparityMap is None or depthMap is None:
        raise IOError(Fore.RED + "\nColor image, disparity map and depth map could not be loaded!\n")

    h, w = depthMap.shape[:2]
    if img.shape[:2] != (h, w):
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)

    if disparityMap.shape[:2] != (h, w):
        disparityMap = cv2.resize(
            disparityMap, (w, h), interpolation=cv2.INTER_AREA
        )

    f = focalLengthFactor * w  # focal length
    Q = np.float32(
        [
            [1, 0, 0, -0.5 * w],
            [0, -1, 0, 0.5 * h],  # turn points 180 deg around x-axis,
            [0, 0, 0, -f],  # so that y-axis looks up
            [0, 0, 1, 0],
        ]
    )

    points = cv2.reprojectImageTo3D(disparityMap, Q)
    colors = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mask = depthMap < maxDepth

    outPoints = points[mask]
    outColors = colors[mask]

    if outPoints.size == 0 or outColors.size == 0:
        raise RuntimeError(Fore.RED + "\nNo points found!\n")

    return outPoints, outColors