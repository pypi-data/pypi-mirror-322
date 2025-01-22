import os
import cv2
from colorama import Fore, init as colorama_init
from typing import Any

colorama_init(autoreset=True)

# I don't know what would be a better way to pass the name to the callback function other than a global variable (maybe a class? but I'm not using classes anywhere else...)
windowName = "Image"

# Get points form photo
def click_event(
        event: int,
        x: int,
        y: int,
        flags: int,
        param: Any | None = None
) -> None:
    """
    Callback function for mouse click events on an image.

    :param int event: The type of mouse event.
    :param int x: The x-coordinate of the mouse click.
    :param int y: The y-coordinate of the mouse click.
    :param int flags: Additional flags for the mouse event.
    :param Any | None param: Additional parameters for the mouse event.

    :return: None
    """
    global windowName  # Access the global variable

    image, points = param  # Unpack the passed parameters

    if event == cv2.EVENT_LBUTTONDOWN:
        print(Fore.GREEN + f"\nPoint clicked: ({x}, {y})")
        points.append((x, y))
        # Draw a circle on the image
        cv2.circle(image, (x, y), 5, (255, 0, 0), -1)
        cv2.imshow(windowName, image)


def get_image_points(
        imgPath: str = None,
        windowSize: tuple[int, int] = (1080, 720),
        windowNameCustom: str = "Image",
) -> list[tuple[int, int]]:
    """
    Get points (pixel coordinates) from an image using mouse click. The points are stored in a list.

    :param str imgPath: The path to the image file.
    :param tuple[int, int] windowSize: The size of the window to display the image. Default is (1080, 720).
    :param str windowNameCustom: The name of the window to display the image. Default is "Image".

    :raises ValueError: Raises ValueError if:
        - **`imgPath`** is not a string.
        - **`windowSize`** is not a tuple of two integers.
        - **`windowNameCustom`** is not a string.
        - **`points`** (output) is empty.

    :raises FileNotFoundError: Raises FileNotFoundError if:
        - **`imgPath`** is not found.
        - **`imgPath`** is not a file.

    :raises IOError: Raises IOError if:
        - **`imgPath`** could not be loaded.

    :return: A list of tuples representing the clicked points on the image.
    """
    global windowName  # Access the global variable
    windowName = windowNameCustom # Update the global variable

    points = []

    if imgPath is None or not isinstance(imgPath, str) or imgPath == "":
        raise ValueError(Fore.RED + "\nImage path must be a non-empty string.\n")

    if not os.path.exists(imgPath) or not os.path.isfile(imgPath):
        raise FileNotFoundError(Fore.RED + f"\nImage file not found: {imgPath}\n")

    if windowSize is None or not isinstance(windowSize, tuple) or len(windowSize) != 2:
        raise ValueError(Fore.RED + "\nWindow size must be a tuple of two integers.\n")

    img = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise IOError(Fore.RED + f"\nImage {imgPath} could not be loaded.\n")

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, windowSize)
    cv2.imshow(windowName, img)

    cv2.setMouseCallback(windowName, click_event, (img, points))

    print(Fore.GREEN + "\nClick on the image to get the points.\nPress any key to `CONFIRM` the points or `QUIT`.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(points) == 0:
        raise ValueError(Fore.RED + "\nNo points were clicked.\n")

    return points
