import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("About")
        self.setFixedSize(380, 450)
        self.setStyleSheet(
            """
            AboutWindow {
                background-color: #ffffff;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(30, 30, 30, 25)
        layout.setSpacing(14)

        self.image_label = QLabel()
        self.image_label.setFixedSize(160, 160)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet(
            """
            QLabel {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 4px;
            }
            """
        )

        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = None
        for candidate in ("Sea_turtle.jpg", "Sea_turtle.png"):
            full_path = os.path.join(script_dir, candidate)
            if os.path.exists(full_path):
                image_path = full_path
                break
            elif os.path.exists(candidate):
                image_path = candidate
                break

        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    150,
                    150,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self.image_label.setPixmap(scaled_pixmap)

        # 2. טקסט הסבר ופרטים - טיפוגרפיה מודרנית עם גווני חום/קור עדינים
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setText(
            """
            <div style='text-align: center;'>
                <div style='font-size: 18px; font-weight: 700; color: #c0392b; margin-bottom: 6px;'>
                    Heat Transfer Simulation
                </div>
                <div style='font-size: 13px; color: #64748b; font-weight: 500;'>
                    Developed by: <span style='color: #1e293b; font-weight: 600;'>Liel Eliyahu</span>
                </div>
            </div>
            """
        )

        # 3. לינק לחיץ ל-GitHub בעיצוב מודרני ונקי
        self.github_label = QLabel(
            '<a href="https://github.com/lielel32238" '
            'style="color: #0284c7; text-decoration: none; font-weight: 600; font-size: 13px;">'
            '🔗 My GitHub Repository'
            '</a>'
        )
        self.github_label.setOpenExternalLinks(True)
        self.github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.github_label.setStyleSheet(
            """
            QLabel {
                padding: 4px 8px;
                border-radius: 6px;
            }
            QLabel:hover {
                background-color: #f0f9ff;
            }
            """
        )

        # 4. כפתור סגירה (Close) מודרני ומעוצב
        self.close_button = QPushButton("Close")
        self.close_button.setFixedSize(120, 36)
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.setStyleSheet(
            """
            QPushButton {
                background-color: #f1f5f9;
                color: #334155;
                font-size: 13px;
                font-weight: 600;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #0f172a;
                border-color: #94a3b8;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
            }
            """
        )
        self.close_button.clicked.connect(self.close)

        # הוספת הרכיבים ל-Layout עם יישור מרכזי
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.github_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(8)
        layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AboutWindow()
    window.show()
    sys.exit(app.exec())
