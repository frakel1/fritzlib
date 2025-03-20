# Fritzlib Documentation

Fritzlib is a Python library designed to manage Fritzbox devices and perform login operations. It provides a set of classes that facilitate communication with Fritzbox devices, allowing users to control and monitor their smart home environment.

## Installation

To install Fritzlib, clone the repository and run the following command in the project directory:

```bash
pip install .
```

## Usage

Here is a basic example of how to use Fritzlib:

```python
from fritzlib import fritzbox

# Initialize the Fritzbox connection
fb = fritzbox()

# Perform operations with the Fritzbox instance
# Example: Get the list of devices
devices = fb.getdevices()
print(devices)
```

## Classes

The library includes the following main classes:

- `Login_Error`: Handles exceptions related to login issues.
- `Communication_Error`: Manages exceptions for communication-related problems.
- `terminationmessage`: Displays termination messages for the application.
- `trackingparameter`: Collects initial scanning parameters.
- `fritzdevice`: Represents a device registered in the Fritzbox.
- `fritzbox`: Manages access to the Fritzbox and device commands.
- `logindialog`: Provides a dialog for user login.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.