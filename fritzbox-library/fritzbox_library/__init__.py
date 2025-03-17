# This file initializes the fritzbox_library package.
# It defines what is exported when the package is imported.

from .fritz_classes import (
    Login_Error,
    Communication_Error,
    terminationmessage,
    trackingparameter,
    fritzdevice,
    fritzbox,
)

__all__ = [
    "Login_Error",
    "Communication_Error",
    "terminationmessage",
    "trackingparameter",
    "fritzdevice",
    "fritzbox",
]