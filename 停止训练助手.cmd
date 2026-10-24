@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ". '%~dp0env.ps1'; & '%~dp0venv\Scripts\python.exe' '%~dp0stop_trainer.py'"
pause
