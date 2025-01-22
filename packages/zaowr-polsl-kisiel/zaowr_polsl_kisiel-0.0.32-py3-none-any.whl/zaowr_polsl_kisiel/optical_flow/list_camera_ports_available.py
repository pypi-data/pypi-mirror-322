import cv2 as cv
from colorama import Fore, init as colorama_init

colorama_init(autoreset=True)

def list_camera_ports_available() -> tuple[list[int], list[int], list[int]]:
    """
    Test the ports and list the available cameras and the ones that are working.

    :return: A tuple with the available ports, the ones that are working and the ones that are not.
    """
    nonWorkingPorts = []
    devPort = 0
    workingPorts = []
    availablePorts = []
    while len(nonWorkingPorts) < 6: # if there are more than 5 non working ports stop the testing.
        camera = cv.VideoCapture(devPort)
        if not camera.isOpened():
            nonWorkingPorts.append(devPort)
            print(Fore.RED + f"\nPort {devPort} is not working.")
        else:
            isReading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if isReading:
                print(Fore.GREEN + f"\nPort {devPort} is working and reads images ({h} x {w})")
                workingPorts.append(devPort)
            else:
                print(Fore.YELLOW + f"\nPort {devPort} for camera ( {h} x {w}) is present but does not reads.")
                availablePorts.append(devPort)
        devPort +=1
    return availablePorts, workingPorts, nonWorkingPorts