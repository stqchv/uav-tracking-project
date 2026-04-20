import cv2
import time

from communication.video_receiver import start_video_stream, recieve_frame
from control import convert
from vision import person_detector

def main():
    video_stream = start_video_stream(port=5000)
    if video_stream is None: return
    time.sleep(0.5)
    
    try:
        while True:
            ret, frame = recieve_frame(video_stream)

            if not ret or frame is None:
                print("Lost frame. Waiting for another...")
                continue

            # YOLO detection
            time.sleep(0.4)

            cv2.imshow("Base Station - Camera Preview", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        video_stream.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

