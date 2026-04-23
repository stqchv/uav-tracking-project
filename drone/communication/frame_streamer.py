import subprocess

class FrameStreamer:
    def __init__(self, target_ip, port=5000, width=640, height=480, fps=30):
        self.target_ip = target_ip
        self.port = port
        self.width = width
        self.height = height
        self.fps = fps
        self.process = None

    def start(self):
        if self.process is not None:
            print("[STREAMER] Stream is already working.")
            return
        
        command = [
            "rpicam-vid",
            "-t", "0",
            "--width", str(self.width),
            "--height", str(self.height),
            "--framerate", str(self.fps),
            "--codec", "h264",
            "--inline",
            "-o", f"udp://{self.target_ip}:{self.port}"
        ]
        
        print(f"[STREAMER] Trying to connect to {self.target_ip}:{self.port}...")
        self.process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[STREAMER] Camera ready. Streaming...")

    def stop(self):
        if self.process:
            print("[STREAMER] Stopping camera...")
            self.process.terminate()
            self.process.wait()
            self.process = None
            print("[STREAMER] Camera stream end.")
