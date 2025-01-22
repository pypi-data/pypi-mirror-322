import numpy as np
from colorama import Fore, Style, init as colorama_init  # , Back

colorama_init(autoreset=True)

def load_pfm_file(
        filePath: str = None
) -> tuple[np.ndarray, float]:
    """
    Load a PFM file and return the data and scale.

    :param str filePath: The path to the PFM file.

    :raises ValueError: Raises ValueError if:
        - **`filePath`** is not provided or is not a string.
        - **`filePath`** is not a PFM file.
        - **`filePath`** is not a valid PFM file.

    :return: tuple[np.ndarray, float] - A tuple containing the data and scale.
    """
    if not filePath or not isinstance(filePath, str):
        raise ValueError(Fore.RED + "\nFile path must be a non-empty string.\n")

    with open(filePath, "rb") as f:
        # Read the header
        header = f.readline().decode().rstrip()
        if header not in ["PF", "Pf"]:
            raise ValueError(Fore.RED + "\nNot a PFM file.\n")

        # Determine color (PF for RGB, Pf for grayscale)
        color = header == "PF"

        # Read width and height
        dims = f.readline().decode().strip()
        width, height = map(int, dims.split())

        # Read scale (endian and range)
        scale = float(f.readline().decode().strip())
        endian = "<" if scale < 0 else ">"
        scale = abs(scale)

        # Read the data
        data = np.fromfile(f, endian + "f")
        data = np.reshape(data, (height, width, 3) if color else (height, width))
        data = np.flipud(data)  # Flip vertically due to PFM format
        data = np.array(data)
        data[np.isinf(data)] = 0

        if data is None or data.size == 0 or np.isnan(data).any() or scale == 0:
            raise ValueError(Fore.RED + "\nInvalid PFM file.\n")

        else:
            print(Fore.GREEN + "\nPFM file loaded successfully")

        return data, scale