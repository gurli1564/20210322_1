@echo off
chcp 65001 > nul
cd /d "%~dp0"

rem ---- 실제로 동작하는 파이썬 찾기 (py 런처 우선, MS Store 가짜 python 제외) ----
set PY=
py -3 -c "import sys" > nul 2>&1 && set PY=py -3
if not defined PY python -c "import sys" > nul 2>&1 && set PY=python
if not defined PY python3 -c "import sys" > nul 2>&1 && set PY=python3
if not defined PY (
  echo [실패] 실행 가능한 파이썬을 찾지 못했습니다.
  echo  - python.org 에서 파이썬을 설치하고, 설치 첫 화면에서 "Add python.exe to PATH" 를 체크하세요.
  echo  - 또는 Windows 설정 ^> 앱 ^> 고급 앱 설정 ^> 앱 실행 별칭 에서 python.exe / python3.exe 를 끄세요.
  echo.
  where python
  pause
  exit /b
)

echo 사용 파이썬:
%PY% -c "import sys; print(sys.executable); print(sys.version)"
echo.

rem ---- pip 확인 (없으면 설치) ----
%PY% -m pip --version > nul 2>&1 || %PY% -m ensurepip --upgrade

echo [1/2] 필요한 라이브러리 설치 중...
%PY% -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo 일반 설치 실패 - 사용자 폴더 설치로 다시 시도합니다...
  %PY% -m pip install --user -r requirements.txt
  if errorlevel 1 (
    echo.
    echo [실패] 라이브러리 설치에 실패했습니다. 위 메시지 전체를 캡처해서 보내주세요.
    pause
    exit /b
  )
)

echo.
echo [2/2] 자동 클릭 시작
%PY% auto_clicker.py --interval 2 --confidence 0.8
echo.
echo ===== 프로그램이 종료되었습니다. 위 메시지를 캡처해서 보내주세요. =====
pause
