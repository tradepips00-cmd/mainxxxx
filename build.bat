
@echo off
python -m pip install --upgrade pip
pip install -r requirements.txt
pyinstaller --noconfirm --onefile --windowed --name VelocityPanel main.py
echo.
echo EXE staat in: dist\VelocityPanel.exe
pause
