@echo off
chcp 65001 > nul
cd /d "%~dp0"
set PY=python
where python > nul 2>&1 || set PY=py
echo [1/2] 필요한 라이브러리 설치 중...
%PY% -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo [실패] 라이브러리 설치에 실패했습니다. 위 오류 메시지를 캡처해서 보내주세요.
  pause
  exit /b
)
echo.
echo [2/2] 자동 클릭 시작
%PY% auto_clicker.py --interval 2 --confidence 0.8
echo.
echo ===== 프로그램이 종료되었습니다. 위 메시지를 캡처해서 보내주세요. =====
pause
