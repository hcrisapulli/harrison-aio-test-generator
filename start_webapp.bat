@echo off
cd /d "%~dp0"
echo Starting AIO Test Generator...
start "" http://localhost:5001
python app.py
