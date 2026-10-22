@echo off
title DSA Traffic Racer
cd /d "%~dp0"
echo Starting DSA Traffic Racer...
py main.py
if %errorlevel% neq 0 (
    echo.
    echo Game exited with an error code: %errorlevel%
    pause
)
