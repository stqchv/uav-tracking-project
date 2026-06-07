import time

from communication.frame_streamer import FrameStreamer
from communication.telemetry_receiver import TelemetryReceiver
from hardware.flight_controller_sender import FlightController

def main():
    streamer = FrameStreamer(target_ip="172.20.10.5", port=5000)
    receiver = TelemetryReceiver(udp_ip="0.0.0.0", udp_port=5001)
    fc = FlightController()

    failsafe_timeout = 1.5
    last_msg_time = time.time()
    failsafe_triggered = False

    try:
        streamer.start()
        print("[UAV] Waiting for commends...")

        while True:
            v_x, v_y = receiver.read()
            current_time = time.time()

            if v_x is not None and v_y is not None:
                print(f"[CONTROL] Recieved movement: v_x: {v_x}, v_y: {v_y}")

            #     fc.send_velocity_ned(v_x, v_y)

            #     last_msg_time = current_time
            #     if failsafe_triggered:
            #         print("[SAFETY] Sygnał odzyskany! Wznawiam ruch.")
            #         failsafe_triggered = False

            # else:
            #     if (current_time - last_msg_time > failsafe_timeout) and not failsafe_triggered:
            #         print(f"[SAFETY] 🛑 Failsafe! Brak komend od {failsafe_timeout}s. Zatrzymuję drona!")
            #         fc.stop_drone()
            #         failsafe_triggered = True
            
            # time.sleep(0.05)
    except KeyboardInterrupt:
        print("\n[UAV] Przerwano działanie programu...")
    finally:
        fc.stop_drone()
        streamer.stop()
        receiver.close()

if __name__ == "__main__":
    main()