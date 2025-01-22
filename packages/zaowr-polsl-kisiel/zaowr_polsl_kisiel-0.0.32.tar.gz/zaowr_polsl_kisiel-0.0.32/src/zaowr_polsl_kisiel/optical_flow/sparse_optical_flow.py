import os
from time import perf_counter
import cv2 as cv
import numpy as np
from colorama import Fore, init as colorama_init

from . import read_images_from_folder

colorama_init(autoreset=True)

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
) -> None:
    """
    Calculate sparse optical flow using Shi-Tomasi corner detection and Lucas-Kanade optical flow. Options to draw bounding boxes around moving objects are provided (**DBSCAN - Density-Based Spatial Clustering of Applications with Noise** and **threshold**).

    :param source: The source of the video feed. Can be a camera number, video file path, or folder with images.
    :param maxCorners: The maximum number of corners to detect (**Shi-Tomasi**).
    :param qualityLevel: The quality level for corner detection (**Shi-Tomasi**).
    :param minDistance: The minimum distance between corners (**Shi-Tomasi**).
    :param blockSize: The block size for corner detection (**Shi-Tomasi**).
    :param winSize: The window size for **Lucas-Kanade** optical flow.
    :param maxLevel: The maximum pyramid level for **Lucas-Kanade** optical flow.
    :param criteria: The termination criteria for **Lucas-Kanade** optical flow.

    :param drawBboxes: Whether to draw bounding boxes around detected corners.
    :param bboxMethod: The method for drawing bounding boxes (**"dbscan"** or **"threshold"**).

    :param thresholdMagnitude: The threshold magnitude for bounding boxes (**threshold**).

    :param clusteringEps: The epsilon value for clustering (**DBSCAN**).
    :param minClusterSize: The minimum size of a cluster (**DBSCAN**).
    :param clusteringMethod: The method for clustering (**DBSCAN**).

    :param scaleFactor: The scale factor to resize the image (for faster processing).

    :param speedFilter: The minimal speed of the object to be detected.
    :param directionFilter: The range of angles for the object to be detected.

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
    if isinstance(source, int) or (isinstance(source, str) and source.isdigit()):
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
        raise ValueError(Fore.RED + f"\nInvalid source! Provide a camera number, video file path, or folder with images ({source})\n\n")

    # Parameters for Shi-Tomasi corner detection
    featureParams = dict(
        maxCorners=maxCorners,
        qualityLevel=qualityLevel,
        minDistance=minDistance,
        blockSize=blockSize
    )

    # Parameters for Lucas-Kanade optical flow
    lkParams = dict(
        winSize=winSize,
        maxLevel=maxLevel,
        criteria=criteria
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

    # Variable for color to draw optical flow track
    # color = (127, 127, 127)
    color = np.random.randint(0, 255, (oldGray.shape[0], 3))

    # Creates an image filled with zero intensities with the same dimensions as the frame - for later drawing purposes
    mask = np.zeros_like(oldFrame)

    if scaleFactor != 1.0:
        oldGray = cv.resize(oldGray, None, fx=scaleFactor, fy=scaleFactor, interpolation=cv.INTER_LINEAR)

    # Detect initial feature points
    p0 = cv.goodFeaturesToTrack(oldGray, mask=None, **featureParams)

    print(Fore.GREEN + f"\nReading from source (type: '{sourceType}'): {source}")
    # print(Fore.GREEN + f"\nWindow '{windowName}' is going to be moved to the edge of the screen - (0, 0)...")
    print(Fore.GREEN + "\nPress `Esc` or `q` to exit...\nPress `s` to save current frame...")

    frameCount = 0
    frameTimes = []
    goodOld, goodNew = None, None
    # out = cv.VideoWriter('output_sparse.avi', cv.VideoWriter_fourcc(*'XVID'), 20.0, (oldGray.shape[1], oldGray.shape[0]))
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

        # Calculates sparse optical flow by Lucas-Kanade method
        # https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowpyrlk
        # next, status, error = cv.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)
        p1, st, err = cv.calcOpticalFlowPyrLK(oldGray, frameGray, p0, None, **lkParams)

        # Select good points
        if p1 is not None:
            # Selects good feature points for previous position
            goodOld = p0[st == 1]
            # Selects good feature points for next position
            goodNew = p1[st == 1]

        else:
            continue

        # draw the tracks
        for i, (new, old) in enumerate(zip(goodNew, goodOld)):
            # Returns a contiguous flattened array as (x, y) coordinates for new point
            a, b = new.ravel()
            # Returns a contiguous flattened array as (x, y) coordinates for old point
            c, d = old.ravel()
            # Draws line between new and old position with green color and 2 thickness
            mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
            # mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)), color, 2)
            # Draws filled circle (thickness of -1) at new position with green color and radius of 3
            frame = cv.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)
            # frame = cv.circle(frame, (int(a), int(b)), 5, color, -1)

        if drawBboxes and len(goodNew) > 0:
            if bboxMethod == "dbscan":
                from sklearn.cluster import DBSCAN

                # Clustering points using DBSCAN
                if len(goodNew) > 0:
                    clustering = DBSCAN(eps=clusteringEps, min_samples=minClusterSize, metric=clusteringMethod, n_jobs=-1).fit(goodNew)
                    labels = clustering.labels_

                    uniqueLabels = set(labels)
                    for label in uniqueLabels:
                        if label == -1: # Ignore noise
                            continue

                        # Check if any points belong to the current cluster
                        clusterPoints = goodNew[labels == label]
                        clusterOldPoints = goodOld[labels == label]

                        # Calculate bounding box for the current cluster
                        x, y, w, h = cv.boundingRect(clusterPoints)
                        x, y, w, h = [int(v / scaleFactor) for v in (x, y, w, h)]

                        # Calculate average motion vector for the cluster
                        motionVectors = (clusterPoints - clusterOldPoints) / scaleFactor
                        avgMotion = np.mean(motionVectors, axis=0)

                        # Calculate speed and direction
                        speed = np.linalg.norm(avgMotion)
                        directionAngle = np.arctan2(avgMotion[1], avgMotion[0]) * 180 / np.pi  # Convert to degrees

                        # Filter by speed and direction
                        if directionFilter:
                            cv.putText(frame, f"Direction filter: <{directionFilter[0]:.1f}, {directionFilter[1]:.1f}> deg", (frame.shape[0] // 2, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
                            lower, upper = directionFilter
                            if not (lower <= directionAngle <= upper):
                                continue

                        if speedFilter:
                            cv.putText(frame, f"Speed filter: {speedFilter:.2f} px/frame", (frame.shape[0] // 2, 20), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
                            if speed < speedFilter:
                                continue


                        # Draw green bounding box around the cluster
                        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        # Draw direction vector on the image
                        startPoint = (int(x + w / 2), int(y + h / 2))  # Center of bounding box
                        endPoint = (int(startPoint[0] + avgMotion[0] * 20), int(startPoint[1] + avgMotion[1] * 20))
                        cv.arrowedLine(frame, startPoint, endPoint, (0, 0, 255), 2, tipLength=0.5)

                        # Add speed and direction text
                        txtColor = (0, 255, 0)
                        speedText = f"Speed: {speed:.2f} px/frame"
                        directionText = f"Dir: {directionAngle:.1f} deg"
                        cv.putText(frame, speedText, (x, y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.7, txtColor, 1)
                        cv.putText(frame, directionText, (x, y - 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, txtColor, 1)

            elif bboxMethod == "threshold":
                # Calculate motion vectors
                motionVectors = goodNew - goodOld
                # print(f"Motion Vectors: {motionVectors.shape}")

                # Compute the magnitude of motion vectors
                motionMagnitude = np.sqrt((motionVectors[:, 0] ** 2) + (motionVectors[:, 1] ** 2))
#                 print(f"Motion Magnitude: {motionMagnitude}")

                # Normalize the magnitude values for thresholding
                motionMagnitude = cv.normalize(motionMagnitude, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)
#                 print(f"Normalized Motion Magnitude: {motionMagnitude}")

                # Apply binary thresholding
                # _, motionMask = cv.threshold(motionMagnitude, thresholdMagnitude, 255, cv.THRESH_BINARY)
                # print(f"Motion Mask Unique Values: {np.unique(motionMask)}")
                # print(f"Thrreshold Magnitude: {thresholdMagnitude}")
                #
                # # Dilate the motion mask to improve contour detection
                # kernel = np.ones((5, 5), np.uint8)  # Increase kernel size for more expansion
                # motionMask = cv.dilate(motionMask, kernel, iterations=3)

                # Create an empty motion mask
                motionMask = np.zeros(frameGray.shape, dtype=np.uint8)

                # Map motion points directly to the mask with boundary checks
                for (x, y), magnitude in zip(goodNew, motionMagnitude):
                    x, y = int(x), int(y)  # Ensure coordinates are integers
                    if 0 <= y < motionMask.shape[0] and 0 <= x < motionMask.shape[1]:  # Check boundaries
                        motionMask[y, x] = 255

                # Dilate the mask to connect regions
                kernel = np.ones((5, 5), np.uint8)
                motionMask = cv.dilate(motionMask, kernel, iterations=2)

                # Find contours on the binary mask
                contours, _ = cv.findContours(motionMask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#                 print(f"Number of contours detected: {len(contours)}")
#                 contours = sorted(contours, key=cv.contourArea, reverse=True)[:5]  # Keep top 5 largest contours

                for cnt in contours:
#                     print(f"Contour area: {cv.contourArea(cnt)}")
                    if cv.contourArea(cnt) > (frameGray.shape[1]) / 10:
                    # if cv.contourArea(cnt) > 65:
                        # Calculate bounding box for the current cluster
                        x, y, w, h = cv.boundingRect(cnt)
                        x, y, w, h = [int(v / scaleFactor) for v in (x, y, w, h)]

                        # Extract points inside the current contour
                        tmpMask = np.zeros_like(motionMask, dtype=np.uint8)
                        cv.drawContours(tmpMask, [cnt], -1, color=255, thickness=-1)  # Create a mask for the current contour

                        # Get motion vectors within the mask
                        # Collect motion vectors within the current contour
                        motionVectorsInContour = []
                        for i, point in enumerate(goodNew):
                            px, py = point.ravel()
                            if cv.pointPolygonTest(cnt, (px, py), False) >= 0:  # Check if point is inside contour
                                motionVectorsInContour.append(motionVectors[i])

                        motionVectorsInContour = np.array(motionVectorsInContour)  # Convert to a NumPy array

                        if motionVectorsInContour.size > 0:  # Check if any motion vectors are present in the contour
                            # Calculate average motion vector for the cluster
                            avgMotion = np.mean(motionVectorsInContour, axis=0)

                            # Calculate speed and direction
                            speed = np.linalg.norm(avgMotion)
                            directionAngle = np.arctan2(avgMotion[1], avgMotion[0]) * 180 / np.pi  # Convert to degrees
                        else:
                            avgMotion = [0, 0]
                            speed = 0
                            directionAngle = 0

                        # Filter by speed and direction
                        if directionFilter:
                            cv.putText(frame, f"Direction filter: <{directionFilter[0]:.1f}, {directionFilter[1]:.1f}> deg",
                                       (frame.shape[0] // 2, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
                            lower, upper = directionFilter
                            if not (lower <= directionAngle <= upper):
                                continue

                        if speedFilter:
                            cv.putText(frame, f"Speed filter: {speedFilter:.2f} px/frame", (frame.shape[0] // 2, 20), cv.FONT_HERSHEY_SIMPLEX, 0.7,
                                       (0, 0, 255), 1)
                            if speed < speedFilter:
                                continue

                        # Draw green bounding box around the cluster
                        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        # Draw direction vector on the image
                        startPoint = (int(x + w / 2), int(y + h / 2))  # Center of bounding box
                        endPoint = (int(startPoint[0] + avgMotion[0] * 20), int(startPoint[1] + avgMotion[1] * 20))
                        cv.arrowedLine(frame, startPoint, endPoint, (0, 0, 255), 2, tipLength=0.5)

                        # Add speed and direction text
                        txtColor = (0, 255, 0)
                        speedText = f"Speed: {speed:.2f} px/frame"
                        directionText = f"Dir: {directionAngle:.1f} deg"
                        cv.putText(frame, speedText, (x, y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.7, txtColor, 1)
                        cv.putText(frame, directionText, (x, y - 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, txtColor, 1)

                        # tmpMask = cv.cvtColor(tmpMask, cv.COLOR_GRAY2BGR)
                        # mask = cv.add(mask, tmpMask)

            else:
                raise ValueError(f"Unknown clustering method: {bboxMethod}")


        # Overlays the optical flow tracks on the original frame
        img = cv.add(frame, mask)

        # print(f"{img.shape[0] = ^24}")
        # print(f"{img.shape[1] = ^24}")
        # print(f"{windowSize[0] = ^24}")
        # print(f"{windowSize[1] = ^24}")

        # Set window size and position for large images
        if img.shape[0] > windowSize[1] or img.shape[1] > windowSize[0]:
            cv.namedWindow(windowName, cv.WINDOW_NORMAL)
            cv.resizeWindow(windowName, windowSize)

        else:
            cv.namedWindow(windowName, cv.WINDOW_AUTOSIZE)

        # cv.moveWindow(windowName, 0, 0)

        # Break if window is closed
        if cv.getWindowProperty(windowName, cv.WND_PROP_VISIBLE) < 1:
            break

        cv.imshow(windowName, img)
        # out.write(img)

        # Frames are read by intervals of 30 milliseconds. The programs breaks out of the while loop when the user presses the 'Esc' or 'q' key
        k = cv.waitKey(30) & 0xff
        if k == 27 or k == ord('q'):
            break

        elif k == ord('s'):
            sparseDir = "sparse_flow"
            if not os.path.exists(sparseDir):
                os.makedirs(sparseDir)

            cv.imwrite(os.path.join(sparseDir, f'sparse_original_{frameCount}.png'), frame)
            cv.imwrite(os.path.join(sparseDir, f'sparse_mask_{frameCount}.png'), img)

            print(Fore.GREEN + f"\nSparse flow frame no. {frameCount} saved to folder: {sparseDir}")

        # Now update the previous frame and previous points
        oldGray = frameGray.copy()
        p0 = goodNew.reshape(-1, 1, 2)

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