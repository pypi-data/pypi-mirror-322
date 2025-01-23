# Dungeon Crawler

This project introduces a hand gesture-controlled dungeon-crawler game that lets users engage with the game through basic hand signs. The Python-developed game allows players to move around the dungeon by using a camera to recognize and decipher hand gestures. Through the use of camera-based gesture recognition, the game seeks to produce an immersive, accessible, and user-friendly experience.

## Runtime Platform

- **Architecture**: x86_64
- **Operating System**: Windows, macOS, Linux

## Technology Stack

- **Programming Language**: Python 3.8+
- **Libraries**:
  - `pygame` for game development
  - `opencv-python` for camera handling
  - `mediapipe` for hand gesture recognition
  - `numpy` for numerical operations
- **Package Manager**: `pip`

## Installation

### Prerequisites

Ensure you have Python 3.8 or higher installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

### Dependencies

Install the required dependencies using `pip`. Run the following command in your terminal:

```sh
pip install -r requirements.txt
```

### Additional Setup

Ensure your system has a working camera for hand gesture recognition.

## Building and Compiling

No explicit build or compile steps are required for this Python project. Ensure all dependencies are installed as mentioned above.

## Packaging and Distribution

To package the game for distribution, follow these steps:

1. **Create a `setup.py` file** in the root directory of your project with the necessary configuration.
2. **Build the package** using `setuptools`:
    ```sh
    python setup.py sdist bdist_wheel
    ```
3. **Upload the package to PyPI** using `twine`:
    ```sh
    twine upload dist/*
    ```

## Installing and Running the Package

Users can install and run the package using `pipx`:

```sh
pipx install dungeon-crawler
dungeon-crawler
```

This will install your package in an isolated environment and create a command-line entry point for running the game.

## Launching the Project

To start the game, run the `main.py` file:

```sh
python main.py
```

This will initialize the game window and start the camera for hand gesture recognition. Use hand gestures to control the character within the game.

## Controls

- **Hand Gestures**:
  - Open hand: Stop moving
  - Closed hand: Stop moving
  - Pointing with index finger: Move in the direction of the finger

## Exiting the Game

Press the `q` key to quit the game or close the game window.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

