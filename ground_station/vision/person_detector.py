import cv2
import time
from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_path='vision/yolov8n.pt'):
        print(f"[VISION] Reading model from: {model_path}")
        self.model = YOLO(model_path)

        self.width = None
        self.height = None
        self.center_x = None
        self.center_y = None

    def get_target_error(self, frame):
        start_time = time.time()

        if self.width is None:
            self.height, self.width = frame.shape[:2]
            self.center_x = self.width // 2.0
            self.center_y = self.height // 2.0
            print(f"[VISION] Set image middle point (UDP): ({self.center_x}, {self.center_y})")
        
        annotated_frame = frame.copy()

        results = self.model.predict(frame, classes=0, conf=.5, verbose=False)

        cv2.drawMarker(annotated_frame, (int(self.center_x), int(self.center_y)), (0, 0, 255), cv2.MARKER_CROSS, 20, 2)

        error_x, error_y = None, None

        for r in results:
            if len(r.boxes) > 0:
                box = r.boxes[0]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                person_cx = (x1 + x2) // 2
                person_cy = (y1 + y2) // 2
                
                raw_error_x = person_cx - self.center_x
                raw_error_y = person_cy - self.center_y

                error_x = raw_error_x / self.center_x
                error_y = -(raw_error_y / self.center_y)
                
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(annotated_frame, (person_cx, person_cy), 5, (0, 255, 0), -1)
                cv2.line(annotated_frame, (int(self.center_x), int(self.center_y)), (person_cx, person_cy), (0, 255, 255), 2)
                
                cv2.putText(annotated_frame, f"Blad X: {error_x:.2f} | Blad Y: {error_y:.2f}", (20, 90), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # FPS 
        fps = 1 / (time.time() - start_time)
        cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        return error_x, error_y, annotated_frame
