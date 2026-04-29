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
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                latest_data = data

            except BlockingIOError:
                break

            except Exception as e:
                continue
            
            if latest_data is None:
                return None, None
            
        try:
            text_data = data.decode('utf-8')
            v_x_str, v_y_str = text_data.split(',')
            v_x = float(v_x_str)
            v_y = float(v_y_str)

            return v_x, v_y
    
        except Exception as e:
            print(f"[TELEMETRIA] Error parsing newest message: {e}")
            return None, None

    def close(self):
        self.sock.close()
        print(f"[TELEMETRY] Connection closed.")