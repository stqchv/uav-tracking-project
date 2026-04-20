import cv2

from communication.video_receiver import start_video_stream, recieve_frame
from control import convert
from vision import person_detector

def main():
    cap = start_video_stream(port=5000)

    if cap is None:
        return
    
    try:
        while True:
            ret, frame = recieve_frame(cap)

            if not ret:
                print("Frame lost or connection failed.")
                break

            # YOLO detection

            cv2.imshow("Base Station - Camera Preview", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

