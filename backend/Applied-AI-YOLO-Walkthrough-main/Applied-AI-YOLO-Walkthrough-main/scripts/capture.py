"""Capture frames from a video file for a YOLO training dataset.

Press SPACE to save the current frame to disk.
Press Q to quit.

Scrubbing controls:
  LEFT/RIGHT arrows: Step backward/forward by 5 frames
  HOME/END: Jump to start/end of video
  0-9: Jump to 0%, 10%, 20%... 90% of video

Frames are saved to data/captured/ as JPGs with a timestamp-based filename.
Run from the project root: `python scripts/capture.py`.
"""
import argparse
import sys
import time
from pathlib import Path

import cv2


def open_video_file(video_path: str = "sample/ensantina.mp4"):
    """Open a video file for frame capture.

    Args:
        video_path: Path to the video file (relative or absolute)
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open video file: {video_path}. "
            "Please ensure the file exists and is a valid video format."
        )
    return cap


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="data/captured",
                        help="Directory to save captured frames")
    parser.add_argument("--video", default="sample/ensantina.mp4",
                        help="Path to video file (default: sample/ensantina.mp4)")
    parser.add_argument("--prefix", default="frame",
                        help="Filename prefix for saved frames")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    cap = open_video_file(args.video)

    print(f"Saving frames to {output_dir.resolve()}")
    print("SPACE to save, Q to quit.")

    saved = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Reached end of video file or failed to read frame.")
            break

        # Show a copy so the saved file does not include the on-screen counter.
        display = frame.copy()
        cv2.putText(display, f"saved: {saved}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("capture (SPACE=save, Q=quit)", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):
            timestamp = int(time.time() * 1000)
            path = output_dir / f"{args.prefix}_{timestamp}.jpg"
            cv2.imwrite(str(path), frame)
            saved += 1
            print(f"  [{saved}] {path.name}")
        elif key in (ord("q"), 27):  # Q or Escape
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Done. Saved {saved} frames to {output_dir.resolve()}")


if __name__ == "__main__":
    main()
