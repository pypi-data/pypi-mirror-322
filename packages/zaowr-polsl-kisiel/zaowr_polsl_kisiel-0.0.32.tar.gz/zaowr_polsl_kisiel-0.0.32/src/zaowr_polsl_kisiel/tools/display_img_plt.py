import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
from colorama import Fore, Style, init as colorama_init  # , Back

colorama_init(autoreset=True)


def display_img_plt(
        img: np.ndarray,
        pltLabel: str = 'Map',
        show: bool = False,
        save: bool = False,
        savePath: str = None,
        cmap: str = 'gray'
) -> None:
    """
    Display the image using matplotlib and optionally save it (single image) as a PNG file.

    :param np.ndarray img: The image to be displayed
    :param str pltLabel: The label for the plot
    :param bool show: If True, show the plot
    :param bool save: If True, save the plot
    :param str savePath: The path to save the plot if `save` is True
    :param str cmap: The colormap to be used for displaying the image

    :raises TypeError: Raises TypeError if:
        - **`img`** is not a numpy array
        - **`pltLabel`** is not a string
        - **`show`** is not a boolean
        - **`save`** is not a boolean
        - **`savePath`** is not a string
        - **`cmap`** is not a string

    :return: None
    """
    if not isinstance(img, np.ndarray):
        raise TypeError(Fore.RED + "\nImage must be a numpy array!\n")

    if not isinstance(pltLabel, str):
        raise TypeError(Fore.RED + "\n`pltLabel` must be a string!\n")

    if not isinstance(show, bool):
        raise TypeError(Fore.RED + "\n`show` must be a boolean!\n")

    if not isinstance(save, bool):
        raise TypeError(Fore.RED + "\n`save` must be a boolean!\n")

    if save and (savePath is None or not isinstance(savePath, str) or len(savePath) == 0):
        raise ValueError(Fore.RED + "\n`savePath` must be a non-empty string!\n")

    if cmap is not None and not isinstance(cmap, str):
        raise TypeError(Fore.RED + "\n`cmap` must be a string or None!\n")

    # Create the plot
    plt.figure(figsize=(20, 10))
    plt.imshow(img, cmap=cmap)
    plt.title(pltLabel)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    if save:
        # Create the parent directory if it does not exist
        saveDir = os.path.dirname(savePath)
        # baseName = os.path.basename(savePath)
        if saveDir and not os.path.exists(saveDir):
            os.makedirs(saveDir)
            print(Fore.BLUE + f"Directory '{saveDir}' created.")

        plt.savefig(savePath, format='png', bbox_inches='tight')
        print(Fore.GREEN + f"\nPlot successfully saved at {savePath}")

        savePathCV2 = savePath.replace(".png", "_2.png")
        cv2.imwrite(savePathCV2, img)
        print(Fore.GREEN + f"\nOpenCV RAW image successfully saved at {savePathCV2}")

    if show:
        plt.show()

    plt.close()