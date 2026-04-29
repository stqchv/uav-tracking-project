import socket

class TelemetryReceiver:
    def __init__(self, udp_ip="0.0.0.0", udp_port=5001):
        self.udp_ip = udp_ip
        self.udp_port = udp_port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))

        self.sock.setblocking(False)

        print(f"[TELEMETRY] Reciever ready. Listening to port: {self.udp_port}...")

    def read(self):
        try:
            data, addr = self.sock.recvfrom(1024)

            text_data = data.decode('utf-8')

            v_x_str, v_y_str = text_data.split(',')
            v_x = float(v_x_str)
            v_y = float(v_y_str)

            return v_x, v_y
        
        except BlockingIOError:
            return None, None
        
        except Exception as e:
            print(f"[TELEMETRIA] Recieved broken message: {e}")
            return None, None

    def close(self):
        self.sock.close()
        print(f"[TELEMETRY] Connection closed.")