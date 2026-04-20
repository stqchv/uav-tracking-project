import cv2

def start_video_stream(port=5000):
    print(f"Waiting for the stream on port {port}...")

    pipeline = (
        f"udpsrc port={port} ! "
        "h264parse ! "
        "avdec_h264 ! "
        "videoconvert ! "
        "video/x-raw,format=BGR ! "
        "appsink sync=false drop=true max-buffers=1"
    )

    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Unable to recieve stream.")
        return None
    
    print("Connected to video stream.")
    return cap

def recieve_frame(cap):
    ret, frame = cap.read()
    return ret, frame