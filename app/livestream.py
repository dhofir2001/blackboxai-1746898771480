import subprocess
import threading

class LivestreamManager:
    def __init__(self):
        self.process = None
        self.lock = threading.Lock()

    def start_livestream(self, video_path: str, rtmp_url: str):
        with self.lock:
            if self.process is not None:
                raise RuntimeError("Livestream already running")
            command = [
                "ffmpeg",
                "-re",
                "-stream_loop", "-1",
                "-i", video_path,
                "-c", "copy",
                "-f", "flv",
                rtmp_url
            ]
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stop_livestream(self):
        with self.lock:
            if self.process is not None:
                self.process.terminate()
                self.process.wait()
                self.process = None

    def is_running(self):
        with self.lock:
            return self.process is not None and self.process.poll() is None

    def validate_stream_key(self, rtmp_url: str) -> bool:
        # Basic validation could be checking if rtmp_url starts with rtmp://
        return rtmp_url.startswith("rtmp://")
