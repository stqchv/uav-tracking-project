import time

from communication.frame_streamer import FrameStreamer

def main():
    streamer = FrameStreamer(target_ip="172.20.10.5", port=5000)

    try:
        streamer.start()

        print("[UAV] Waiting for commends...")

        while True:
            time.sleep(1)

    finally:
        streamer.stop()

if __name__ == "__main__":
    main()