import sys
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trady")
        self.setGeometry(300, 300, 300, 200)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # button to start the CryptoKeeper program
        digital_legacy_btn = QPushButton("CryptoKeeper")
        digital_legacy_btn.clicked.connect(lambda: self.start_program('python digital_legacy_safe/main.py'))
        layout.addWidget(digital_legacy_btn)

        # button to start the MakroTrader program
        macro_btn = QPushButton("MakroTrader")
        macro_btn.clicked.connect(lambda: self.start_program('python path/to/macro_tool/main.py'))
        layout.addWidget(macro_btn)

        # button to start the AssetTracker program
        asset_tracker_btn = QPushButton("AssetTracker")
        asset_tracker_btn.clicked.connect(lambda: self.start_program('python path/to/asset_tracker/main.py'))
        layout.addWidget(asset_tracker_btn)

    def start_program(self, path):
        subprocess.Popen(path.split())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Launcher()
    window.show()
    sys.exit(app.exec())
