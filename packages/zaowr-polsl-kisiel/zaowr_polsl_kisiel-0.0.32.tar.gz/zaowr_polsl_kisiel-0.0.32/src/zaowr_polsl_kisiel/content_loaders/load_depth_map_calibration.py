from __future__ import annotations
import os
from typing import TYPE_CHECKING, TypedDict, Any
from ..custom_exceptions.exceptions import CalibrationParamsWrongFormat
from colorama import Fore, Style, init as colorama_init  # , Back

colorama_init(autoreset=True)

# To avoid creating a class at runtime, for type-hinting alone.
if TYPE_CHECKING:
    # Map the `dict` fields here
    class DepthCalibrationParams(TypedDict):
        """
        A dictionary containing parsed calibration data, including focal length.

        Keys:
            - **cam0** (list[list[float]]): Camera 0 calibration data.
            - **cam1** (list[list[float]]): Camera 1 calibration data.
            - **doffs** (float): Disparity offset.
            - **baseline** (float): Baseline.
            - **dyavg** (float): Disparity range average.
            - **dymax** (float): Disparity range maximum.
            - **vmin** (float): Disparity range minimum.
            - **vmax** (float): Disparity range maximum.
            - **width** (int): Image width.
            - **height** (int): Image height.
            - **ndisp** (int): Number of disparities.
            - **isint** (int): Integer flag.
            - **focalLength** (float): Focal length.
        """
        cam0: list[list[float]]
        cam1: list[list[float]]
        doffs: float
        baseline: float
        dyavg: float
        dymax: float
        vmin: float
        vmax: float
        width: int
        height: int
        ndisp: int
        isint: int
        focalLength: float

def load_depth_map_calibration(
        calibFile: str
) -> DepthCalibrationParams:
    """
    Load depth map calibration data from a calibration file.

    :param str calibFile: Path to the calibration file.

    :raises FileNotFoundError: If the calibration file is not found.

    :raises ValueError: Raises ValueError if:
        - **`calibFile`** is not a file,
        - **`calibFile`** is not a string or is an empty string,
        - **`calibFile`** is empty,

    :raises IOError: Raises IOError if:
        - **`calibFile`** could not be read.

    :raises CalibrationParamsWrongFormat: Raises an error if the calibration file is not in the correct format or parameters are empty.

    :return: A dictionary containing parsed calibration data, including focal length.
    """
    if not os.path.exists(calibFile):
        raise FileNotFoundError(Fore.RED + f"\nCalibration file not found: {calibFile}\n")

    if not os.path.isfile(calibFile):
        raise ValueError(Fore.RED + f"\nCalibration file is not a file: {calibFile}\n")

    if calibFile is None or not isinstance(calibFile, str) or len(calibFile) == 0:
        raise ValueError(Fore.RED + "\n`calibFile` must be a non-empty string!\n")

    with open(calibFile, "r") as f:
        lines = f.readlines()

    if len(lines) == 0:
        raise ValueError(Fore.RED + f"\nCalibration file is empty: {calibFile}\n")

    if lines is None:
        raise IOError(Fore.RED + f"\nUnable to read calibration file!\n{calibFile} is not a valid file\n")

    # Parse the calibration data
    calibrationData = {}
    for line in lines:
        key, value = line.strip().split("=")
        key = key.strip()
        value = value.strip()

        if key.startswith("cam"):  # cam0 or cam1
            rows = value.strip("[]").split(";")
            calibrationData[key] = [
                [float(x) for x in row.split()] for row in rows
            ]
        elif key in {"doffs", "baseline", "dyavg", "dymax", "vmin", "vmax"}:
            calibrationData[key] = float(value)  # Float values
        elif key in {"width", "height", "ndisp", "isint"}:
            calibrationData[key] = int(value)  # Integer values
        else:
            calibrationData[key] = value  # Fallback for unexpected keys

    # Calculate focalLength from cam0
    if "cam0" in calibrationData:
        cam0FirstRow = calibrationData["cam0"][0]
        focalLength = cam0FirstRow[0]  # Extract the first element of the first row
        calibrationData["focalLength"] = focalLength
    else:
        raise CalibrationParamsWrongFormat(Fore.RED + "\n`cam0` is missing or invalid in the calibration file.\n")

    # Validation
    try:
        if not isinstance(calibrationData["doffs"], float):
            raise CalibrationParamsWrongFormat(Fore.RED + "\n`doffs` must be a float.\n")

        if not isinstance(calibrationData["baseline"], float):
            raise CalibrationParamsWrongFormat(Fore.RED + "\n`baseline` must be a float.\n")

        if not isinstance(calibrationData["width"], int) or calibrationData["width"] <= 0:
            raise CalibrationParamsWrongFormat(Fore.RED + "\n`width` must be a positive integer.\n")

        if not isinstance(calibrationData["height"], int) or calibrationData["height"] <= 0:
            raise CalibrationParamsWrongFormat(Fore.RED + "\n`height` must be a positive integer.\n")

        if not isinstance(calibrationData["cam0"], list) or not calibrationData["cam0"]:
            raise CalibrationParamsWrongFormat(Fore.RED + "\n`cam0` must be a non-empty list.\n")

        if not isinstance(calibrationData["cam1"], list) or not calibrationData["cam1"]:
            raise CalibrationParamsWrongFormat(Fore.RED + "\n`cam1` must be a non-empty list.\n")

    except KeyError as e:
        raise CalibrationParamsWrongFormat(Fore.RED + f"\nMissing key in calibration data: {e}\n")

    print(Fore.GREEN + "\nCalibration parameters loaded successfully")

    return calibrationData  # Type-hinted as DepthCalibrationParams