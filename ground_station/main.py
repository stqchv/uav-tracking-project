import cv2
import time

from communication.video_receiver import start_video_stream, receive_frame
from control import convert
from vision.person_detector import PersonDetector

def main():
    video_stream = start_video_stream(port=5000)
    if video_stream is None: return
    time.sleep(0.5)

    vision = PersonDetector()
    
    try:
        while True:
            ret, frame = receive_frame(video_stream)

            if not ret or frame is None:
                # print("Lost frame. Waiting for another...")
                continue

            # YOLO detection
            error_x, error_y, annotated_frame = vision.get_target_error(frame)

            # CONTROLL
            # if error_x is not None:
            #     print(f"Błąd X: {error_x}, Y: {error_y}")

            cv2.imshow("Base Station - Tracking Live", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Closing ground station...")
                break
    finally:
        video_stream.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

