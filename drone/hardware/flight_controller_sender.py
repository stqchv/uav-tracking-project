import time
from pymavlink import mavutil

class FlightController:
    def __init__(self, port='/dev/ttyAMA0', baud=57600):
        print(f"[MAVLINK] Łączenie z kontrolerem lotu na {port}...")
        self.master = mavutil.mavlink_connection(port, baud=baud)
        self.master.wait_heartbeat()
        print("[MAVLINK] ✅ Połączono! Otrzymano heartbeat od FC.")

    def send_velocity_ned(self, vx, vy, vz=0.0):
        """
        Wysyła wektor prędkości (m/s) do ArduPilota.
        vx: Prędkość przód/tył
        vy: Prędkość prawo/lewo
        """
        type_mask = 0b0000111111000111 

        self.master.mav.set_position_target_local_ned_send(
            0, 
            self.master.target_system, 
            self.master.target_component,
            mavutil.mavlink.MAV_FRAME_BODY_NED, 
            type_mask,
            0, 0, 0, 
            vx, vy, vz, 
            0, 0, 0, 
            0, 0
        )

    def stop_drone(self):
        """Awaryjne wyhamowanie drona do zera."""
        self.send_velocity_ned(0.0, 0.0, 0.0)