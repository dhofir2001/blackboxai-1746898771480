import datetime

class LivestreamLogger:
    def __init__(self):
        self.logs = []

    def log(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.logs.append(entry)
        print(entry)  # Also print to console for debugging

    def get_logs(self):
        return self.logs
