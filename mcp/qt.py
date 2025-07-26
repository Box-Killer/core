import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt

class ModernWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("现代桌面应用")
        self.setGeometry(100, 100, 600, 400) # x, y, width, height

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter) # 居中对齐

        title_label = QLabel("欢迎来到现代应用")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)

        description_label = QLabel("这是一个使用 PySide6 构建的示例窗口，展示美观的UI。")
        description_label.setFont(QFont("Segoe UI", 12))
        description_label.setAlignment(Qt.AlignCenter)

        button = QPushButton("点击我")
        button.setFont(QFont("Segoe UI", 14))
        button.setFixedSize(200, 50) # 固定按钮大小
        button.clicked.connect(self.on_button_click)

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(button, alignment=Qt.AlignCenter) # 按钮也居中

        self.setLayout(layout)

    def apply_styles(self):
        # 使用 QSS 应用样式，模拟网页效果
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5; /* 浅灰色背景 */
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #333;
                margin-bottom: 10px;
            }
            QLabel#title_label { /* 可以给特定标签ID设置样式 */
                color: #007bff; /* 蓝色标题 */
            }
            QPushButton {
                background-color: #007bff; /* 蓝色按钮 */
                color: white;
                border: none;
                border-radius: 8px; /* 圆角 */
                padding: 10px 20px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* 阴影 */
            }
            QPushButton:hover {
                background-color: #0056b3; /* 鼠标悬停变深 */
            }
            QPushButton:pressed {
                background-color: #004085; /* 点击时更深 */
            }
        """)
        # 也可以从外部文件加载 QSS
        # with open("styles.qss", "r") as f:
        #     self.setStyleSheet(f.read())

    def on_button_click(self):
        print("按钮被点击了！")
        # 可以在这里添加更多交互逻辑

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernWindow()
    window.show()
    sys.exit(app.exec())