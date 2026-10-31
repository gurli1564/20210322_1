"""
화면 이미지 감지 자동 클릭 프로그램

targets 폴더에 넣어둔 이미지(버튼 캡처 등)가 화면에 나타나면
그 위치를 자동으로 클릭합니다.

중지 방법: 마우스를 화면 왼쪽 위 모서리로 옮기거나 (failsafe), 콘솔에서 Ctrl+C
"""
import argparse
import sys
import time
from pathlib import Path

try:
    import pyautogui
except ImportError:
    sys.exit("pyautogui가 필요합니다:  pip install -r requirements.txt")

try:
    import cv2  # noqa: F401  (confidence 옵션 사용에 필요)
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp"}

pyautogui.FAILSAFE = True  # 마우스를 왼쪽 위 모서리로 옮기면 즉시 중지


def load_targets(folder: Path):
    if not folder.is_dir():
        sys.exit(f"이미지 폴더가 없습니다: {folder}")
    images = sorted(p for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTS)
    if not images:
        sys.exit(f"'{folder}' 폴더에 클릭할 대상 이미지(png/jpg)를 넣어주세요.")
    return images


def find_on_screen(image: Path, confidence: float, grayscale: bool):
    kwargs = {"grayscale": grayscale}
    if HAS_CV2:
        kwargs["confidence"] = confidence
    try:
        return pyautogui.locateCenterOnScreen(str(image), **kwargs)
    except pyautogui.ImageNotFoundException:
        return None


def main():
    parser = argparse.ArgumentParser(description="특정 화면(이미지)이 뜨면 자동으로 클릭")
    parser.add_argument("--folder", default=str(Path(__file__).parent / "targets"),
                        help="대상 이미지 폴더 (기본: ./targets)")
    parser.add_argument("--interval", type=float, default=1.0, help="화면 검사 간격(초), 기본 1.0")
    parser.add_argument("--confidence", type=float, default=0.85,
                        help="일치 정확도 0~1 (opencv 설치 시), 기본 0.85")
    parser.add_argument("--clicks", type=int, default=1, help="클릭 횟수 (2 = 더블클릭)")
    parser.add_argument("--button", choices=["left", "right", "middle"], default="left")
    parser.add_argument("--offset", type=int, nargs=2, default=[0, 0], metavar=("X", "Y"),
                        help="찾은 위치 중심에서 이동해서 클릭할 픽셀 (예: --offset 50 0)")
    parser.add_argument("--cooldown", type=float, default=2.0,
                        help="클릭 후 다음 검사까지 대기(초), 기본 2.0")
    parser.add_argument("--once", action="store_true", help="한 번 클릭하면 종료")
    parser.add_argument("--max-clicks", type=int, default=0, help="최대 클릭 횟수 (0 = 무제한)")
    parser.add_argument("--no-return", action="store_true",
                        help="클릭 후 마우스를 원래 위치로 되돌리지 않음")
    parser.add_argument("--grayscale", action="store_true", help="흑백으로 비교 (더 빠름)")
    args = parser.parse_args()

    targets = load_targets(Path(args.folder))
    if not HAS_CV2:
        print("[알림] opencv 미설치 → 정확히 일치하는 이미지만 찾습니다. "
              "(pip install opencv-python 권장)")

    print(f"감시 시작: {len(targets)}개 이미지 → {', '.join(t.name for t in targets)}")
    print("중지: Ctrl+C 또는 마우스를 화면 왼쪽 위 모서리로 이동\n")

    total = 0
    try:
        while True:
            clicked = False
            for img in targets:
                pos = find_on_screen(img, args.confidence, args.grayscale)
                if pos is None:
                    continue
                x, y = pos.x + args.offset[0], pos.y + args.offset[1]
                original = pyautogui.position()
                pyautogui.click(x, y, clicks=args.clicks, interval=0.1, button=args.button)
                if not args.no_return:
                    pyautogui.moveTo(original)
                total += 1
                print(f"[{time.strftime('%H:%M:%S')}] '{img.name}' 발견 → ({x}, {y}) 클릭 (총 {total}회)")
                clicked = True
                if args.once or (args.max_clicks and total >= args.max_clicks):
                    print("설정한 횟수만큼 클릭하여 종료합니다.")
                    return
                break  # 한 번에 하나씩 클릭
            time.sleep(args.cooldown if clicked else args.interval)
    except KeyboardInterrupt:
        print("\n사용자가 중지했습니다.")
    except pyautogui.FailSafeException:
        print("\nFailsafe 작동(마우스가 모서리로 이동) → 중지했습니다.")


if __name__ == "__main__":
    main()
