import os
import platform

from colorama import Fore, init as colorama_init

colorama_init(autoreset=True)

def configure_qt_platform() -> None:
    """
    Sets the `QT_QPA_PLATFORM` environment variable to 'xcb' on Linux systems to suppress warnings about Wayland plugins.

    :return: None
    """
    if platform.system() == "Linux":
        try:
            os.environ["QT_QPA_PLATFORM"] = "xcb"

            print(
                Fore.GREEN
                + "\n\n[CONFIGURATION] QT_QPA_PLATFORM set to 'xcb'\n"
            )

        except Exception as e:
            print(
                Fore.RED
                + f"\nWarning: Unable to set QT_QPA_PLATFORM to 'xcb': {e}\n"
            )
            raise

    else:
        print(
            Fore.GREEN
            + "\n\n[CONFIGURATION] QT_QPA_PLATFORM not set on non-Linux systems\n"
        )

# Optional: Uncomment the line below to enable automatic configuration
# configure_qt_platform()