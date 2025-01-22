# RTFM - Use Cases for zaowr_polsl_kisiel and the importance of docstrings

<br/>
<br/>

<div style="font-size: 22px">

[RTFM v2 here (GitHub Pages)](https://revalew.github.io/zaowr-py-package) (auto-generated documentation with `pdoc`)

</div>

<br/>
<br/>

## Table of Contents

1. [`Docstrings`](#docstrings)
2. [`calibration` submodule](#calibration-submodule)
   - [`calibrate_camera()`](#calibrate_camera)
   - [`stereo_calibration()`](#stereo_calibration)
   - [`calculate_fov()`](#calculate_fov)
3. [`content_loaders` submodule](#content_loaders-submodule)
   - [`are_params_valid()`](#are_params_valid)
   - [`load_calibration()`](#load_calibration)
   - [`load_depth_map_calibration()`](#load_depth_map_calibration)
   - [`load_pfm_file()`](#load_pfm_file)
   - [`load_pgm_file()`](#load_pgm_file)
   - [`load_rectification_maps()`](#load_rectification_maps)
   - [`load_stereo_calibration()`](#load_stereo_calibration)
   - [`save_calibration()`](#save_calibration)
   - [`save_disparity_map()`](#save_disparity_map)
   - [`write_ply_file()`](#write_ply_file)
4. [`custom_exceptions` submodule](#custom_exceptions-submodule)
5. [`image_processing` submodule](#image_processing-submodule)
   - [`calculate_color_difference_map()`](#calculate_color_difference_map)
   - [`calculate_disparity_map()`](#calculate_disparity_map)
   - [`plot_disparity_map_comparison()`](#plot_disparity_map_comparison)
   - [`create_color_point_cloud()`](#create_color_point_cloud)
   - [`decode_depth_map()`](#decode_depth_map)
   - [`depth_map_normalize()`](#depth_map_normalize)
   - [`depth_to_disparity_map()`](#depth_to_disparity_map)
   - [`disparity_map_normalize()`](#disparity_map_normalize)
   - [`disparity_to_depth_map()`](#disparity_to_depth_map)
   - [`remove_distortion()`](#remove_distortion)
   - [`stereo_rectify()`](#stereo_rectify)
6. [`optical_flow` submodule](#optical_flow-submodule) 
   - [`dense_optical_flow()`](#dense_optical_flow)
   - [`list_camera_ports_available()`](#list_camera_ports_available)
   - [`read_images_from_folder()`](#read_images_from_folder)
   - [`sparse_optical_flow()`](#sparse_optical_flow)
7. [`tools` submodule](#tools-submodule). 
   - [`calculate_mse_disparity()`](#calculate_mse_disparity)
   - [`calculate_ssim_disparity()`](#calculate_ssim_disparity)
   - [`compare_images()`](#compare_images)
   - [`configure_qt_platform()`](#configure_qt_platform)
   - [`crop_image()`](#crop_image)
   - [`display_img_plt()`](#display_img_plt)
   - [`find_aruco_dict()`](#find_aruco_dict)
   - [`get_image_points()`](#get_image_points)
   - [`get_map_value_for_points()`](#get_map_value_for_points)
   - [`@measure_perf() decorator`](#measure_perf-decorator)

<br/>
<br/>

## Docstrings

Using Python Docstrings to Enhance Understanding

In Python, docstrings are a way to provide documentation for your functions, classes, and modules. They explain what your code does, what each parameter does, what is returned and how to use it. They are written between triple quotes (""") and are often used to explain the purpose of a function, class, or module.

<ul>
<li> In IDEs or Text Editors: Many modern Integrated Development Environments (IDEs) and text editors, such as PyCharm, Visual Studio Code, or Jupyter Notebook, allow you to hover your mouse over a function to see its description provided by the docstring. Similarly, hovering over a parameter will display information about what that parameter does (if it is described in the docstring).

</li>
<br/>
<li> In the Terminal: You can read docstrings in the terminal using the help() function, which prints the docstring to the console.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

# Display documentation for the entire module
help(zw)

# Display specific submodule's documentation
help(zw.calibration)

# Display detailed documentation for a specific function
help(zw.calibrate_camera)
```

</li>
</ul>

<br/>
<br/>

## `calibration` submodule

### `calibrate_camera()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def calibrate_camera(
    chessBoardSize: tuple[int, int],
    squareRealDimensions: float,
    calibImgDirPath: str,
    globImgExtension: str = "png",
    saveCalibrationParams: bool = False,
    calibrationParamsPath: str = "",
    displayFoundCorners: bool = False,
    displayMSE: bool = False,
    improveSubPix: bool = True,
    showListOfImagesWithChessboardFound: bool = False,
    terminationCriteria: tuple[Any, int, float] = (
        cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER,
        30,
        0.001,
    ),
    useCharuco: bool = False,
    charucoDictName: str = "DICT_6X6_250",
    markerLength: float = 20.0,
    displayIds: bool = False,
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calibrate a MONO camera.
As a result, the camera matrix, distortion coefficients, and rotation and translation vectors are saved to a JSON file, which can be used later to process images.

To properly calibrate the camera, we have to specify the number of inner corners, the real-world dimension of one side of a square, and the path to the calibration images.

Before running the function we have to check the image extensions and image paths. If the extensions are not the same, an error will be raised and the function will fail.

When we want to save the calibration parameters, we also have to specify the path to the file where we want to save them and enable the `saveCalibrationParams` parameter.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/calibration_params/calibration_params.json"

imgPath = "./ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/"

zw.calibrate_camera(
    chessBoardSize=(10, 7), # NUMBER OF INNER CORNERS
    squareRealDimensions=28.67, # mm
    calibImgDirPath=imgPath, # PATH TO CALIBRATION IMAGES
    saveCalibrationParams=True, # SAVE CALIBRATION PARAMETERS
    calibrationParamsPath=calibrationFile, # PATH TO CALIBRATION PARAMETERS
    displayFoundCorners=True, # DISPLAY FOUND CORNERS
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>


### `stereo_calibration()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def stereo_calibration(
    chessBoardSize: tuple[int, int],
    squareRealDimensions: float,
    calibImgDirPath_left: str,
    calibImgDirPath_right: str,
    globImgExtension: str = "png",
    saveCalibrationParams: bool = False,
    loadCalibrationParams: bool = False,
    calibrationParamsPath_left: str = "",
    calibrationParamsPath_right: str = "",
    saveStereoCalibrationParams: bool = False,
    stereoCalibrationParamsPath: str = "",
    displayFoundCorners: bool = False,
    displayMSE: bool = False,
    improveSubPix: bool = True,
    showListOfImagesWithChessboardFound: bool = False,
    terminationCriteria: tuple[Any, int, float] = (
        cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER,
        30,
        0.001
    ),
    stereoCalibrationFlags: Any = cv.CALIB_FIX_INTRINSIC,
    useCharuco: bool = False,
    charucoDictName: str = "DICT_6X6_250",
    markerLength: float = 20.0,
    displayIds: bool = False,
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calibrate the stereo camera. As a result, we get 3 files with stereo calibration parameters and the left and right camera calibration parameters.

To properly calibrate the stereo camera, we have to specify the number of inner corners, the real-world dimension of one side of a square, and the paths to the left and right calibration images.

Before running the function we have to check the image extensions and image paths. If the extensions are not the same, an error will be raised and the function will fail.

After calibrating the stereo camera, we can use the `are_params_valid` function to check if the new parameters are valid and exit the program if they are not.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

left_cam = "./ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam1/"
right_cam = "./ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam4/"

left_cam_params_stereo = "./tests/stereo_calibration_params/left_params.json"
right_cam_params_stereo = "./tests/stereo_calibration_params/right_params.json"
stereo_cam_params = "./tests/stereo_calibration_params/stereo_params.json"

left_valid, params_left = zw.are_params_valid(left_cam_params_stereo)
right_valid, params_right = zw.are_params_valid(right_cam_params_stereo)
stereo_valid, stereo_params = zw.are_params_valid(stereo_cam_params)

if not left_valid or not right_valid or not stereo_valid:
    # hover over function parameters to see what they do (if names are not enough...)
    zw.stereo_calibration(
        chessBoardSize=(10, 7),
        # squareRealDimensions=28.67,
        squareRealDimensions=50.0,
        calibImgDirPath_left=left_cam,
        calibImgDirPath_right=right_cam,
        globImgExtension="png",
        saveCalibrationParams=True,
        calibrationParamsPath_left=left_cam_params_stereo,
        calibrationParamsPath_right=right_cam_params_stereo,
        saveStereoCalibrationParams=True,
        stereoCalibrationParamsPath=stereo_cam_params,
        showListOfImagesWithChessboardFound=True, # Zapisz listę plików użytych do kalibracji lewej i prawej kamery.
    )

    # Revalidate parameters after calibration
    left_valid, params_left = zw.are_params_valid(left_cam_params_stereo)
    right_valid, params_right = zw.are_params_valid(right_cam_params_stereo)
    stereo_valid, stereo_params = zw.are_params_valid(stereo_cam_params)

    # Check again to ensure parameters are valid
    if not left_valid or not right_valid or not stereo_valid:
        raise RuntimeError("Calibration failed. Parameters are still invalid.")
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `calculate_fov()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def calculate_fov(cameraMatrix: np.ndarray, imageSize: tuple[float, float]) -> tuple[float, float]
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calculate the field of view (FOV) of the camera. As a result, we get the horizontal and vertical FOV.

To calculate the FOV, we have to specify the camera matrix and the image size. The image size is the size of one of the images in the calibration images. And the camera matrix can be found in the calibration parameters.

<br/>
<br/>

```python
import cv2
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/calibration_params/calibration_params.json"

imgPath = "./ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/1.png"

imgSize = cv2.cvtColor(cv2.imread(imgPath), cv2.COLOR_BGR2GRAY).shape[::-1]
# OR imgSize = cv2.imread(imgPath).shape[2:][::-1]

sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)

if sub_valid:
    fov_horizontal, fov_vertical = zw.calculate_fov(
        cameraMatrix=calibrationParams1["cameraMatrix"],
        imageSize=imgSize,
    )
    print(f"Horizontal fov: {fov_horizontal:.2f} degrees")
    print(f"Vertical fov: {fov_vertical:.2f} degrees")
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

## `content_loaders` submodule

### `are_params_valid()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def are_params_valid(path: str) -> tuple[bool, dict[str, Any] | None]
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to check if the calibration parameters are valid. If they are not valid, we can calibrate the camera and save the new parameters. If they are valid, we can skip the calibration and use them to process images quickly.

If the parameters are valid, the function returns `True` and the parameters as a `tuple[bool, dict[str, Any]]` and if they are not valid, the function returns `False` and `None`. If validation fails, an error will be raised.

This function **WILL NOT** provide type hints for the returned dictionary (as opposed to the `load_calibration`, `load_rectification_maps`, and `load_stereo_calibration` functions).

To check if the parameters are valid, we have to specify the path to the file where we saved them.

If the file does not exist, an error will be raised and the function will return `False` and `None` but the program will not exit.

After calibrating the camera, we can use the `are_params_valid` function to check if the new parameters are valid and exit the program if they are not.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/calibration_params/calibration_params.json"

imgPath = "./ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/"

sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)

if not sub_valid:
    zw.calibrate_camera(
        chessBoardSize=(10, 7),
        squareRealDimensions=28.67,
        calibImgDirPath=imgPath,
        saveCalibrationParams=True,
        calibrationParamsPath=calibrationFile,
        displayFoundCorners=False,
    )

    sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)

    if not sub_valid:
        raise RuntimeError("Calibration failed. Parameters are still invalid.")
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `load_calibration()`

[Back to the top (TOC))](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
class CalibrationParams(TypedDict):
    mse: float
    rms: float
    objPoints: np.ndarray
    imgPoints: np.ndarray
    cameraMatrix: np.ndarray
    distortionCoefficients: np.ndarray
    rotationVectors: list
    translationVectors: list


def load_calibration(calibrationParamsPath: str) -> CalibrationParams
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to load the calibration parameters from a JSON file and return them as a `dict[str, Any]`.

This function will provide type hints for the returned dictionary.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/calibration_params/calibration_params.json"

calibrationParams1 = zw.load_calibration(calibrationFile)

mse = calibrationParams1["mse"]
rms = calibrationParams1["rms"]
# ...
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `load_depth_map_calibration()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
class DepthCalibrationParams(TypedDict):
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

    
def load_dept_map_calibration(calibFile: str) -> DepthCalibrationParams
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to load the calibration parameters from a TXT file. The function returns a dictionary with the calibration parameters as a `dict[str, Any]`.

This function will provide type hints for the returned dictionary.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationParams = zw.load_depth_map_calibration("./calibration_params.txt")

print(calibrationParams["cam0"])
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `load_pfm_file()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def load_pfm_file(
        filePath: str = None
) -> tuple[np.ndarray, float]
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to load a PFM file and return it as a numpy array and a float (the image and the scale factor). We have to specify the path to the file.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

image, scale = zw.load_pfm_file("./image.pfm")
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `load_pgm_file()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def load_pgm_file(
        pgmPath: str,
        targetShape: tuple[int, int]
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to load a PGM file and return it as a numpy array. The function also resizes the image to the specified shape (usually the shape of the calculated disparity map).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

pgmPath = "./tests/disparity_maps/ground_truth.pgm"

groundTruth = zw.load_pgm_file(pgmPath, targetShape=(512, 512))
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `load_rectification_maps()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
class RectificationMaps(TypedDict):
    map1_left: np.ndarray
    map2_left: np.ndarray
    map1_right: np.ndarray
    map2_right: np.ndarray


def load_rectification_maps(rectificationMapsPath: str) -> RectificationMaps
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to load the rectification maps from a JSON file and return them as a `dict[str, Any]`.

This function will provide type hints for the returned dictionary.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

rectificationMapsFile = "./tests/rectification_maps/rectification_maps.json"

rectificationMaps = zw.load_rectification_maps(rectificationMapsFile)

map1_left = rectificationMaps["map1_left"]
map2_left = rectificationMaps["map2_left"]
# ...
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `load_stereo_calibration()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
class StereoCalibrationParams(TypedDict):
    reprojectionError: float
    fov_left: tuple[float, float]
    fov_right: tuple[float, float]
    baseline: float
    cameraMatrix_left: np.ndarray
    distortionCoefficients_left: np.ndarray
    cameraMatrix_right: np.ndarray
    distortionCoefficients_right: np.ndarray
    rotationMatrix: np.ndarray
    translationVector: np.ndarray
    essentialMatrix: np.ndarray
    fundamentalMatrix: np.ndarray


def load_stereo_calibration(calibrationParamsPath: str) -> StereoCalibrationParams
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to load the stereo calibration parameters from a JSON file and return them as a `dict[str, Any]`.

This function will provide type hints for the returned dictionary.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/stereo_calibration_params/stereo_params.json"

stereoParams = zw.load_stereo_calibration(calibrationFile)

reprojectionError = stereoParams["reprojectionError"]
fov_left = stereoParams["fov_left"]
# ...
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `save_calibration()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def save_calibration(
    calibrationParams: dict[str, list | Any], calibrationParamsPath: str
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to save the calibration parameters to a JSON file OR use it to save the dictionary to a JSON file.

If the directory in the `calibrationParamsPath` does not exist, it will be created.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/calibration_params/calibration_params.json"

calibrationParams = zw.load_calibration(calibrationFile)

zw.save_calibration(calibrationParams, calibrationFile)

# OR

distorted_params = {
    "k1": calibrationParams["distortionCoefficients"][0][0],
    "k2": calibrationParams["distortionCoefficients"][0][1],
    "p1": calibrationParams["distortionCoefficients"][0][2],
    "p2": calibrationParams["distortionCoefficients"][0][3],
    "k3": calibrationParams["distortionCoefficients"][0][4],
}

zw.save_calibration(distorted_params, "./tests/distorted_params/distorted_params.json")
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `save_disparity_map()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def save_disparity_map(
    disparityMap: np.ndarray,
    savePath: str,
    show: bool = False,
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to save a disparity map as a PNG file and optionally show it.

We can save the disparity map to a file using the `saveDisparityMap` parameter (and `saveDisparityMapPath`) directly in the function `calculate_disparity_map()` (**recommended**). 

We can also show the map using the `show` parameter with or without saving.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

disparityMap = zw.calculate_disparity_map(
    leftImagePath="./tests/disparity_maps/left.png",
    rightImagePath="./tests/disparity_maps/right.png",
)

zw.save_disparity_map(
    disparityMap=disparityMap,
    savePath="./tests/disparity_maps/disparity_map.png",
    show=True
)

#######################
# OR (RECOMMENDED)
#######################

disparityMap = zw.calculate_disparity_map(
    leftImagePath="./tests/disparity_maps/left.png",
    rightImagePath="./tests/disparity_maps/right.png",
    saveDisparityMap=True, # set saveDisparityMap to True
    saveDisparityMapPath="./tests/disparity_maps/disparity_map.png", # desired path to save
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `write_ply_file()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def write_ply_file(
        fileName: str,
        verts: np.ndarray,
        colors: np.ndarray
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to write a PLY file. We have to specify the name of the file, the vertices and the colors.

To get the vertices and colors from an image, we can use the `cv2.reprojectImageTo3D()` and `cv2.cvtColor()` functions. Then we can apply a mask to the vertices and colors to remove the points that are too far from the camera.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import cv2
import numpy as np

img = cv2.imread("./image.png", 0)
disparityMap = cv2.imread("./disparity_map.png", 0)
depthMap = cv2.imread("./depth_map.png", 0)

h, w = img.shape[:2]
f = 0.8 * w # focal length
Q = np.float32([[1, 0, 0, -0.5 * w],
                [0, -1, 0, 0.5 * h], # turn points 180 deg around x-axis,
                [0, 0, 0, -f], # so that y-axis looks up
                [0, 0, 1, 0]])

points = cv2.reprojectImageTo3D(disparityMap, Q)
colors = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
mask = depthMap < 50

outPoints = points[mask]
outColors = colors[mask]

zw.write_ply_file(
    fileName="./image.ply",
    verts=outPoints,
    colors=outColors,
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

## `custom_exceptions` submodule

This submodule contains custom exceptions used in the package. This is a good practice to have a clear and specific error message for common issues encountered while using the package. They should be caught and handled appropriately to ensure a smooth user experience.

**HOWEVER** this was not needed for this package. Later on I started using common built-in exceptions.

<br/>
<br/>

## `image_processing` submodule

### `calculate_color_difference_map()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def calculate_color_difference_map(
        disparityMap: np.ndarray,
        groundTruth: np.ndarray
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calculate the color difference map and return it as a numpy array. We have to specify the disparity map and the ground truth image. The disparity map is calculated using the `calculate_disparity_map()` function and the ground truth image is loaded using the `load_pgm_file()` function.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import os

disparityMapBM = zw.calculate_disparity_map(
            leftImagePath=img_left,
            rightImagePath=img_right,
            blockSize=9,
            numDisparities=16,
            disparityCalculationMethod="bm",
            saveDisparityMap=saveDisparityMap,
            saveDisparityMapPath=os.path.join(saveDisparityMapPath, "disparity_map_BM.png"),
            showDisparityMap=showMaps
        )
groundTruth = zw.load_pgm_file(groundTruthPath, disparityMapBM.shape)
colorDiffBM = zw.calculate_color_difference_map(disparityMapBM, groundTruth)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `calculate_disparity_map()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def calculate_disparity_map(
    leftImagePath: str,
    rightImagePath: str,
    blockSize: int = 9, # for StereoBM, StereoSGBM & Custom 2
    numDisparities: int = 16, # for StereoBM & StereoSGBM
    minDisparity: int = 0, # for StereoSGBM
    maxDisparity: int = 64, # for Custom 1 & Custom 2
    windowSize: tuple[int, int] = (11, 11), # for Custom 1
    disparityCalculationMethod: str = "bm",
    saveDisparityMap: bool = False,
    saveDisparityMapPath: str = None,
    showDisparityMap: bool = False,
    normalizeDisparityMap: bool = True,
    normalizeDisparityMapRange: str = "8-bit",
) -> np.ndarray:
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calculate the disparity map and optionally save it and/or show it. We have to specify the path to the left and right images (**already rectified images!**), the block size, the number of disparities, the minimum disparity, the maximum disparity, the window size, the disparity calculation method, the save disparity map and/or show disparity map parameters.

We can choose the disparity calculation method between StereoBM, StereoSGBM, Custom 1 and Custom 2. Depending on the disparity calculation method, we have to specify different parameters.

We can normalize the disparity map using the `normalizeDisparityMap` and `normalizeDisparityMapRange` parameters (8-bit, 16-bit, 24-bit, 32-bit). 

We can also show the map using the `showDisparityMap` parameter with or without saving.

<br/>
<br/>

```python
import os
import zaowr_polsl_kisiel as zw

disparityMapSGBM = zw.calculate_disparity_map(
            leftImagePath="left.png", # path to the left image
            rightImagePath="right.png", # path to the right image
            blockSize=9, # block size for StereoBM & StereoSGBM
            numDisparities=16, # number of disparities for StereoBM & StereoSGBM
            minDisparity=0, # minimum disparity for StereoSGBM
            disparityCalculationMethod="sgbm", # use StereoSGBM for disparity calculation
            saveDisparityMap=True, # save the disparity map
            saveDisparityMapPath=os.path.join("./tests/disparity_maps", "disparity_map_SGBM.png"), # path to save the disparity map
            showDisparityMap=True, # show the disparity map
            normalizeDisparityMap=True, # normalize the disparity map
            normalizeDisparityMapRange="8-bit", # normalize the disparity map to 8-bit
        )
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `plot_disparity_map_comparison()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def plot_disparity_map_comparison(
    disparityMapBM: np.ndarray,
    disparityMapSGBM: np.ndarray,
    disparityMapCustom: np.ndarray,
    groundTruth: np.ndarray,
    colorDiffMapBM: np.ndarray = None,
    colorDiffMapSGBM: np.ndarray = None,
    colorDiffMapCustom: np.ndarray = None,
    showComparison: bool = False,
    saveComparison: bool = False,
    savePath: str = None
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to plot the comparison of three disparity maps and the ground truth. Before plotting we have to calculate the disparity maps and the color difference maps.

We can save the comparison to a file using the `saveComparison` parameter (and `savePath`) directly in the function `plot_disparity_map_comparison()` (**recommended**).

We can also show the comparison using the `showComparison` parameter with or without saving.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import os

disparityMapBM = zw.calculate_disparity_map(...)
disparityMapSGBM = zw.calculate_disparity_map(...)
disparityMapCustom = zw.calculate_disparity_map(...)

groundTruth = zw.load_pgm_file("./ground_truth.pgm", disparityMapBM.shape)

colorDiffMapBM = zw.calculate_color_difference_map(disparityMapBM, groundTruth)
colorDiffMapSGBM = zw.calculate_color_difference_map(disparityMapSGBM, groundTruth)
colorDiffMapCustom = zw.calculate_color_difference_map(disparityMapCustom, groundTruth)

zw.plot_disparity_map_comparison(
    disparityMapBM=disparityMapBM,
    disparityMapSGBM=disparityMapSGBM,
    disparityMapCustom=disparityMapCustom,
    groundTruth=groundTruth,
    colorDiffMapBM=colorDiffMapBM,
    colorDiffMapSGBM=colorDiffMapSGBM,
    colorDiffMapCustom=colorDiffMapCustom,
    showComparison=True
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `create_color_point_cloud()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def create_color_point_cloud(
        colorImgPath: str,
        disparityMapPath: str,
        depthMapPath: str,
        focalLengthFactor: float = 0.8,
        maxDepth: float = 50.0,
) -> tuple[np.ndarray, np.ndarray]
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to load the color image, disparity map and depth map and create a point cloud. We have to specify the path to the color image, disparity map and depth map (**already rectified images!**).

We can also specify the focal length factor and the maximum depth. The focal length factor is used to calculate the focal length of the camera, and the maximum depth is used to limit the depth of the points (limit of 50 meters means that the maximum depth of the point cloud is 50 meters every point further than that will be discarded).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

outPoints, outColors = zw.create_color_point_cloud(
    colorImgPath=imgPath,
    disparityMapPath=disparityMapPath,
    depthMapPath=depthMapPath,
    focalLengthFactor=0.8,
    maxDepth=50.0)

zw.write_ply_file(
  fileName=plyPath,
  verts=outPoints,
  colors=outColors,
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `decode_depth_map()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def decode_depth_map(
        depthMap: np.ndarray,
        maxDepth: float = 1000.0,
        decodeDepthMapRange: str = "24-bit"
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to decode a depth map. We have to specify the depth map, the maximum depth and the range of the depth map to decode (e.g. **"8-bit"**, **"16-bit"**, **"24-bit"**. **ONLY USE THE 24-BIT RANGE - OTHER RANGES MAY BE INCORRECT**, check the docstring for more info).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import cv2

depthMap_uint24 = cv2.imread("./depth_map.png", cv2.IMREAD_UNCHANGED)
maxDepth = 1000.0 # meters

depthMap_decoded = zw.decode_depth_map(
    depthMap=depthMap_uint24,
    maxDepth=maxDepth,
    decodeDepthMapRange="24-bit",
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `depth_map_normalize()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def depth_map_normalize(
        depthMap: np.ndarray,
        normalizeDepthMapRange: str = "8-bit"
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

After importing the package, we can use the function to normalize a depth map. The function requires the depth map and the desired range for normalization (e.g. **"8-bit"**, **"16-bit"**, **"24-bit"**. **ONLY USE THE 8-BIT AND 24-BIT RANGES - OTHER RANGES MAY BE INCORRECT**, check the docstring for more info).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationParams = zw.load_depth_map_calibration(calibFile="./calibration_params.txt")

disparityMap, scale = zw.load_pfm_file(filePath="./disparity_map.pfm")

depthMap = zw.disparity_to_depth_map(
    disparityMap=disparityMap,
    baseline=calibrationParams["baseline"],
    focalLength=calibrationParams["focalLength"],
    aspect=1000.0
)

depthMap_8bit = zw.depth_map_normalize(
    depthMap=depthMap,
    normalizeDepthMapRange="8-bit"
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `depth_to_disparity_map()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def depth_to_disparity_map(
        depthMap: np.ndarray,
        baseline: float,
        focalLength: float,
        minDepth: float = 0.001,
        normalizeDisparityMapRange: str = "8-bit"
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

After importing the package, we can use the function to convert a depth map to a disparity map. We have to specify the depth map, the baseline and the focal length of the camera. The function returns the disparity map.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import cv2
import numpy as np

hFOV = 60
baseline = 0.1 # meters
maxDepth = 1000.0 # meters
depthMap_uint24 = cv2.imread("./depth_map.png", cv2.IMREAD_UNCHANGED) # load the 24-bit depth map
focalLength = (depthMap_uint24[0] / 2) / np.tan(np.radians(hFOV / 2))

depthMap = zw.decode_depth_map(
    depthMap=depthMap_uint24,
    maxDepth=maxDepth,
    decodeDepthMapRange="24-bit",
)

disparityMap = zw.depth_to_disparity_map(
    depthMap=depthMap,
    baseline=baseline,
    focalLength=focalLength,
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `disparity_map_normalize()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def disparity_map_normalize(
        disparityMap: np.ndarray,
        normalizeDisparityMapRange: str = "8-bit"
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

This function is used only internally by the `depth_to_disparity_map()` function to normalize the disparity map after conversion, but it can also be used to normalize a disparity map on its own if we use the `calculate_disparity_map()` function with the `normalizeDisparityMap` parameter set to `False`.

After importing the package, we can use the function to normalize the calculated disparity map to the desired range.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

disparityMapSGBM = zw.calculate_disparity_map(
    leftImagePath="./left.png",
    rightImagePath="./right.png",
    blockSize=9,
    numDisparities=256,
    minDisparity=0,
    disparityCalculationMethod="sgbm",
    normalizeDisparityMap=False,
)

disparityMap_8bit = zw.disparity_map_normalize(
    disparityMap=disparityMapSGBM,
    normalizeDisparityMapRange="8-bit", # normalize the disparity map to 8-bit range (default)
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `disparity_to_depth_map()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def disparity_to_depth_map(
        disparityMap: np.ndarray,
        baseline: float,
        focalLength: float,
        aspect: float = 1000.0
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

After importing the package, we can use the function to convert a disparity map into a depth map. The function requires the disparity map, the baseline (distance between the two cameras), the focal length, and an optional aspect ratio for scaling (default is 1000, which returns the depth in meters).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationParams = zw.load_depth_map_calibration(calibFile="./depth_calibration.txt")

disparityMap, _ = zw.load_pfm_file(filePath="./disparity_map.pfm")

depthMap = zw.disparity_to_depth_map(
    disparityMap=disparityMap,
    baseline=calibrationParams["baseline"],
    focalLength=calibrationParams["focalLength"],
    aspect=1000.0 # return depth in meters
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `disparity_to_depth_map()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def disparity_to_depth_map(
        disparityMap: np.ndarray,
        baseline: float,
        focalLength: float,
        aspect: float = 1000.0
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

After importing the package, we can use the function to convert a disparity map into a depth map. The function requires the disparity map, the baseline (distance between the two cameras), the focal length, and an optional aspect ratio for scaling (default is 1000, which returns the depth in meters).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationParams = zw.load_depth_map_calibration(calibFile="./depth_calibration.txt")

disparityMap, _ = zw.load_pfm_file(filePath="./disparity_map.pfm")

depthMap = zw.disparity_to_depth_map(
    disparityMap=disparityMap,
    baseline=calibrationParams["baseline"],
    focalLength=calibrationParams["focalLength"],
    aspect=1000.0 # return depth in meters
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `remove_distortion()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def remove_distortion(
    cameraMatrix: Any,
    distortionCoefficients: Any,
    imgToUndistortPath: str,
    showImgToUndistort: bool = False,
    showUndistortedImg: bool = False,
    saveUndistortedImg: bool = False,
    undistortedImgPath: str = "",
    undistortionMethod: str = "undistort",
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to remove distortion from an image. As a result, we get an undistorted image.

To remove distortion from an image, we have to specify the camera matrix, distortion coefficients, and the path to the image to be undistorted. The calibration params must be valid, and we can use the `are_params_valid` function to check if they are valid and load them.

If we want to save the undistorted image, we also have to specify the path to the directory where we want to save it and enable the `saveUndistortedImg` parameter. The file will be saved with the name `{original_image_name}_undistorted{original_file_extension}`. If the directory does not exist, it will be created.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

calibrationFile = "./tests/calibration_params/calibration_params.json"

imgToUndistort = "./tests/undistorted/distorted.png"

undistortedImgPath = "./tests/undistorted/"

sub_valid, calibrationParams1 = zw.are_params_valid(calibrationFile)

if sub_valid:
    zw.remove_distortion(
        cameraMatrix=calibrationParams1["cameraMatrix"],
        distortionCoefficients=calibrationParams1["distortionCoefficients"],
        imgToUndistortPath=imgToUndistort,
        saveUndistortedImg=True,
        undistortedImgPath=undistortedImgPath,
    )
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `stereo_rectify()`

[Back to the top (TOC))](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def stereo_rectify(
    calibImgDirPath_left: str,
    calibImgDirPath_right: str,
    cameraMatrix_left: np.ndarray = None,
    cameraMatrix_right: np.ndarray = None,
    distortionCoefficients_left: np.ndarray = None,
    distortionCoefficients_right: np.ndarray = None,
    R: np.ndarray = None,
    T: np.ndarray = None,
    F: np.ndarray = None,
    imgPoints_left: np.ndarray = None,
    imgPoints_right: np.ndarray = None,
    whichImage: int = 0,
    saveRectifiedImages: bool = False,
    rectifiedImagesDirPath: str = "./rectifiedImages",
    globImgExtension: str = "png",
    showRectifiedImages: bool = False,
    loadStereoCalibrationParams: bool = False,
    stereoCalibrationParamsPath: str = "",
    saveRectificationMaps: bool = False,
    loadRectificationMaps: bool = False,
    rectificationMapsPath: str = "",
    testInterpolationMethods: bool = False,
    drawEpipolarLinesParams: tuple[int, int, int] = (15, 2, 2),
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to rectify the stereo images. As a result, we get 3 files with stereo rectified images.

To properly rectify the stereo images, we have to specify the paths to the left and right calibration images, as well as the paths to the stereo, left and right calibration parameters and the path to the directory where we want to save the rectified images. If the directory for rectified images does not exist, it will be created.

Best practices are to calibrate the stereo camera first and then rectify the images. We can load the stereo calibration parameters in the main function and pass them to the `stereo_rectify` function, or we can pass the paths to the stereo calibration parameters and enable the `loadStereoCalibrationParams` parameter. 

Before running the function we have to check the image extensions and image paths. If the extensions are not the same, an error will be raised and the function will fail.

We can specify the parameters for drawing the epipolar lines - the number of lines, the thickness of the lines, and the thickness of the ROI with the `drawEpipolarLinesParams` parameter.

`whichImage` parameter is used to specify which image to rectify. By default, it is set to 0, which means that the first set of images in the `left_cam` and `right_cam` directories will be rectified. Sometimes `glob` function can change the order ot the images in the list (in my case, `0` was actually `28.png` and not `1.png`).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

left_cam = "./ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam1/"
right_cam = "./ZAOWiR Image set - Calibration/Chessboard/Stereo 2/cam4/"

left_cam_params_stereo = "./tests/stereo_calibration_params/left_params.json"
right_cam_params_stereo = "./tests/stereo_calibration_params/right_params.json"
stereo_cam_params = "./tests/stereo_calibration_params/stereo_params.json"

rectified_images_dir = "./tests/stereo_rectified_images/"

left_valid, params_left = zw.are_params_valid(left_cam_params_stereo)
right_valid, params_right = zw.are_params_valid(right_cam_params_stereo)
stereo_valid, stereo_params = zw.are_params_valid(stereo_cam_params)

if left_valid and right_valid and stereo_valid:
    zw.stereo_rectify(
        calibImgDirPath_left=left_cam,
        calibImgDirPath_right=right_cam,
        imgPoints_left=params_left["imgPoints"],
        imgPoints_right=params_right["imgPoints"],
        loadStereoCalibrationParams=True,
        stereoCalibrationParamsPath=stereo_cam_params,
        saveRectifiedImages=True,
        rectifiedImagesDirPath=rectified_images_dir,
        whichImage=0,
        drawEpipolarLinesParams=(20, 3, 2)
    )
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

## `optical_flow` submodule

### `dense_optical_flow()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def dense_optical_flow(
        source: str | int = -1,  # -1 for 1st accessible webcam
        pyr_scale: float = 0.5,
        levels: int = 3,
        winsize: int = 15,
        iterations: int = 3,
        poly_n: int = 5,
        poly_sigma: float = 1.2,
        flags: int = 0,
        drawBboxes: bool = False,
        bboxMethod: str = "threshold",
        thresholdMagnitude: float = 15.0,
        clusteringEps: float = 15.0,
        minClusterSize: int = 100,
        clusteringMethod: str = "cityblock",
        scaleFactor: float = 1.0,
        speedFilter: float = None,  # Minimal value of speed to be detected
        directionFilter: tuple[float, float] = None,  # Range of angles to be detected
        windowSize: tuple[int, int] = (1080, 720),
        windowName: str = "Dense optical flow",
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calculate dense optical flow. We have to specify the source: camera number, video path, or folder path.

The scale factor is the factor by which the image is scaled before calculating the optical flow. This can be used to reduce the size of the image, which can improve performance (important for high resolution and dense optical flow).

We can choose the parameters for the optical flow calculation and the drawing of bounding boxes. Bounding boxes are drawn only when the `drawBboxes` parameter is set to `True`. To draw bounding boxes, we have to specify the method for drawing them (**"dbscan"** - Density-Based Spatial Clustering of Applications with Noise OR **"threshold"**), default is **"threshold"** because it is faster and less resource-intensive.

We can also specify the parameters for the speed and direction filters. The speed filter is a minimal value of speed to be detected, and the direction filter is a range of angles to be detected. Values out of the range are ignored.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

videoPath = "path/to/video.mp4"
# OR
# videoPath = 0  # 0 for 1st accessible webcam
zw.dense_optical_flow(
    source=videoPath,
    levels=3,
    winsize=11,
    iterations=4,
    drawBboxes=True,
    bboxMethod="threshold",
    thresholdMagnitude=40.0,
    speedFilter=.6, # Minimal value of speed to be detected
    directionFilter=(45, 135), # Movement direction filter (values between - 45° and 135°)
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `list_camera_ports_available()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def list_camera_ports_available(
) -> tuple[list[int], list[int], list[int]]
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to list available camera ports. The function returns a tuple of three lists: available ports, working ports and non working ports. **Use the working ports to read images.**

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import os

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

availablePorts, workingPorts, nonWorkingPorts = zw.list_camera_ports_available()
# Port 0 is working and reads images (480.0 x 640.0)
# Port 2 is working and reads images (480.0 x 640.0)

cls() # Clear the console ^^^

# print(f"\nAvailable ports: {availablePorts}")
print(f"\nWorking ports: {workingPorts}") # Working ports: [0, 2]
# print(f"Non working ports: {nonWorkingPorts}")
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `read_images_from_folder()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def read_images_from_folder(
        folderPath: str
) -> list[str]
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to read images from a folder and return a list of their file paths (sorted alphabetically).

We only have to specify the path to the folder. Folder must contain only images to be read (**at least 2**).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

folderPath = "/path/to/folder/with/images"
imagePaths: list[str] = zw.read_images_from_folder(folderPath)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `sparse_optical_flow()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def sparse_optical_flow(
        source: str | int = -1,  # -1 for 1st accessible webcam
        maxCorners: int = 100,
        qualityLevel: float = 0.3,
        minDistance: int = 7,
        blockSize: int = 7,
        winSize: tuple[int, int] = (15, 15),
        maxLevel: int = 2,
        criteria: tuple[int, int, float] = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03),
        drawBboxes: bool = False,
        bboxMethod: str = "threshold",
        thresholdMagnitude: float = 15.0,
        clusteringEps: float = 40.0,
        minClusterSize: int = 3,
        clusteringMethod: str = "cityblock",
        scaleFactor: float = 1.0,
        speedFilter: float = None,  # Minimal value of speed to be detected
        directionFilter: tuple[float, float] = None,  # Range of angles to be detected
        windowSize: tuple[int, int] = (1080, 720),
        windowName: str = "Sparse optical flow",
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calculate dense optical flow. We have to specify the source: camera number, video path, or folder path.

The scale factor is the factor by which the image is scaled before calculating the optical flow. This can be used to reduce the size of the image, which can improve performance (important for high resolution and dense optical flow).

We can choose the parameters for the optical flow calculation and the drawing of bounding boxes. Bounding boxes are drawn only when the `drawBboxes` parameter is set to `True`. To draw bounding boxes, we have to specify the method for drawing them (**"dbscan"** - Density-Based Spatial Clustering of Applications with Noise OR **"threshold"**), default is **"threshold"** because it is faster and less resource-intensive.

We can also specify the parameters for the speed and direction filters. The speed filter is a minimal value of speed to be detected, and the direction filter is a range of angles to be detected. Values out of the range are ignored.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

videoPath = "path/to/video.mp4"
# OR
# videoPath = 0  # 0 for 1st accessible webcam
zw.sparse_optical_flow(
    source=videoPath,
    maxCorners=300,
    qualityLevel=0.1,
    minDistance=7,
    blockSize=5,
    winSize=(15, 15),
    maxLevel=2,
    drawBboxes=True,
    bboxMethod="threshold",
    thresholdMagnitude=1,
    speedFilter=2, # Minimal value of speed to be detected
    directionFilter=(-45, 45), # Movement direction filter (values between - -45° and 45°)
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

## `tools` submodule

### `calculate_mse_disparity()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def calculate_mse_disparity(
        map1: np.ndarray,
        map2: np.ndarray
) -> float
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calculate the **Mean Squared Error (MSE)** of two disparity maps and return it as a float. We have to specify the two disparity maps to compare - the ground truth and the calculated disparity map. Images are cropped before calculating the MSE.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import os

disparityMapBM = zw.calculate_disparity_map(
            leftImagePath=img_left,
            rightImagePath=img_right,
            blockSize=9,
            numDisparities=16,
            disparityCalculationMethod="bm",
            saveDisparityMap=saveDisparityMap,
            saveDisparityMapPath=os.path.join(saveDisparityMapPath, "disparity_map_BM.png"),
            showDisparityMap=showMaps
        )
groundTruth = zw.load_pgm_file("./tests/disparity_maps/ground_truth.pgm", disparityMapBM.shape)

groundTruth = zw.crop_image(groundTruth, cropPercentage=0.75)
disparityMapBM = zw.crop_image(disparityMapBM, cropPercentage=0.75)

mseBM = zw.calculate_mse_disparity(disparityMapBM, groundTruth)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `calculate_ssim_disparity()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def calculate_ssim_disparity(
        map1: np.ndarray,
        map2: np.ndarray
) -> float
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to calculate the **Structural Similarity Index (SSIM)** of two disparity maps and return it as a float. We have to specify the two disparity maps to compare - the ground truth and the calculated disparity map. Images are cropped before calculating the SSIM.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import os

disparityMapBM = zw.calculate_disparity_map(
            leftImagePath=img_left,
            rightImagePath=img_right,
            blockSize=9,
            numDisparities=16,
            disparityCalculationMethod="bm",
            saveDisparityMap=saveDisparityMap,
            saveDisparityMapPath=os.path.join(saveDisparityMapPath, "disparity_map_BM.png"),
            showDisparityMap=showMaps
        )
groundTruth = zw.load_pgm_file("./tests/disparity_maps/ground_truth.pgm", disparityMapBM.shape)

groundTruth = zw.crop_image(groundTruth, cropPercentage=0.75)
disparityMapBM = zw.crop_image(disparityMapBM, cropPercentage=0.75)

ssimBM = zw.calculate_ssim_disparity(disparityMapBM, groundTruth)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `compare_images()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
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
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package, we can use the function to compare multiple images. The function accepts a list of images, their corresponding colormaps, and titles. You can also specify the number of rows and columns for the layout. Optionally, the resulting comparison can be saved to a file.

The function displays the images using Matplotlib and plots them in a grid layout. If `nrows` and `ncols` are not provided, the grid layout will be determined automatically based on the number of images (1 row and `n` columns, where `n` is the number of images).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import cv2

# Load multiple images (e.g., disparity maps or depth maps)
disparityMap1, _ = cv2.imread("./disparity_map1.png", cv2.IMREAD_GRAYSCALE)
disparityMap2, _ = cv2.imread("./disparity_map2.png", cv2.IMREAD_GRAYSCALE)
disparityMap3, _ = cv2.imread("./disparity_map3.png", cv2.IMREAD_GRAYSCALE)
disparityMap4, _ = cv2.imread("./disparity_map4.png", cv2.IMREAD_GRAYSCALE)

# Prepare the images and their corresponding colormaps
images = [disparityMap1, disparityMap2, disparityMap3, disparityMap4]
cmaps = ['gray', 'hot', 'viridis', 'plasma']  # Different colormaps for each image
titles = ['Disparity Map 1', 'Disparity Map 2', 'Disparity Map 3', 'Disparity Map 4']

# Display and compare the images using a grid layout
zw.compare_images(
    images=images,
    cmaps=cmaps,
    pltLabel='Comparison of Disparity and Depth Maps',
    titles=titles,
    nrows=2,  # 2 rows in the grid
    ncols=2,  # 2 columns in the grid
    show=True,  # Display the plot
    save=True,  # Save the plot to a file
    savePath='./output/comparison_plot.png'  # File path for saving
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `configure_qt_platform()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def configure_qt_platform(
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to configure the Qt platform. This function sets the `QT_QPA_PLATFORM` environment variable to 'xcb' on Linux. It suppresses warnings about Wayland plugins.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

zw.configure_qt_platform()
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `crop_image()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def crop_image(
        img: np.ndarray,
        cropPercentage: float = 0.75
) -> np.ndarray
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to crop an image and return it as a numpy array. We have to specify the image and the percentage of the image to crop.

Image is cropped from the top, bottom, left and right to retain only a certain percentage of the original image (75% by default).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import os

groundTruth = zw.load_pgm_file("./tests/disparity_maps/ground_truth.pgm")
groundTruth = zw.crop_image(groundTruth, cropPercentage=0.75)

# AND

disparityMapBM = zw.calculate_disparity_map(
            leftImagePath=img_left,
            rightImagePath=img_right,
            blockSize=9,
            numDisparities=16,
            disparityCalculationMethod="bm",
            saveDisparityMap=saveDisparityMap,
            saveDisparityMapPath=os.path.join(saveDisparityMapPath, "disparity_map_BM.png"),
            showDisparityMap=showMaps
        )
disparityMapBM = zw.crop_image(disparityMapBM, cropPercentage=0.75)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `display_img_plt()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def display_img_plt(
        img: np.ndarray,
        pltLabel: str = 'Map',
        show: bool = False,
        save: bool = False,
        savePath: str = None,
        cmap: str = 'gray'
) -> None
```

</li>
<br/>
<li> Example usage

After importing the package, we can use the function to display an image using Matplotlib. The function requires the image and an optional plot label.

If the `show` parameter is set to `True`, the image will be displayed in a new window.

It can also save the image to a file if a `savePath` is provided and the `save` parameter is set to `True`.

You can also specify a custom color map using the `cmap` parameter (default is `'gray'`).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

disparityMap, _ = zw.load_pfm_file(filePath="./disparity_map.pfm")

zw.display_img_plt(
    img=disparityMap,
    pltLabel="Disparity map (Ground Truth PFM)",
    show=True,
    save=True,
    savePath="./disparity_map.png",
    cmap=None
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `find_aruco_dict()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def find_aruco_dict(imgPath) -> None
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to find the aruco dictionary used by the calibration board. 

This function will print the dictionary names and the number of markers found in that dictionary to the console.

e.g.
    "[INFO] detected 4 markers for '4X4_50'"
    "[INFO] detected 44 markers for '6X6_50'"
    "[INFO] detected 44 markers for '6X6_100'"
    "[INFO] detected 44 markers for '6X6_250'"
    "[INFO] detected 44 markers for '6X6_1000'"

We should choose the dictionary with the highest number of markers found and lowest number of IDs in that dictionary - "6X6_100" means that the ArUco markers are 6x6 and have 100 IDs. Each charuco board should come with detailed information about the size, square size, marker size and the dictionary type [e.g. here](../tests/charuco_tests/charuco_details.jpg).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

imgPath = "./ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/1.png"

zw.find_aruco_dict(imgPath)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `get_image_points()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def get_image_points(
        imgPath: str = None,
        windowSize: tuple[int, int] = (1080, 720),
        windowNameCustom: str = "Image",
) -> list[tuple[int, int]]
```

</li>
<br/>
<li> Example usage

After importing the package we can use the function to get the image points (pixel coordinates). When the image opens, we can click with the mouse on the image to get the points. After choosing the points, confirm with `ANY` key on the keyboard. The image points are returned as a list of tuples `(x, y)`. We have to specify the path to the image.

When the image is too big, we can specify the window size and the window name.

We can use the function to get the image points and then use them to get the map values - depth or disparity for that particular point.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import cv2

inputInfoPath = "info.png"
depthMap = cv2.imread("depth_map.png", 0)

points = zw.get_image_points(imgPath=inputInfoPath)
print(f"{points = }") # points = [(x1, y1), (x2, y2), ...]

# Use the points to get the depth values
results = zw.get_map_value_for_points(
      imgPoints=points,
      mapPoints=depthMap,
      mapType="depth"
)
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `get_map_value_for_points()`

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Function definition

<br/>
<br/>

```python
def get_map_value_for_points(
        imgPoints: np.ndarray,
        mapPoints: np.ndarray,
        mapType: str = "disparity"
) -> list[tuple[str, int, int, np.ndarray]]
```

</li>
<br/>
<li> Example usage

After importing the package, we can use the function to get the map values for the image points. We have to specify the image points, the map points and the map type. The map type can be either **"disparity"** or **"depth"**. The function returns a list of tuples `(pointIndex, x, y, depthOrDisparityValue)`. Value for each point is printed to the console.

Input image points can be a set manually or obtained with the `get_image_points()` function.

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
import cv2

inputInfoPath = "info.png"
depthMap = cv2.imread("depth_map.png", 0)
disparityMap = cv2.imread("disparity_map.png", 0)

# Get the image points with the mouse
points = zw.get_image_points(imgPath=inputInfoPath)

# Specify the points manually
points = [(804, 474), (1630, 273), (343, 171)]
print(f"{points = }") # points = [(x1, y1), (x2, y2), ...]

# Use the points to get the depth values
results = zw.get_map_value_for_points(
      imgPoints=points,
      mapPoints=depthMap,
      mapType="depth"
)
# (P1) X, Y = [804, 474]
# depth P1 = 21.88 m

# (P2) X, Y = [1630, 273]
# depth P2 = 8.00 m

# (P3) X, Y = [343, 171]
# depth P3 = 56.01 m

# Use the points to get the disparity values
results = zw.get_map_value_for_points(
      imgPoints=points,
      mapPoints=disparityMap,
      mapType="disparity"
)
# (P1) X, Y = [804, 474]
# disparity P1 = 12.00 px

# (P2) X, Y = [1630, 273]
# disparity P2 = 37.00 px

# (P3) X, Y = [343, 171]
# disparity P3 = 0.00 px

print(f"{results = }") # results = [(pointIndex, x, y, depthOrDisparityValue), ...]
```

<br/>
</li>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>
<br/>
<br/>

### `@measure_perf()` decorator

[Back to the top (TOC)](#table-of-contents)

<ol>
<li> Example usage

After importing the package we can use the `@measure_perf()` decorator to measure the performance of a function. The decorator will print the function name and the time it takes to run.

We can also save the results to a file using the `output_file` parameter (`@measure_perf(output_file="perf_results.txt")`).

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw

@zw.measure_perf()
def my_function():
    pass

my_function()
```

```python
import zaowr_polsl_kisiel as zw

@zw.measure_perf("./perf_results.txt")
def my_function():
    pass

my_function()
```

</li>
<br/>
<li> Other params are optional and have default values. Each of them can be found in the function definition, and their descriptions are provided in the docstrings (hover over the function name).

</li>
</ol>

<br/>
<br/>