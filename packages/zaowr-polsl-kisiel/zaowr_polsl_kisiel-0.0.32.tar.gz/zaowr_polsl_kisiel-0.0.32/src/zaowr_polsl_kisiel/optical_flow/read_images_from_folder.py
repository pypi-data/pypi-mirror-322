import os
from glob import glob

from colorama import Fore, init as colorama_init

colorama_init(autoreset=True)

# Function to read images from a folder
def read_images_from_folder(folderPath: str) -> list[str]:
    """
    Read images from a folder and sort them alphabetically.

    :param str folderPath: The path to the folder containing the images.

    :raises FileNotFoundError: If the folder is not found.

    :raises ValueError: If the folder does not contain at least two images.

    :return: A list of image file paths sorted alphabetically.
    """
    if not os.path.isdir(folderPath):
        raise FileNotFoundError(Fore.RED + f"\nFolder '{folderPath}' not found!\n")

    imagePaths = sorted(glob(os.path.join(folderPath, "*.*")), key=os.path.basename)

    if len(imagePaths) < 2:
        raise ValueError(Fore.RED + "\nFolder must contain at least two images!\n")

    return imagePaths