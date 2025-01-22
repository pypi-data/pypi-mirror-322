"""
The `optical_flow` module provides functions for computing optical flow using different algorithms.

Functions:

- `list_camera_ports_available`: Lists available camera ports and the ones that are working.

- `read_images_from_folder`: Reads images from a folder and sorts them alphabetically.

- `sparse_optical_flow`: Calculates sparse optical flow using Shi-Tomasi corner detection and Lucas-Kanade optical flow. Options to draw bounding boxes around moving objects are provided (DBSCAN - Density-Based Spatial Clustering of Applications with Noise).

- `dense_optical_flow`: Calculates dense optical flow using Farneback optical flow algorithm. Options to draw bounding boxes around moving objects are provided (DBSCAN - Density-Based Spatial Clustering of Applications with Noise).

Usage:
    - Use this module to perform optical flow computation.
"""

__all__ = [
    "list_camera_ports_available",
    "read_images_from_folder",
    "sparse_optical_flow",
    "dense_optical_flow",
]

from .list_camera_ports_available import list_camera_ports_available # list available camera ports and the ones that are working
from .read_images_from_folder import read_images_from_folder # read images from a folder and sort them alphabetically, returns sorted list
from .sparse_optical_flow import sparse_optical_flow  # calculate sparse optical flow with Shi-Tomasi corner detection and Lucas-Kanade optical flow
from .dense_optical_flow import dense_optical_flow  # calculate dense optical flow with Farneback optical flow algorithm