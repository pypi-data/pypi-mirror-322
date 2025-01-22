import os
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

def compare_images(
        images: list[np.ndarray],
        cmaps: list[str] = None,
        pltLabel: str = 'Comparison',
        titles: list[str] = None,
        nrows: int = None,
        ncols: int = None,
        show: bool = False,
        save: bool = False,
        savePath: str = None
) -> None:
    """
    Compare multiple images using matplotlib with configurable grid layout and colormaps.

    :param list[np.ndarray] images: List of images to be compared
    :param list[str] cmaps: List of colormaps for each image
    :param str pltLabel: The label for the plot
    :param list[str] titles: List of titles for the images
    :param int nrows: Number of rows in the plot grid
    :param int ncols: Number of columns in the plot grid
    :param bool show: If True, show the plot
    :param bool save: If True, save the plot
    :param str savePath: The path to save the plot if `save` is True

    :raises ValueError: Raises ValueError if:
        - the grid dimensions do not accommodate all images
        - **`cmaps`** and **`titles`** have different lengths than **`images`**
        - **`ncols`** and **`nrows`** cannot accommodate all images
        - **`ncols`** or **`nrows`** are smaller than 1
        - **`savePath`** is not provided

    :raises TypeError: Raises TypeError if:
        - Elements in **`images`** are not numpy arrays
        - **`cmaps`** is not a list of strings
        - **`pltLabel`** is not a string
        - **`show`** is not a boolean
        - **`save`** is not a boolean
        - **`titles`** is not a list of strings
        - **`savePath`** is not a string

    :return: None
    """
    if not isinstance(images, list) or not all(isinstance(img, np.ndarray) for img in images):
        raise TypeError(Fore.RED + "\nAll elements in `images` must be numpy arrays!\n")

    if cmaps is not None:
        if not isinstance(cmaps, list) or not all(isinstance(cmap, (str, type(None))) for cmap in cmaps):
            raise TypeError(Fore.RED + "\n`cmaps` must be a list of strings or None!\n")
        if len(cmaps) != len(images):
            raise ValueError(Fore.RED + "\nThe number of colormaps must match the number of images!\n")
    else:
        cmaps = [None] * len(images)

    if not isinstance(pltLabel, str):
        raise TypeError(Fore.RED + "\n`pltLabel` must be a string!\n")

    if not isinstance(show, bool):
        raise TypeError(Fore.RED + "\n`show` must be a boolean!\n")

    if not isinstance(save, bool):
        raise TypeError(Fore.RED + "\n`save` must be a boolean!\n")

    if titles is not None:
        if not isinstance(titles, list) or not all(isinstance(title, str) for title in titles):
            raise TypeError(Fore.RED + "\n`titles` must be a list of strings!\n")
        if len(titles) != len(images):
            raise ValueError(Fore.RED + "\nThe number of titles must match the number of images!\n")
    else:
        titles = [f'Image {i + 1}' for i in range(len(images))]

    # Determine grid dimensions if not provided
    num_images = len(images)
    if nrows is None and ncols is None:
        nrows = 1
        ncols = num_images
    elif nrows is None:
        nrows = (num_images + ncols - 1) // ncols
    elif ncols is None:
        ncols = (num_images + nrows - 1) // nrows

    if nrows * ncols < num_images:
        raise ValueError(Fore.RED + "\nThe grid dimensions do not fit all images!\n")

    if nrows < 1 or ncols < 1:
        raise ValueError(Fore.RED + "\nGrid dimensions cannot be negative or smaller than 1!\n")

    if save and (savePath is None or not isinstance(savePath, str) or len(savePath) == 0):
        raise ValueError(Fore.RED + "\n`savePath` must be a non-empty string if `save` is True!\n")

    # Create the parent directory if it does not exist
    if save and savePath:
        saveDir = os.path.dirname(savePath)
        if saveDir and not os.path.exists(saveDir):
            os.makedirs(saveDir)
            print(Fore.BLUE + f"Directory '{saveDir}' created.")

    plt.figure(figsize=(5 * ncols, 5 * nrows))

    for i, (img, cmap) in enumerate(zip(images, cmaps)):
        plt.subplot(nrows, ncols, i + 1)
        plt.imshow(img, cmap=cmap)
        plt.title(titles[i])
        plt.axis('off')

    # Adjust layout to fit everything, including the main title
    plt.tight_layout(rect=(0, 0, 1, 0.95))  # Leaves space for the main title
    # Main title
    plt.suptitle(pltLabel, fontsize=16, fontweight='bold')

    if save:
        plt.savefig(savePath, format='png', bbox_inches='tight')
        print(Fore.GREEN + f"\nPlot successfully saved at {savePath}")

    if show:
        plt.show()

    plt.close()
