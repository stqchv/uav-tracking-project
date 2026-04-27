import time
from communication.telemetry_sender import TelemetrySender

sender = TelemetrySender(udp_ip="172.20.10.2", udp_port=5001)

print("Rozpoczynam ciągłe wysyłanie...")
while True:
    sender.send_velocity(1.5, -2.5)
    print("Wysłano pakiet!")
    time.sleep(0.5)