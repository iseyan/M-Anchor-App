@echo off
cd /d "%~dp0"
py -3 app\launcher.py --fresh-demo
if errorlevel 1 (
  echo Startup failed. Read the error above and README.md.
  pause
)
