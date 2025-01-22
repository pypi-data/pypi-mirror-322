import os
import numpy as np
from colorama import Fore, init as colorama_init  # , Back

colorama_init(autoreset=True)

def write_ply_file(
        fileName: str,
        verts: np.ndarray,
        colors: np.ndarray
) -> None:
    """
    Write a point cloud to a PLY file. The point cloud is represented by a list of vertices and a list of colors. The PLY file is saved in ASCII format. If the directory does not exist, it will be created.

    :param str fileName: Name of the PLY file.
    :param np.ndarray verts: Vertices of the point cloud.
    :param np.ndarray colors: Colors of the vertices.

    :raises ValueError: Raises ValueError if:
        - **`fileName`** is not a string or is an empty string,
        - **`verts`** or **`colors`** is not a numpy array
    :raises TypeError: Raises TypeError if:
        - **`fileName`** is not a string or is an empty string,
        - **`verts`** or **`colors`** is not a numpy array

    :return: None
    """
    if verts is None or colors is None:
        raise ValueError(Fore.RED + "\nVertices and colors must be provided!\n")

    if not isinstance(verts, np.ndarray) or not isinstance(colors, np.ndarray):
        raise TypeError(Fore.RED + "\nVertices and colors must be numpy arrays!\n")

    if fileName is None or not isinstance(fileName, str) or len(fileName) == 0:
        raise ValueError(Fore.RED + "\n`fileName` must be an non-empty string!\n")

    # Ensure the directory exists
    directory = os.path.dirname(fileName)
    if not os.path.exists(directory):
        os.makedirs(directory)

    ply_header = '''ply
    format ascii 1.0
    element vertex %(vert_num)d
    property float x
    property float y
    property float z
    property uchar red
    property uchar green
    property uchar blue
    end_header
    '''

    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fileName, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')

    print(Fore.GREEN + f"\nPoint cloud saved to {fileName}")