"""
The `image_processing` module provides utilities for processing images
after camera calibration.

Functions:

- `remove_distortion`: Removes distortion from a single image using calibration parameters.

- `stereo_rectify`: Rectifies a stereo image pair after stereo calibration.

- `calculate_disparity_map`: Calculates a disparity map using different algorithms.

- `calculate_color_difference_map`: Calculates a color difference map between two images (calculated disparity map and ground truth disparity map).

- `plot_disparity_map_comparison`: Plots a comparison of disparity maps.

- `disparity_to_depth_map`: Converts a disparity map to a depth map.

- `depth_map_normalize`: Normalizes a depth map to a specified range.

- `disparity_map_normalize`: Normalizes a disparity map to a specified range (e.g. "8-bit", "16-bit", "24-bit", "32-bit". ONLY USE THE 8-BIT AND 24-BIT RANGES).

- `depth_to_disparity_map`: Converts a depth map to a disparity map.

- `decode_depth_map`: Decodes a depth map to a specified range (e.g. 8-bit, 16-bit, 24-bit. ONLY USE THE 24-BIT RANGE).

- `create_color_point_cloud`: Creates a color point cloud from disparity map, depth map and color image and limit max depth.

Usage:
    - Import this module for image distortion correction,
    - stereo rectification,
    - disparity map calculation (you can also save the disparity map and plot the comparison of different disparity maps),
    - disparity map normalization,
    - color difference map calculation,
    - convert a disparity map to a depth map and normalize it to a specified range,
    - convert a depth map to a disparity map,
    - decode a depth map to a specified range (e.g. 8-bit, 16-bit, 24-bit. ONLY USE THE 24-BIT RANGE).
"""

__all__ = [
    "remove_distortion",
    "stereo_rectify",
    "calculate_disparity_map",
    "calculate_color_difference_map",
    "plot_disparity_map_comparison",
    "disparity_to_depth_map",
    "depth_map_normalize",
    "disparity_map_normalize",
    "depth_to_disparity_map",
    "decode_depth_map",
    "create_color_point_cloud",
]

from .remove_distortion import remove_distortion # remove distortion from single image
from .stereo_rectify import stereo_rectify # rectify stereo image after stereo calibration
from .calculate_disparity_map import calculate_disparity_map, plot_disparity_map_comparison # calculate disparity map using StereoBM, StereoSGBM, and custom block matching; plot disparity map comparison
from .calculate_color_difference_map import calculate_color_difference_map # calculate color difference map
from .disparity_to_depth_map import disparity_to_depth_map # convert disparity map to depth map
from .depth_map_normalize import depth_map_normalize # normalize depth map to a specified range
from .disparity_map_normalize import disparity_map_normalize # normalize disparity map to a specified range
from .depth_to_disparity_map import depth_to_disparity_map # convert depth map to disparity map
from .decode_depth_map import decode_depth_map # decode depth map
from .create_color_point_cloud import create_color_point_cloud # create color point cloud from disparity map, depth map and color image and limit max depth