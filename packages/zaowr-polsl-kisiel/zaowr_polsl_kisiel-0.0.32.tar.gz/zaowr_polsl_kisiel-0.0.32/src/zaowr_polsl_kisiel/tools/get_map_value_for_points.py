import numpy as np
from colorama import Fore, init as colorama_init

colorama_init(autoreset=True)

def get_map_value_for_points(
        imgPoints: np.ndarray,
        mapPoints: np.ndarray,
        mapType: str = "disparity"
) -> list[tuple[str, int, int, np.ndarray]]:
    """
    Get the value of the map at the specified image points.

    :param np.ndarray imgPoints: The image points.
    :param np.ndarray mapPoints: The map points.
    :param str mapType: The type of map. Can be "disparity" or "depth". Default is "disparity".

    :raises TypeError: Raises TypeError if `imgPoints` or `mapPoints` is not a numpy array.

    :raises ValueError: Raises ValueError if `mapType` is not "disparity" or "depth".

    :raises RuntimeError: Raises RuntimeError if no points are found or `results` is None after the loop.

    :return: A list of tuples containing the point index, X and Y coordinates, and the map value.
    """
    results = []

    if not isinstance(imgPoints, np.ndarray):
        raise TypeError(Fore.RED + "\nImage points must be a numpy array!\n")

    if not isinstance(mapPoints, np.ndarray):
        raise TypeError(Fore.RED + "\nMap points must be a numpy array!\n")


    if mapType == "disparity":
        unit = "px"

    elif mapType == "depth":
        unit = "m"

    else:
        raise ValueError(Fore.RED + f"\nInvalid map type: {mapType}\n")


    for idx, (x, y) in enumerate(imgPoints, start=1):
        if x < 0 or x >= mapPoints.shape[1] or y < 0 or y >= mapPoints.shape[0]:
            continue

        # Rounding to the nearest integer to avoid errors when indexing the map
        if isinstance(x, float) or isinstance(y, float):
            print(Fore.YELLOW + f"\nPoint {idx} ({x}, {y}) is not an integer. Rounding to nearest integer...")
            x = round(x)
            y = round(y)
            print(Fore.YELLOW + f"Point {idx} ({x}, {y}) rounded to nearest integer.")

        value = mapPoints[y, x]
        results.append((f"P{idx}", x, y, value))
        print(Fore.GREEN + f"\n(P{idx}) X, Y = [{x}, {y}]\n{mapType} P{idx} = {value:.2f} {unit}")

    if len(results) == 0 or results is None:
        raise RuntimeError(Fore.RED + "\nNo points found!\n")

    return results