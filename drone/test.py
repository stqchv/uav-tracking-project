import time
from communication.telemetry_receiver import TelemetryReceiver

receiver = TelemetryReceiver(udp_ip="0.0.0.0", udp_port=5001)

print("Rozpoczynam nasłuch...")
while True:
    vx, vy = receiver.read()
    if vx is not None and vy is not None:
        print(f"BINGO! Otrzymano: v_x={vx}, v_y={vy}")
    
    time.sleep(0.1)