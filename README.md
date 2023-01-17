# Sudokusolver
* [Motivation](#motivation)
* [Features](#features)
* [Known Issues](#known_issues)
* [Limitations](#Limitations)
* [Usage](#usage)

## Motivation
The project was created during my studies at the FH Aachen in the module image processing.
The program reads in a Sudoku in the form of an image via webcam or via sample images and provides the recognized numbers and, if required, the solution.

## Features
The program can have the following features:
Read in and process images (webcam)
Modify read in numbers

## Known_Issues
Due to the limited time, errors may occur during use. The following is a list of known errors by the first useage:
* Reliable reading of numbers
* Not detect the webcam -> main.py:17 ::Change Number
* No reading of numbers -> main.py:20 ::Change to your Path

## Limitations
Since the OCR engine Tesseract is only available for Windows, the application is limited to computers with an installed Windows operating system (Win10+)
## Usage
To use the program you need python 3.0 or higher
Additionally, you need the OCR engine Tesseract to convert the numbers (https://github.com/UB-Mannheim/tesseract/wiki)
To install the following packages you need pip or an alternative package installer (https://pip.pypa.io/en/stable/installation/)
~~~~~~~~~~~~~{.cpp}
pip install opencv-python
pip install numpy
pip install tk
pip install Pillow
pip install threaded
pip install scipy
pip install DateTime
pip install python-time
~~~~~~~~~~~~~
