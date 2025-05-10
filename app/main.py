import sys
import datetime
from PyQt5 import QtWidgets
from app.login_window import LoginWindow
from app.main_window import MainWindow
from app.user import UserManager
from app.livestream import LivestreamManager
from app.scheduler import LivestreamScheduler
from app.logger import LivestreamLogger
from app.encryption import encrypt_message, decrypt_message

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Auto Livestreaming")
        self.user_manager = UserManager()
        self.livestream_manager = LivestreamManager()
        self.logger = LivestreamLogger()
        self.scheduler = LivestreamScheduler(self.start_scheduled_livestream)

        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.handle_login)
        self.login_window.register_requested.connect(self.show_register_dialog)

        self.main_window = MainWindow()
        self.main_window.start_livestream.connect(self.start_livestream)
        self.main_window.stop_livestream.connect(self.stop_livestream)
        self.main_window.schedule_livestream.connect(self.schedule_livestream)
        self.main_window.cancel_schedule.connect(self.cancel_schedule)

        self.setCentralWidget(self.login_window)

        self.current_user = None

    def handle_login(self, username):
        # For simplicity, password is not passed here; in real app, handle securely
        # Here, just accept login for demonstration
        self.current_user = username
        self.logger.log(f"User {username} logged in")
        self.setCentralWidget(self.main_window)

    def show_register_dialog(self):
        username, ok1 = QtWidgets.QInputDialog.getText(self, "Register", "Enter username:")
        if not ok1 or not username:
            return
        password, ok2 = QtWidgets.QInputDialog.getText(self, "Register", "Enter password:", QtWidgets.QLineEdit.Password)
        if not ok2 or not password:
            return
        success = self.user_manager.register_user(username, password)
        if success:
            QtWidgets.QMessageBox.information(self, "Success", "User registered successfully")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Registration failed")

    def start_livestream(self):
        stream_key = self.main_window.stream_key_input.text()
        video_path = self.main_window.video_path
        if not stream_key or not video_path:
            QtWidgets.QMessageBox.warning(self, "Error", "Stream key and video must be provided")
            return
        rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"
        if not self.livestream_manager.validate_stream_key(rtmp_url):
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid stream key")
            return
        try:
            self.livestream_manager.start_livestream(video_path, rtmp_url)
            self.logger.log("Livestream started")
            self.main_window.append_log("Livestream started")
        except Exception as e:
            self.logger.log(f"Error starting livestream: {e}")
            self.main_window.append_log(f"Error starting livestream: {e}")

    def stop_livestream(self):
        self.livestream_manager.stop_livestream()
        self.logger.log("Livestream stopped")
        self.main_window.append_log("Livestream stopped")

    def schedule_livestream(self, datetime_obj):
        self.scheduler.schedule(datetime_obj)
        self.logger.log(f"Livestream scheduled for {datetime_obj}")
        self.main_window.append_log(f"Livestream scheduled for {datetime_obj}")

    def cancel_schedule(self):
        self.scheduler.cancel()
        self.logger.log("Livestream schedule cancelled")
        self.main_window.append_log("Livestream schedule cancelled")

    def start_scheduled_livestream(self):
        self.logger.log("Starting scheduled livestream")
        self.main_window.append_log("Starting scheduled livestream")
        self.start_livestream()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
