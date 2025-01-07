import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QVBoxLayout, QWidget, QLabel, QGraphicsDropShadowEffect,
                            QSystemTrayIcon, QMenu, QMenuBar,
                             QStatusBar, QStyle)
from PySide6.QtCore import (Qt, QTimer, QPropertyAnimation, QPoint, QPointF,
                          QEasingCurve, QSize, QRectF)
from PySide6.QtGui import (QFont, QColor, QPainter, QPainterPath, QPen, QTransform,
                          QLinearGradient, QRadialGradient, QIcon, QAction)
import subprocess

class DuckLogo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 計算中心點和尺寸
        center = self.rect().center()
        size = min(self.width(), self.height()) - 20
        
        # 1. 繪製頭部（白色圓形）
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor('white'))
        head_rect = QRectF(center.x() - size/2, center.y() - size/2, size, size)
        painter.drawEllipse(head_rect)
        
        # 2. 繪製嘴巴
        beak_path = QPainterPath()
        
        # 修改嘴巴的大小和位置
        beak_width = size * 0.5  # 加寬
        beak_height = size * 0.25  # 降低高度
        beak_x = center.x() - beak_width/2
        beak_y = center.y() + size * 0.05  # 位置微調
        
        # 上嘴（較小）
        upper_beak = QRectF(beak_x, beak_y - beak_height/2, 
                           beak_width, beak_height)
        
        # 下嘴（較大）
        lower_beak = QRectF(beak_x - beak_width * 0.05, beak_y,
                           beak_width * 1.1, beak_height)
        
        # 先畫下嘴
        painter.setBrush(QColor(255, 140, 0))  # 橙色
        painter.drawEllipse(lower_beak)
        
        # 再畫上嘴
        painter.drawEllipse(upper_beak)
        
        # 3. 繪製眼睛
        painter.setBrush(QColor('black'))
        eye_size = size * 0.08
        eye_spacing = size * 0.2  # 眼睛之間的間距
        
        # 左眼
        left_eye_x = center.x() - eye_spacing/2
        eye_y = center.y() - size * 0.15  # 往上移
        painter.drawEllipse(QPointF(left_eye_x, eye_y), eye_size, eye_size)
        
        # 右眼
        right_eye_x = center.x() + eye_spacing/2
        painter.drawEllipse(QPointF(right_eye_x, eye_y), eye_size, eye_size)
        
        # 4. 為每個眼睛添加高光
        painter.setBrush(QColor('white'))
        highlight_size = eye_size * 0.3
        
        # 左眼高光
        painter.drawEllipse(QPointF(left_eye_x + eye_size * 0.2, eye_y - eye_size * 0.2),
                          highlight_size, highlight_size)
                          
        # 右眼高光
        painter.drawEllipse(QPointF(right_eye_x + eye_size * 0.2, eye_y - eye_size * 0.2),
                          highlight_size, highlight_size)

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(600, 400)
        
        # 設定視窗居中
        screen = QApplication.primaryScreen().geometry()
        self.move(
            screen.center().x() - self.width() // 2,
            screen.center().y() - self.height() // 2
        )
        
        # 創建並定位 Logo
        self.logo = DuckLogo(self)
        self.logo.setGeometry((self.width() - 200) // 2, 50, 200, 200)
        
        # 創建標籤
        self.label_title = QLabel("TRADY", self)
        self.label_description = QLabel("Use Trady, Trade Easy", self)
        
        # 設定字體
        title_font = QFont("Arial", 48, QFont.Bold)
        desc_font = QFont("Arial", 18)
        
        self.label_title.setFont(title_font)
        self.label_description.setFont(desc_font)
        
        # 設定樣式
        style = """
            QLabel {
                color: white;
                background-color: transparent;
            }
        """
        self.label_title.setStyleSheet(style)
        self.label_description.setStyleSheet(style)
        
        # 添加陰影效果
        self.add_shadow_effect(self.label_title)
        self.add_shadow_effect(self.label_description)
        
        # 初始隱藏文字
        self.label_title.hide()
        self.label_description.hide()
        
        # 設定位置
        self.label_title.move((self.width() - self.label_title.width()) // 2, 250)
        self.label_description.move(800, 320)  # 初始在右側外
        
        # 設定初始不透明度
        self.setWindowOpacity(0)
        
        # 開始動畫序列
        QTimer.singleShot(100, self.start_animation_sequence)
    
    def add_shadow_effect(self, widget):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 180))
        widget.setGraphicsEffect(shadow)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 180))
        gradient.setColorAt(1, QColor(0, 0, 0, 140))
        painter.fillRect(self.rect(), gradient)
    
    def start_animation_sequence(self):
        # 1. 整體淡入（包含鴨子）
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(1000)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.start()
        
        # 2. 等待後顯示標題
        QTimer.singleShot(0, self.show_title)
        
        # 3. 顯示描述
        QTimer.singleShot(1000, self.show_description)
        
        # 4. 結束動畫
        QTimer.singleShot(4000, self.finish_splash)
    
    def show_title(self):
        self.label_title.show()
        self.title_anim = QPropertyAnimation(self.label_title, b"pos")
        self.title_anim.setDuration(1000)
        self.title_anim.setStartValue(QPoint(-300, 250))
        self.title_anim.setEndValue(QPoint((self.width() - self.label_title.width()) // 2, 250))
        self.title_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.title_anim.start()
    
    def show_description(self):
        self.label_description.show()
        self.desc_anim = QPropertyAnimation(self.label_description, b"pos")
        self.desc_anim.setDuration(1000)
        self.desc_anim.setStartValue(QPoint(800, 320))
        self.desc_anim.setEndValue(QPoint((self.width() - self.label_description.width()) // 2, 320))
        self.desc_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.desc_anim.start()
    
    def finish_splash(self):
        self.fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out.setDuration(1000)
        self.fade_out.setStartValue(1)
        self.fade_out.setEndValue(0)
        self.fade_out.finished.connect(self.show_main_window)
        self.fade_out.start()
    
    def show_main_window(self):
        self.main_window = Launcher()
        self.main_window.show()
        self.close()

class StyledButton(QPushButton):
    def __init__(self, text, icon_name=None, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(50)
        self.setMinimumWidth(250)
        if icon_name:
            icon = self.style().standardIcon(getattr(QStyle.StandardPixmap, icon_name))
            self.setIcon(icon)
        self.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #424242, stop: 1 #323232);
                border: none;
                border-radius: 5px;
                padding: 10px;
                color: white;
                font-size: 14px;
                text-align: left;
                padding-left: 20px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #4a4a4a, stop: 1 #404040);
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
        """)

class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trady")
        self.setFixedSize(400, 500)
        self.init_ui()
        
    def init_ui(self):
        # 設定整體樣式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: white;
                font-size: 16px;
            }
            QStatusBar {
                color: #888888;
            }
            QMenuBar {
                background-color: #1e1e1e;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #3e3e3e;
            }
        """)
        
        # 建立菜單欄
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        settings_menu = menubar.addMenu('Settings')
        help_menu = menubar.addMenu('Help')
        
        # 添加菜單項目
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        about_action = QAction('About', self)
        help_menu.addAction(about_action)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Logo
        logo_label = DuckLogo(self)
        logo_label.setFixedSize(120, 120)
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        
        # 版本標籤
        version_label = QLabel("Trady Trading Suite")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # 添加一些空間
        layout.addSpacing(20)
        
        # 按鈕
        crypto_btn = StyledButton("CryptoKeeper", "SP_DialogSaveButton")
        crypto_btn.clicked.connect(lambda: self.start_program('python digital_legacy_safe/main.py'))
        layout.addWidget(crypto_btn)
        
        macro_btn = StyledButton("Makro", "SP_CommandLink")
        macro_btn.clicked.connect(lambda: self.start_program('python path/to/macro_tool/main.py'))
        layout.addWidget(macro_btn)
        
        asset_btn = StyledButton("AssetTracker", "SP_FileDialogContentsView")
        asset_btn.clicked.connect(lambda: self.start_program('python path/to/asset_tracker/main.py'))
        layout.addWidget(asset_btn)
        
        layout.addStretch()
        
        # 狀態列
        status = QStatusBar()
        self.setStatusBar(status)
        status.showMessage('Version 1.0.0')
        
        # 系統托盤
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(app.quit)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
    
    def start_program(self, path):
        try:
            subprocess.Popen(path.split())
            self.statusBar().showMessage(f'Starting {path.split("/")[-1]}...', 3000)
        except Exception as e:
            self.statusBar().showMessage(f'Error: {str(e)}', 5000)
    
    def closeEvent(self, event):
        self.hide()
        event.ignore()  # 不真正關閉程式，而是最小化到托盤

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec())