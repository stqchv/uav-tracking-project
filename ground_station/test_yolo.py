import time
print("1. Rozpoczynam import YOLO...")
start_time = time.time()
from ultralytics import YOLO
print(f"2. Import zakończony w {time.time() - start_time:.2f} sekund. Teraz ładuję model...")
start_time = time.time()
model = YOLO("yolov8n.pt") # lub waga, której używasz (nano, small)
print(f"3. Model załadowany w {time.time() - start_time:.2f} sekund. Sukces!")
