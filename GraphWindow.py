import sys
import csv
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QSizePolicy,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class GraphWindow(QWidget):

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Graph Window")
        self.resize(800, 500)
        self.setMinimumSize(700, 450)

        # Main horizontal layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # -------------------------------------------------------------
        # Left Side: Matplotlib Canvas
        # -------------------------------------------------------------
        self.figure = Figure(figsize=(6, 4), tight_layout=True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True, linestyle="--", alpha=0.6)

        main_layout.addWidget(self.canvas, stretch=4)

        # -------------------------------------------------------------
        # Right Side: Vertical Controls Column
        # -------------------------------------------------------------
        right_layout = QVBoxLayout()
        right_layout.setSpacing(12)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 1. Combo box to select body ("Body 1", "Body 2")
        self.body_combo = QComboBox()
        self.body_combo.addItems(["Body 1", "Body 2"])
        self.body_combo.setFixedHeight(34)
        self.body_combo.setMinimumWidth(140)

        # 2. Draw button
        self.btn_draw = QPushButton("Draw")
        self.btn_draw.setFixedHeight(34)

        # 3. Clear button
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setFixedHeight(34)

        # 4. Export to CSV button
        self.btn_export = QPushButton("Export to CSV")
        self.btn_export.setFixedHeight(34)

        # Apply consistent styling to right-side controls
        controls_style = """
            QComboBox {
                font-size: 13px;
                padding: 4px 10px;
                border: 1px solid #ced4da;
                border-radius: 6px;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QPushButton {
                font-size: 13px;
                font-weight: 600;
                border: 1px solid #ced4da;
                border-radius: 6px;
                background-color: #f8f9fa;
                color: #212529;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #adb5bd;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """
        self.body_combo.setStyleSheet(controls_style)
        self.btn_draw.setStyleSheet(controls_style)
        self.btn_clear.setStyleSheet(controls_style)
        self.btn_export.setStyleSheet(controls_style)

        right_layout.addWidget(self.body_combo)
        right_layout.addWidget(self.btn_draw)
        right_layout.addWidget(self.btn_clear)
        right_layout.addWidget(self.btn_export)
        right_layout.addStretch()

        main_layout.addLayout(right_layout, stretch=1)
        self.btn_draw.clicked.connect(self.draw_graph)
        self.btn_clear.clicked.connect(self.clear_graph)
        self.btn_export.clicked.connect(self.export_to_csv)

    def draw_graph(self):
        selected = self.body_combo.currentText()
        times = self.main_window.time_history

        if not times:
            return

        if selected == "Body 1":
           self.ax.plot(times, self.main_window.body1_temp_history, color="red", label="Body 1")
        elif selected == "Body 2":
            self.ax.plot(times, self.main_window.body2_temp_history, color="blue", label="Body 2")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.set_title("Heat Transfer Temperature vs. Time")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def clear_graph(self):
        self.ax.clear()
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True)
        self.canvas.draw()

    def export_to_csv(self):
        filename = "heat_transfer_results.csv"
        times = self.main_window.time_history
        t1_list = self.main_window.body1_temp_history
        t2_list = self.main_window.body2_temp_history
        with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["Time (s)", "Body 1 Temp (°C)", "Body 2 Temp (°C)"])
            for t, t1, t2 in zip(times, t1_list, t2_list):
                writer.writerow([round(t, 2), round(t1, 2), round(t2, 2)])
        os.startfile(filename)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    sys.exit(app.exec())
