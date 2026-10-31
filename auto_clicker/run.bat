@echo off
chcp 65001 > nul
cd /d "%~dp0"
pip install -r requirements.txt -q
python auto_clicker.py --interval 2 --confidence 0.8
pause
