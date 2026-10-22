@echo off
title DSA Traffic Racer - Unit Tests
cd /d "%~dp0"
echo ========================================================
echo Running DSA Traffic Racer Unit & Integration Tests...
echo ========================================================
py -m unittest discover tests -v
echo.
echo ========================================================
echo All tests completed.
echo ========================================================
pause
