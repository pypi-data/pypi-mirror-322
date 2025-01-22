"""
The `tools` module contains additional utilities for specific tasks.

Functions:

- `find_aruco_dict`: Identifies the ArUco dictionary used in marker detection.

- `measure_perf`: (custom decorator) Measures the performance (execution time) of a function (optionally saves results to a file).

- `calculate_mse_disparity`: Calculates the Mean Squared Error (MSE) between two disparity maps.

- `calculate_ssim_disparity`: Calculates the Structural Similarity Index (SSIM) between two disparity maps.

- `crop_image`: Crops an image to retain only the center part (specified by percentage).

- `display_img_plt`: Displays an image using matplotlib.

- `compare_images`: Compares multiple images.

- `get_image_points`: Gets points form photo using mouse click (pixel coordinates).

- `get_map_value_for_points`: Gets map value for points (e.g. disparity, depth value at a specific point).

- `configure_qt_platform`: Configures the `QT_QPA_PLATFORM` environment variable to 'xcb' on Linux (suppress warnings about Wayland plugins).

Usage:
    - Use this module for miscellaneous tools that enhance functionality.
"""

__all__ = [
    "find_aruco_dict",
    "measure_perf",
    "calculate_mse_disparity",
    "calculate_ssim_disparity",
    "crop_image",
    "display_img_plt",
    "compare_images",
    "get_image_points",
    "get_map_value_for_points",
    "configure_qt_platform",
]

from .find_aruco_dict import find_aruco_dict # find aruco dictionary if we don't know it
from .measure_perf import measure_perf # measure performance (time) of a function (custom decorator with option to save the results to a file)
from .calculate_mse_disparity import calculate_mse_disparity # calculate MSE between two disparity maps
from .calculate_ssim_disparity import calculate_ssim_disparity # calculate Structural Similarity Index (SSIM) between two disparity maps
from .crop_image import crop_image # crop image to retain only the center part (specified by percentage)
from .display_img_plt import display_img_plt # display the image using matplotlib
from .compare_images import compare_images # compare multiple images
from .get_image_points import get_image_points # get points form photo using mouse click (pixel coordinates)
from .get_map_value_for_points import get_map_value_for_points # get map value for points (e.g. disparity, depth)
from .configure_qt_platform import configure_qt_platform # configure the `QT_QPA_PLATFORM` environment variable to 'xcb' on Linux (suppress warnings about Wayland plugins)