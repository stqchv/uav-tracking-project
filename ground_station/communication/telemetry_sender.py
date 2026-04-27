import socket

class TelemetrySender:
    def __init__(self, udp_ip, udp_port=5000):
        self.udp_ip = udp_ip
        self.udp_port = udp_port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"[TELEMETRY] Transmitter ready. Sending to {self.udp_ip}: {self.udp_port}...")

    def send_velocity(self, v_x, v_y):
        message = f"{v_x},{v_y}"
        self.sock.sendto(message.encode('utf-8'), (self.udp_ip, self.udp_port))
    
    def close(self):
        self.sock.close()
        print(f"[TELEMETRY] Connection closed.")
