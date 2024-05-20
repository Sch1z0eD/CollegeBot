@echo off
REM Set the name of the virtual environment
set VENV_NAME=venv

REM Create a virtual environment
python -m venv %VENV_NAME%

REM Activate the virtual environment
call %VENV_NAME%\Scripts\activate

REM Install the required packages
pip install -r requirements.txt

REM Run the bot
python main.py

REM Deactivate the virtual environment
deactivate

REM Optional: pause the script to keep the command prompt open
pause