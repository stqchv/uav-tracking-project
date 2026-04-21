import cv2
import threading

class VideoStream:
    def __init__(self, port=5000):
        pipeline = (
            f"udpsrc port={port} ! "
            "h264parse ! "
            "avdec_h264 ! "
            "videoconvert ! "
            "video/x-raw,format=BGR ! "
            "appsink sync=false drop=true max-buffers=1"
        )

        self.cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        self.ret = False
        self.frame = None
        self.running = False

        if self.cap.isOpened():
            self.running = True

    def start(self):
        self.thread = threading.Thread(target=self.update, args=(), daemon=True)
        self.thread.start()
        return self
    
    def update(self):
        while self.running:
            if self.cap.isOpened():
                self.ret, self.frame = self.cap.read()

    def read(self):
        return self.ret, self.frame
    
    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        self.cap.release()
    

def start_video_stream(port=5000):
    print(f"Waiting for the stream on port {port}...")
    stream = VideoStream(port)
    
    if not stream.running:
        print("Error: Could not open stream.")
        return None
    
    print("Connected to video stream. Starting thread...")
    return stream.start()

def receive_frame(stream):
    return stream.read()