from PyQt5.QtCore import QTimer, QDateTime
import datetime

class LivestreamScheduler:
    def __init__(self, start_callback):
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_schedule)
        self.start_callback = start_callback
        self.scheduled_time = None

    def schedule(self, datetime_obj: datetime.datetime):
        self.scheduled_time = datetime_obj
        self.timer.start(60000)  # check every 60 seconds

    def cancel(self):
        self.timer.stop()
        self.scheduled_time = None

    def check_schedule(self):
        if self.scheduled_time is None:
            return
        now = datetime.datetime.now()
        if now >= self.scheduled_time:
            self.timer.stop()
            self.scheduled_time = None
            self.start_callback()
