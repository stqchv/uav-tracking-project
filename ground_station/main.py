import cv2
import time

from communication.video_receiver import VideoStream
from communication.telemetry_sender import TelemetrySender
# from control.movementspeed import ErrorToMovement
from vision.person_detector import PersonDetector

def main():
    video_stream = VideoStream(port=5000)
    if not video_stream.running:
        print("Error: Could not open stream.")
        return
    video_stream.start()

    telemetry_sender = TelemetrySender(udp_ip="172.20.10.2", udp_port=5001)

    time.sleep(0.5)

    vision = PersonDetector()
    
    try:
        while True:
            print(f"[TELEMETRY] Sending telemetry message.")

            ret, frame = video_stream.read()

            if not ret or frame is None:
                # print("Lost frame. Waiting for another...")
                continue

            # YOLO detection
            error_x, error_y, annotated_frame = vision.get_target_error(frame)

            telemetry_sender.send_velocity(error_x, error_y)

            # CONTROLL
            # if error_x is not None:
            #     print(f"Błąd X: {error_x}, Y: {error_y}")

            cv2.imshow("Base Station - Tracking Live", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Closing ground station...")
                break

            time.sleep(0.05)
    finally:
        video_stream.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

