from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import datetime

class MainWindow(QtWidgets.QWidget):
    start_livestream = QtCore.pyqtSignal()
    stop_livestream = QtCore.pyqtSignal()
    schedule_livestream = QtCore.pyqtSignal(datetime.datetime)
    cancel_schedule = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Auto Livestreaming")
        self.setFixedSize(600, 400)

        layout = QtWidgets.QVBoxLayout()

        # Stream Key Input
        self.stream_key_input = QtWidgets.QLineEdit()
        self.stream_key_input.setPlaceholderText("Enter YouTube Secret Stream Key")
        layout.addWidget(self.stream_key_input)

        # Video selection
        self.video_path_label = QtWidgets.QLabel("No video selected")
        layout.addWidget(self.video_path_label)
        self.select_video_button = QtWidgets.QPushButton("Select Video")
        self.select_video_button.clicked.connect(self.select_video)
        layout.addWidget(self.select_video_button)

        # Start/Stop buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton("Start Livestream")
        self.start_button.clicked.connect(self.start_livestream.emit)
        btn_layout.addWidget(self.start_button)
        self.stop_button = QtWidgets.QPushButton("Stop Livestream")
        self.stop_button.clicked.connect(self.stop_livestream.emit)
        btn_layout.addWidget(self.stop_button)
        layout.addLayout(btn_layout)

        # Scheduling
        schedule_layout = QtWidgets.QHBoxLayout()
        self.datetime_picker = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.datetime_picker.setCalendarPopup(True)
        schedule_layout.addWidget(self.datetime_picker)
        self.schedule_button = QtWidgets.QPushButton("Schedule Livestream")
        self.schedule_button.clicked.connect(self.handle_schedule)
        schedule_layout.addWidget(self.schedule_button)
        self.cancel_schedule_button = QtWidgets.QPushButton("Cancel Schedule")
        self.cancel_schedule_button.clicked.connect(self.cancel_schedule.emit)
        schedule_layout.addWidget(self.cancel_schedule_button)
        layout.addLayout(schedule_layout)

        # Log display
        self.log_display = QtWidgets.QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

        self.setLayout(layout)
        self.video_path = None

    def select_video(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi *.mov *.mkv)", options=options)
        if file_path:
            self.video_path = file_path
            self.video_path_label.setText(file_path)

    def handle_schedule(self):
        dt = self.datetime_picker.dateTime().toPyDateTime()
        if dt <= datetime.datetime.now():
            QMessageBox.warning(self, "Invalid Time", "Please select a future date and time for scheduling.")
            return
        self.schedule_livestream.emit(dt)

    def append_log(self, message: str):
        self.log_display.append(message)
