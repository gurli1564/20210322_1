@echo off
chcp 65001 > nul
cd /d "%~dp0"
set PY=python
where python > nul 2>&1 || set PY=py
%PY% -m pip install -r requirements.txt -q
%PY% auto_clicker.py --interval 2 --confidence 0.8
pause
