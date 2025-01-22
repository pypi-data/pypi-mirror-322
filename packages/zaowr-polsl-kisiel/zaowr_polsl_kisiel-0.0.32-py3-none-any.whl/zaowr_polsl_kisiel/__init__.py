"""
This package provides tools and utilities for camera calibration, stereo calibration,
image processing, calculation of disparity/depth maps, calculation of optical flow and related operations.

Modules:

- `calibration`: Tools for single and stereo camera calibration.

- `content_loaders`: Functions to load and validate calibration data from files, load the ground truth `.pgm` or `.pfm` file,  save the disparity map, write a .ply file and load depth map calibration.

- `custom_exceptions`: Custom exceptions for error handling.

- `image_processing`: Utilities for image rectification, distortion removal, disparity map calculation, color difference map calculation, disparity map comparison, depth map conversion (disparity to depth), disparity map normalization, depth map normalization, depth map to disparity map conversion, depth map decoding, color point cloud creation.

- `optical_flow`: Tools to calculate the Optical Flow using **Sparse** (Shi-Tomasi corner detection and Lucas-Kanade optical flow) and **Dense** (Farneback optical flow) Optical Flow** algorithms. Tool to list available camera ports and the ones that are working (and can be used as a feed fot the optical flow algorithms).

- `tools`: Additional tools, such as ArUco dictionary identification, performance measurement, image cropping, image display using matplotlib, get points form photo using mouse click (pixel coordinates), get map value for points (e.g. disparity, depth).

Status: Development

Year of development: 2024/2025

Author: Maksymilian Kisiel

Institution: Silesian University of Technology

Faculty: Faculty of Automatic Control, Electronics and Computer Science

Major: Informatics, master degree

Specialization: Interactive Three-Dimensional Graphics (IGT, pol. Interaktywna Grafika Trójwymiarowa, https://www.polsl.pl/rau6/en/igt-specjalization/)
"""

__version__ = "0.0.32"
__status__ = "Development"  # Allowed: "Prototype", "Beta", "Stable"

__all__ = [
    "calibration",
    "content_loaders",
    "exceptions",
    "image_processing",
    "optical_flow",
    "tools",
]

# IMPORT SUBMODULES
from . import calibration
from .calibration import (
    calibrate_camera, # calibrate single camera
    stereo_calibration, # stereo calibration
    calculate_fov, # calculate fov - horizontal and vertical
)

from . import custom_exceptions
from .custom_exceptions import exceptions # custom_exceptions

from . import content_loaders
from .content_loaders import (
    are_params_valid, # validate calibration parameters stored in files and return them if valid
    save_calibration, # save calibration parameters (used for all types of params - single, stereo, rectification, etc.)
    load_calibration, # load calibration parameters for single camera
    load_stereo_calibration, # load stereo calibration
    load_rectification_maps, # load rectification maps
    save_disparity_map, # save disparity map
    load_pgm_file, # load the ground truth .pgm file
    load_pfm_file, # load the ground truth .pfm file
    write_ply_file, # write .ply file
    load_depth_map_calibration, # load depth map calibration
)

from . import image_processing
from .image_processing import (
    remove_distortion, # remove distortion from single image
    stereo_rectify, # rectify stereo image after stereo calibration
    calculate_disparity_map, # calculate disparity map using StereoBM, StereoSGBM, Custom Block Matching
    calculate_color_difference_map, # calculate color difference map
    plot_disparity_map_comparison, # plot disparity map comparison
    disparity_to_depth_map, # convert disparity map to depth map
    disparity_map_normalize, # normalize disparity map to a specified range
    depth_map_normalize, # normalize depth map to a specified range
    depth_to_disparity_map, # convert depth map to disparity map
    decode_depth_map, # decode depth map
    create_color_point_cloud, # create color point cloud with specified max depth
)

from . import optical_flow
from .optical_flow import (
    list_camera_ports_available, # list available camera ports and the ones that are working
    read_images_from_folder, # read images from a folder and sort them alphabetically
    sparse_optical_flow, # calculate sparse optical flow with Shi-Tomasi corner detection and Lucas-Kanade optical flow
    dense_optical_flow, # calculate dense optical flow with Farneback optical flow algorithm
)

from . import tools
from .tools import (
    find_aruco_dict, # find aruco dictionary if we don't know
    measure_perf, # measure performance
    calculate_mse_disparity, # calculate MSE between two disparity maps
    calculate_ssim_disparity, # calculate SSIM between two disparity maps
    crop_image, # crop image to retain only the center part (specified by percentage)
    display_img_plt, # display the image using matplotlib
    compare_images, # compare multiple images
    get_image_points, # get points form photo using mouse click (pixel coordinates)
    get_map_value_for_points, # get map value for points (e.g. disparity, depth)
    configure_qt_platform, # configure the `QT_QPA_PLATFORM` environment variable to 'xcb' on Linux (suppress warnings about Wayland plugins)
)