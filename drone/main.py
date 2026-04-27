import time

from communication.frame_streamer import FrameStreamer
from communication.telemetry_receiver import TelemetryReceiver

def main():
    streamer = FrameStreamer(target_ip="172.20.10.5", port=5000)
    receiver = TelemetryReceiver(udp_ip="0.0.0.0", udp_port=5001)

    try:
        streamer.start()
        print("[UAV] Waiting for commends...")

        while True:
            v_x, v_y = receiver.read()

            if v_x is not None and v_y is not None:
                print(f"[CONTROL] Recieved movement: v_x: {v_x}, v_y: {v_y}")
            
            time.sleep(.1)

    finally:
        streamer.stop()
        receiver.close()

if __name__ == "__main__":
    main()