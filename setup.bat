@echo off
echo ====================================
echo    AGE GENDER RECOGNITION SETUP
echo ====================================
echo.

echo Checking Python installation...
py --version
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found! Please install Python first.
    pause
    exit /b 1
)

echo.
echo Upgrading pip and setuptools...
py -m pip install --upgrade pip setuptools wheel

echo.
echo Installing required libraries...
echo Installing NumPy...
py -m pip install --pre --find-links https://pypi.anaconda.org/scientific-python-nightly-wheels/simple numpy

echo Installing OpenCV...
py -m pip install opencv-python --no-deps

echo Installing Pillow...
py -m pip install Pillow

echo.
echo Testing installation...
py -c "import cv2; import numpy as np; from PIL import Image; print('All libraries installed successfully!')"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================
    echo    SETUP COMPLETED SUCCESSFULLY!
    echo ====================================
    echo.
    echo To run the program, execute: py main.py
    echo.
) else (
    echo.
    echo ====================================
    echo    SETUP FAILED!
    echo ====================================
    echo Please check the error messages above.
)

pause