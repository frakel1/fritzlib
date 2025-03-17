# Fritzbox Library

This project is a Python library designed to interact with Fritzbox devices. It provides classes and methods for managing devices, handling errors, and performing various operations related to Fritzbox functionalities.

## Features

- **Device Management**: Easily manage and interact with devices connected to a Fritzbox.
- **Error Handling**: Custom exceptions for handling login and communication errors.
- **User Interface**: Dialogs for user input and device selection.

## Installation

To install the Fritzbox library, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd fritzbox-library
pip install -r requirements.txt
```

## Usage

To use the Fritzbox library, import the necessary classes from the `fritzbox_library` package. Here is a simple example:

```python
from fritzbox_library.fritz_classes import fritzbox

# Initialize the Fritzbox connection
fritz = fritzbox()
```

## Running Tests

To run the unit tests for the library, navigate to the `tests` directory and execute:

```bash
python -m unittest discover
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.