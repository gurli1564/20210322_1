# 화면 감지 자동 클릭 프로그램

특정 화면(버튼, 팝업 등)이 나타나면 자동으로 클릭해 주는 프로그램입니다.
Windows / macOS / Linux(X11)에서 동작합니다.

## 1. 설치

[Python 3.8+](https://www.python.org/downloads/) 설치 후:

```bash
pip install -r requirements.txt
```

## 2. 클릭할 화면 캡처

1. 클릭하고 싶은 버튼/화면이 떠 있을 때 그 부분만 캡처합니다.
   (Windows: `Win + Shift + S`, macOS: `Cmd + Shift + 4`)
2. 캡처한 이미지를 `targets` 폴더에 png로 저장합니다. 여러 장 넣어도 됩니다.

> 팁: 버튼 글자 등 **특징적인 부분만 작게** 자르면 더 잘 찾습니다.
> 캡처할 때와 같은 화면 배율(디스플레이 확대/축소 %)에서 사용하세요.

## 3. 실행

```bash
python auto_clicker.py
```

중지: 콘솔에서 `Ctrl + C`, 또는 마우스를 **화면 왼쪽 위 모서리**로 이동.

## 옵션

| 옵션 | 설명 | 기본값 |
|---|---|---|
| `--interval 0.5` | 화면 검사 간격(초) | 1.0 |
| `--confidence 0.8` | 일치 정확도 (낮을수록 느슨하게 찾음) | 0.85 |
| `--clicks 2` | 클릭 횟수 (2 = 더블클릭) | 1 |
| `--button right` | 마우스 버튼 (left/right/middle) | left |
| `--offset 50 0` | 찾은 위치 기준으로 옆을 클릭 | 0 0 |
| `--cooldown 3` | 클릭 후 대기 시간(초) | 2.0 |
| `--once` | 한 번 클릭 후 종료 | - |
| `--max-clicks 10` | 최대 클릭 횟수 | 무제한 |
| `--no-return` | 클릭 후 마우스를 원위치로 되돌리지 않음 | - |
| `--grayscale` | 흑백 비교 (빠름) | - |
| `--folder 경로` | 대상 이미지 폴더 | ./targets |

예시:

```bash
python auto_clicker.py --interval 0.5 --confidence 0.8 --once
```

## 문제 해결

- **못 찾을 때**: `--confidence`를 0.7 정도로 낮추거나, 이미지를 더 작게/정확히 다시 캡처하세요.
- **macOS**: 시스템 설정 → 개인정보 보호 및 보안 → *화면 기록*, *손쉬운 사용*에 터미널 권한을 허용해야 합니다.
- **Linux**: X11 환경 필요 (`sudo apt install scrot python3-tk python3-dev`).
