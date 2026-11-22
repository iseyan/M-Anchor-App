@echo off
setlocal
cd /d "%~dp0"
rem Choose Python once: the py launcher if it gives Python 3.10 or later, otherwise python.
set "PYCMD="
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
if not errorlevel 1 set "PYCMD=py -3"
if defined PYCMD goto run
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
if not errorlevel 1 set "PYCMD=python"
if defined PYCMD goto run
echo Python 3.10 or later was not found.
echo Tried "py -3" and "python". Install Python 3.10 or later from python.org, then run this file again.
echo If "python" opens the Microsoft Store, Python is not installed yet.
pause
exit /b 1
:run
%PYCMD% app\launcher.py
if errorlevel 1 (
  echo Startup failed. Read the error above and README.md.
  pause
)
