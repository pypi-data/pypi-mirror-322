import os
from time import perf_counter
import cv2 as cv
import numpy as np
from colorama import Fore, init as colorama_init

from . import read_images_from_folder

colorama_init(autoreset=True)

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
) -> None:
    """
    Calculate dense optical flow using Farneback's algorithm. Options to draw bounding boxes around moving objects are provided (**DBSCAN - Density-Based Spatial Clustering of Applications with Noise** and **threshold**).

    :param source: The source of the video feed. Can be a camera number, video file path, or folder with images.
    :param pyr_scale: The pyramid scale factor for Farneback's algorithm.
    :param levels: The number of pyramid levels for Farneback's algorithm.
    :param winsize: The window size for Farneback's algorithm.
    :param iterations: The number of iterations for Farneback's algorithm.
    :param poly_n: The polynomial order for Farneback's algorithm.
    :param poly_sigma: The standard deviation for Farneback's algorithm.
    :param flags: The flags for Farneback's algorithm.

    :param drawBboxes: Whether to draw bounding boxes around detected corners.
    :param bboxMethod: The method for drawing bounding boxes (**"dbscan"** or **"threshold"**).

    :param thresholdMagnitude: The threshold magnitude for bounding boxes (**threshold**).

    :param clusteringEps: The epsilon value for clustering (**DBSCAN**).
    :param minClusterSize: The minimum size of a cluster (**DBSCAN**).
    :param clusteringMethod: The method for clustering (**DBSCAN**).

    :param scaleFactor: The scale factor to resize the image (for faster processing).

    :param speedFilter: The minimal value of speed to be detected.
    :param directionFilter: The range of angles to be detected.

    :param windowSize: The size of the window to display the optical flow.
    :param windowName: The name of the window to display the optical flow.

    :raises ValueError: Raises ValueError if:
        - **`source`** is None.
        - **`source`** is **NOT** an integer, a string, or a folder path.
        - **`bboxMethod`** not in ["dbscan", "threshold"].

    :raises IOError: Raises IOError if:
        - **`source`** is a video file path and the file could not be loaded.

    :return: None

    **DBSCAN clustering**:  _VALID_METRICS = [
    "euclidean",
    "l2",
    "l1",
    "manhattan",
    "cityblock",
    "braycurtis",
    "canberra",
    "chebyshev",
    "correlation",
    "cosine",
    "dice",
    "hamming",
    "jaccard",
    "mahalanobis",
    "matching",
    "minkowski",
    "rogerstanimoto",
    "russellrao",
    "seuclidean",
    "sokalsneath",
    "sqeuclidean",
    "yule",
    "wminkowski",
    "nan_euclidean",
    "haversine",]
    """

    # Determine the type of source
    if source is None:
        raise ValueError(Fore.RED + f"\nInvalid source! Provide a camera number, video file path, or folder with images ('{source}' provided)\n\n")

    elif isinstance(source, int) or (isinstance(source, str) and source.isdigit()):
        # Case: Camera feed (number)
        # The video feed is read in as a VideoCapture object
        cap = cv.VideoCapture(int(source))
        sourceType = "camera"

    elif os.path.isdir(source):
        # Case: Folder with images
        imagePaths = read_images_from_folder(source)
        cap = None
        sourceType = "images"

    elif os.path.isfile(source):
        # Case: Video file
        # The video feed is read in as a VideoCapture object
        cap = cv.VideoCapture(source)
        sourceType = "video"

    else:
        raise ValueError(Fore.RED + f"\nInvalid source! Provide a camera number, video file path, or folder with images ('{source}' provided)\n\n")

    # Parameters for Farneback optical flow
    fbParams = dict(
        pyr_scale=pyr_scale,
        levels=levels,
        winsize=winsize,
        iterations=iterations,
        poly_n=poly_n,
        poly_sigma=poly_sigma,
        flags=flags
    )

    # Initialization for different source types
    if sourceType == "images":
        oldFrame = cv.imread(imagePaths[0])
        imageIter = iter(imagePaths[1:])

    else:
        # Take first frame and find corners in it
        # ret = a boolean return value from getting the frame, oldFrame = the first frame in the entire video sequence
        ret, oldFrame = cap.read()

        if not ret:
            raise IOError(Fore.RED + f"\nUnable to read source: {source}\n")

    oldGray = cv.cvtColor(oldFrame, cv.COLOR_BGR2GRAY)

    mask = np.zeros_like(oldFrame) # HSV mask
    mask[..., 1] = 255 # Sets image saturation to maximum

    if scaleFactor != 1.0:
        oldGray = cv.resize(oldGray, None, fx=scaleFactor, fy=scaleFactor, interpolation=cv.INTER_LINEAR)

    print(Fore.GREEN + f"\nReading from source (type: '{sourceType}'): {source}")
    # print(Fore.GREEN + f"\nWindow '{windowName}' is going to be moved to the edge of the screen - (0, 0)...")
    print(Fore.GREEN + "\nPress `Esc` or `q` to exit...\nPress `s` to save current frame...")

    frameCount = 0
    frameTimes = []
    # out = cv.VideoWriter('output_dense.avi', cv.VideoWriter_fourcc(*'XVID'), 20.0, (oldGray.shape[1], oldGray.shape[0]))
    while True:
        startTime = perf_counter()

        # Read next frame or image
        if sourceType == "images":
            try:
                framePath = next(imageIter)
                frame = cv.imread(framePath)

            except StopIteration:
                print(Fore.YELLOW + "\nEnd of images in folder.")
                print(Fore.YELLOW + "Press any key to exit...")
                cv.waitKey(0)
                break

        else:
            # ret = a boolean return value from getting the frame, frame = the current frame being projected in the video
            ret, frame = cap.read()

            if not ret:
                print(Fore.YELLOW + "\nNo more frames to read.")
                print(Fore.YELLOW + "Press any key to exit...")
                cv.waitKey(0)
                break

        # Convert frame to grayscale for easier calculations
        frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        if scaleFactor != 1.0:
            frameGray = cv.resize(frameGray, None, fx=scaleFactor, fy=scaleFactor, interpolation=cv.INTER_LINEAR)

        # Calculates dense optical flow by Farneback method
        # https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowfarneback
        # flow = cv.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        flow = cv.calcOpticalFlowFarneback(oldGray, frameGray, None, **fbParams)

        # Computes the magnitude and angle of the 2D vectors
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])

        overlay = np.zeros_like(mask)

        # Filter by speed and direction
        if speedFilter or directionFilter:
            tmpMaskMag = np.ones_like(mag, dtype=bool)
            tmpMaskAng = np.ones_like(ang, dtype=bool)

            if speedFilter:
                cv.putText(overlay, f"Speed filter: {speedFilter:.2f} px/frame", (frame.shape[0] // 2, 20), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
                tmpMaskMag &= (mag > speedFilter)

            if directionFilter:
                cv.putText(overlay, f"Direction filter: <{directionFilter[0]:.1f}, {directionFilter[1]:.1f}> deg", (frame.shape[0] // 2, 40),
                           cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
                lower, upper = directionFilter
                tmpMaskAng &= (ang * 180 / np.pi >= lower) & (ang * 180 / np.pi <= upper)

            mag = mag * tmpMaskMag
            ang = ang * tmpMaskAng

        # Clustering pixels with similar speed and direction
        if drawBboxes:
            if bboxMethod == "dbscan":
                from sklearn.cluster import DBSCAN

                h, w = mag.shape
                motionPoints = np.column_stack((np.where(mag > 0)))  # Points with ANY motion

                if len(motionPoints) > 0:
                    # Get speed and direction for active pixels
                    motionVectors = np.column_stack((motionPoints, mag[motionPoints[:, 0], motionPoints[:, 1]]))

                    # Clustering points using DBSCAN
                    clustering = DBSCAN(eps=clusteringEps, min_samples=minClusterSize, metric=clusteringMethod, n_jobs=-1).fit(motionPoints)
                    labels = clustering.labels_

                    for label in set(labels):
                        if label == -1: # Ignore noise
                            continue

                        # Check if any points belong to the current cluster
                        clusterPoints = motionPoints[labels == label]

                        # Calculate bounding box for the current cluster
                        x, y, w, h = cv.boundingRect(clusterPoints)
                        x, y, w, h = [int(v / scaleFactor) for v in (x, y, w, h)]

                        # Calculate average speed and direction
                        avgSpeed = mag[clusterPoints[:, 0], clusterPoints[:, 1]].mean()
                        avgAngle = np.degrees(ang[clusterPoints[:, 0], clusterPoints[:, 1]].mean())

                        # Draw green bounding box around the cluster
                        cv.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        # Add speed and direction text
                        txtColor = (0, 255, 0)
                        speedText = f"Speed: {avgSpeed:.2f} px/frame"
                        directionText = f"Dir: {avgAngle:.1f} deg"
                        cv.putText(overlay, speedText, (x, y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, txtColor, 1)
                        cv.putText(overlay, directionText, (x, y - 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, txtColor, 1)

            elif bboxMethod == "threshold":
                # Normalize and threshold the motion magnitude
                motionMagnitude = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
                _, motionMask = cv.threshold(motionMagnitude, thresholdMagnitude, 255, cv.THRESH_BINARY)
                motionMask = motionMask.astype(np.uint8)

                # Find contours on the motion mask
                contours, _ = cv.findContours(motionMask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    if cv.contourArea(cnt) > 500:
                        x, y, w, h = cv.boundingRect(cnt)
                        x, y, w, h = [int(v / scaleFactor) for v in (x, y, w, h)]

                        # Extract magnitudes and angles for points inside the contour
                        tmpMask = np.zeros_like(motionMask, dtype=np.uint8)
                        cv.drawContours(tmpMask, [cnt], -1, color=255, thickness=-1)  # Mask of the current contour

                        # Get magnitudes and angles inside the mask
                        mag_inside = mag[tmpMask > 0]  # Magnitudes of motion vectors
                        ang_inside = ang[tmpMask > 0]  # Angles of motion vectors

                        if mag_inside.size > 0:
                            avgSpeed = np.mean(mag_inside)  # Average motion magnitude
                            avgAngle = np.degrees(np.mean(ang_inside))  # Average motion angle in degrees
                        else:
                            avgSpeed, avgAngle = 0, 0

                        # Draw green bounding box around the cluster
                        cv.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        # Calculate motion components
                        avgMotionX = avgSpeed * np.cos(np.radians(avgAngle))  # X component
                        avgMotionY = avgSpeed * np.sin(np.radians(avgAngle))  # Y component

                        # Draw direction vector as an arrow
                        startPoint = (int(x + w / 2), int(y + h / 2))  # Center of bounding box
                        endPoint = (
                            int(startPoint[0] + avgMotionX * 20),
                            int(startPoint[1] + avgMotionY * 20),
                        )
                        cv.arrowedLine(overlay, startPoint, endPoint, (0, 0, 255), 2, tipLength=0.5)

                        # Add speed and direction text
                        txtColor = (0, 255, 0)
                        speedText = f"Speed: {avgSpeed:.2f} px/frame"
                        directionText = f"Dir: {avgAngle:.1f} deg"
                        cv.putText(overlay, speedText, (x, y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, txtColor, 1)
                        cv.putText(overlay, directionText, (x, y - 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, txtColor, 1)

            else:
                raise ValueError(f"Unknown clustering method: {bboxMethod}")


        """
        TODO !!!
        NOTE: ChatGPT may be stupid but so am I... -_-
        I don't even want to try anymore...
        Clustering pixels based on HSV values
        
        

            # # Klasteryzacja na podstawie HSV
            # ang_copy = ang.copy()
            # mag_copy = mag.copy()
            #
            # # Tworzenie obrazu HSV dla wizualizacji
            # mask_copy = mask.copy()
            # if scaleFactor != 1.0:
            #     mask_copy = cv.resize(mask_copy, None, fx=scaleFactor, fy=scaleFactor, interpolation=cv.INTER_LINEAR)
            # mask_copy[..., 0] = ang_copy * 180 / np.pi / 2  # Kąt na hue
            # mask_copy[..., 2] = cv.normalize(mag_copy, None, 0, 255, cv.NORM_MINMAX)  # Prędkość na value
            #
            # hsv_image = cv.cvtColor(mask_copy, cv.COLOR_HSV2BGR)
            #
            # # Przygotowanie danych wejściowych do klasteryzacji
            # hsv_pixels = np.column_stack((
            #     mask_copy[..., 0].ravel() / 180,  # Hue (skalowane do 0-1)
            #     mask_copy[..., 2].ravel() / 255  # Value (skalowane do 0-1)
            # ))
            #
            # # Filtrowanie pikseli na podstawie prędkości (Value > speedFilter)
            # valid_mask = (mag > speedFilter).ravel()
            # hsv_pixels = hsv_pixels[valid_mask]
            #
            # # print(f"{hsv_pixels.shape = }")
            #
            # if len(hsv_pixels) > 0:
            #     # Klasteryzacja DBSCAN w przestrzeni HSV
            #     clustering = DBSCAN(eps=clusteringEps, min_samples=minClusterSize).fit(hsv_pixels)
            #     labels = clustering.labels_
            #
            #     # print(f"{labels = }")
            #
            #     # Iteracja przez klastry
            #     for label in set(labels):
            #         if label == -1:
            #             continue  # Ignoruj szum
            #
            #         # Znajdź piksele w klastrze
            #         cluster_indices = np.where(labels == label)[0]
            #         cluster_points = np.column_stack(np.where(valid_mask.reshape(mag.shape)))
            #
            #         # Wyznacz bounding box
            #         cluster_box = cv.boundingRect(cluster_points[cluster_indices])
            #         x, y, w, h = cluster_box
            #
            #         # Wylicz średnią prędkość i kierunek klastra
            #         avg_speed = mag[cluster_points[cluster_indices][:, 0], cluster_points[cluster_indices][:, 1]].mean()
            #         avg_angle = ang[cluster_points[cluster_indices][:, 0], cluster_points[cluster_indices][:, 1]].mean()
            #
            #         # Rysowanie bounding boxa
            #         cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #
            #         # Dodanie tekstu z prędkością i kierunkiem
            #         speed_text = f"Speed: {avg_speed:.2f} px/frame"
            #         angle_text = f"Dir: {np.degrees(avg_angle):.1f} deg"
            #         cv.putText(frame, speed_text, (x, y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            #         cv.putText(frame, angle_text, (x, y - 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        """


        if scaleFactor != 1.0:
            ang = cv.resize(ang, None, fx=(1 / scaleFactor), fy=(1 / scaleFactor), interpolation=cv.INTER_LINEAR)
            mag = cv.resize(mag, None, fx=(1 / scaleFactor), fy=(1 / scaleFactor), interpolation=cv.INTER_LINEAR)

        # Sets image hue according to the optical flow direction
        mask[..., 0] = ang * 180 / np.pi / 2
        # Sets image value according to the optical flow magnitude (normalized)
        mask[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)

        # Converts HSV to RGB (BGR) color representation
        bgr = cv.cvtColor(mask, cv.COLOR_HSV2BGR)

        bgr = cv.add(bgr, overlay)

        # Set window size and position for large images
        if bgr.shape[0] > windowSize[1] or bgr.shape[1] > windowSize[0]:
            cv.namedWindow(windowName, cv.WINDOW_NORMAL)
            cv.resizeWindow(windowName, windowSize)

        else:
            cv.namedWindow(windowName, cv.WINDOW_AUTOSIZE)

        # cv.moveWindow(windowName, 0, 0)

        # Break if window is closed
        if cv.getWindowProperty(windowName, cv.WND_PROP_VISIBLE) < 1:
            break

        cv.imshow(windowName, bgr)
        # out.write(bgr)

        # Frames are read by intervals of 30 milliseconds. The programs breaks out of the while loop when the user presses the 'Esc' or 'q' key
        # if 's' is pressed, it saves the current frame
        k = cv.waitKey(30) & 0xff
        if k == 27 or k == ord('q'):
            break

        elif k == ord('s'):
            denseDir = "dense_flow"
            if not os.path.exists(denseDir):
                os.makedirs(denseDir)

            cv.imwrite(os.path.join(denseDir, f'dense_original_{frameCount}.png'), frame)
            cv.imwrite(os.path.join(denseDir, f'dense_mask_{frameCount}.png'), bgr)

            print(Fore.GREEN + f"\nDense flow frame no. {frameCount} saved to folder: {denseDir}")

        oldGray = frameGray.copy()
        frameCount += 1
        frameTimes.append(perf_counter() - startTime)
        # print(f"Frame time: {frameTime:.2f} s")

    # Calculate average time of operations per frame
    avgTime = np.mean(frameTimes)
    print(Fore.GREEN + f"\nAverage mean operation time per frame: {avgTime:.4f} sec/frame")

    # Release resources and close windows
    # if out is not None:
    #     out.release()
    if cap is not None:
        cap.release()
    cv.destroyAllWindows()