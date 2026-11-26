import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QSlider,
    QDoubleSpinBox,
    QPushButton,
    QFrame,
    QGroupBox,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer
from Body import Body
from About import AboutWindow
from GraphWindow import GraphWindow

class HeatTransfer(QWidget):

    def __init__(self):
        super().__init__()
        self.about_window = AboutWindow()
        self.body_obj1 = None
        self.body_obj2 = None
        self.dt = 0.1         
        self.time_elapsed = 0.0
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_method)
        self.graph_window = GraphWindow(self)
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []
        self.setupUI()


    def setupUI(self):
        self.setWindowTitle("Heat Transfer Simulation")
        self.setMinimumSize(740, 480)
        self.resize(760, 500)

        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # -------------------------------------------------------------
        # Section 1: Visual representation of bodies, sliders & bridge
        # -------------------------------------------------------------
        visual_group = QGroupBox("Thermal System")
        visual_layout = QHBoxLayout(visual_group)
        visual_layout.setContentsMargins(15, 20, 15, 20)
        visual_layout.setSpacing(15)

        # Slider 1 (Left - Body 1 initial temperature, 0 to 200)
        slider1_container = QVBoxLayout()
        slider1_top_lbl = QLabel("200°C")
        slider1_top_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider1_top_lbl.setStyleSheet("font-size: 11px; color: #555;")

        self.slider1 = QSlider(Qt.Orientation.Vertical)
        self.slider1.setRange(0, 200)
        self.slider1.setValue(200)
        self.slider1.setTickPosition(QSlider.TickPosition.TicksRight)
        self.slider1.setTickInterval(50)
        self.slider1.setFixedHeight(140)

        slider1_bot_lbl = QLabel("0°C")
        slider1_bot_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider1_bot_lbl.setStyleSheet("font-size: 11px; color: #555;")

        slider1_container.addWidget(slider1_top_lbl)
        slider1_container.addWidget(self.slider1, alignment=Qt.AlignmentFlag.AlignCenter)
        slider1_container.addWidget(slider1_bot_lbl)

        # Bodies & Rod sub-container (Spacing 0 so rod connects directly to bodies)
        bodies_rod_container = QWidget()
        bodies_rod_layout = QHBoxLayout(bodies_rod_container)
        bodies_rod_layout.setContentsMargins(0, 0, 0, 0)
        bodies_rod_layout.setSpacing(0)

        # Body 1 (Left Rectangle - Red by default)
        self.body1 = QLabel("Body 1")
        self.body1.setFixedSize(140, 140)
        self.body1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1.setStyleSheet(
            """
            QLabel {
                background-color: #d32f2f;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #b71c1c;
                border-radius: 8px;
            }
            """
        )

        # Center Bridge Area (Conductivity spinbox above horizontal gray rod)
        bridge_container = QWidget()
        bridge_container.setFixedHeight(140)
        bridge_layout = QVBoxLayout(bridge_container)
        bridge_layout.setContentsMargins(0, 0, 0, 0)
        bridge_layout.setSpacing(0)

        # Conductivity control section (Above rod)
        cond_widget = QWidget()
        cond_widget.setFixedHeight(58)
        cond_layout = QVBoxLayout(cond_widget)
        cond_layout.setContentsMargins(10, 0, 10, 4)
        cond_layout.setSpacing(2)
        cond_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cond_label = QLabel("Conductivity")
        cond_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cond_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #333333;")

        self.spin_conductivity = QDoubleSpinBox()
        self.spin_conductivity.setRange(0.01, 1000.0)
        self.spin_conductivity.setDecimals(2)
        self.spin_conductivity.setSingleStep(0.1)
        self.spin_conductivity.setValue(1.00)
        self.spin_conductivity.setSuffix(" J/s°C")
        self.spin_conductivity.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_conductivity.setFixedWidth(130)

        cond_layout.addWidget(cond_label)
        cond_layout.addWidget(self.spin_conductivity)

        # Gray horizontal conducting rod/bridge (Connects Body 1 and Body 2)
        self.rod = QFrame()
        self.rod.setFixedHeight(24)
        self.rod.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.rod.setStyleSheet(
            """
            QFrame {
                background-color: #7f8c8d;
                border-top: 2px solid #5a6268;
                border-bottom: 2px solid #5a6268;
            }
            """
        )

        # Bottom space to balance conductivity controls and keep rod vertically centered
        bottom_balance = QWidget()
        bottom_balance.setFixedHeight(58)

        bridge_layout.addWidget(cond_widget)
        bridge_layout.addWidget(self.rod)
        bridge_layout.addWidget(bottom_balance)

        # Body 2 (Right Rectangle - Black by default)
        self.body2 = QLabel("Body 2")
        self.body2.setFixedSize(140, 140)
        self.body2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2.setStyleSheet(
            """
            QLabel {
                background-color: #212121;
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #000000;
                border-radius: 8px;
            }
            """
        )

        bodies_rod_layout.addWidget(self.body1)
        bodies_rod_layout.addWidget(bridge_container, stretch=1)
        bodies_rod_layout.addWidget(self.body2)

        # Slider 2 (Right - Body 2 initial temperature, 0 to 200)
        slider2_container = QVBoxLayout()
        slider2_top_lbl = QLabel("200°C")
        slider2_top_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider2_top_lbl.setStyleSheet("font-size: 11px; color: #555;")

        self.slider2 = QSlider(Qt.Orientation.Vertical)
        self.slider2.setRange(0, 200)
        self.slider2.setValue(0)
        self.slider2.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.slider2.setTickInterval(50)
        self.slider2.setFixedHeight(140)

        slider2_bot_lbl = QLabel("0°C")
        slider2_bot_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider2_bot_lbl.setStyleSheet("font-size: 11px; color: #555;")

        slider2_container.addWidget(slider2_top_lbl)
        slider2_container.addWidget(self.slider2, alignment=Qt.AlignmentFlag.AlignCenter)
        slider2_container.addWidget(slider2_bot_lbl)

        # Assemble visual section
        visual_layout.addLayout(slider1_container)
        visual_layout.addWidget(bodies_rod_container, stretch=1)
        visual_layout.addLayout(slider2_container)

        main_layout.addWidget(visual_group)

        # -------------------------------------------------------------
        # Section 2: Parameters & Center Control Buttons
        # -------------------------------------------------------------
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # --- Body 1 Parameters (Left Column) ---
        group_params1 = QGroupBox("Body 1 Parameters")
        form_params1 = QFormLayout(group_params1)
        form_params1.setContentsMargins(15, 15, 15, 15)
        form_params1.setSpacing(10)

        self.temp1_display = QLabel("200.0 °C")
        self.temp1_display.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.temp1_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temp1_display.setStyleSheet(
            """
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 4px;
                font-weight: bold;
                font-size: 13px;
                color: #212529;
            }
            """
        )

        self.spin_mass1 = QDoubleSpinBox()
        self.spin_mass1.setRange(0.01, 1000.0)
        self.spin_mass1.setDecimals(2)
        self.spin_mass1.setSingleStep(1.0)
        self.spin_mass1.setValue(10.00)
        self.spin_mass1.setSuffix(" kg")

        self.spin_hcap1 = QDoubleSpinBox()
        self.spin_hcap1.setRange(0.01, 100.0)
        self.spin_hcap1.setDecimals(2)
        self.spin_hcap1.setSingleStep(0.05)
        self.spin_hcap1.setValue(0.40)
        self.spin_hcap1.setSuffix(" J/kg°C")

        form_params1.addRow("Temp.:", self.temp1_display)
        form_params1.addRow("Mass:", self.spin_mass1)
        form_params1.addRow("H. Cap.:", self.spin_hcap1)

        bottom_layout.addWidget(group_params1, stretch=1)

        # --- Center Control Buttons ---
        controls_group = QGroupBox("Controls")
        controls_layout = QVBoxLayout(controls_group)
        controls_layout.setContentsMargins(15, 15, 15, 15)
        controls_layout.setSpacing(10)
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_start = QPushButton("Start")
        self.btn_start.setCheckable(True)
        self.btn_start.setFixedHeight(34)
        self.btn_start.setFixedWidth(120)
        self.btn_start.setStyleSheet(
            """
            QPushButton {
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:checked {
                background-color: #e67e22;
                color: white;
            }
            """
        )

        self.btn_graphs = QPushButton("Graphs")
        self.btn_graphs.setFixedHeight(34)
        self.btn_graphs.setFixedWidth(120)

        self.btn_about = QPushButton("About")
        self.btn_about.setFixedHeight(34)
        self.btn_about.setFixedWidth(120)

        controls_layout.addWidget(self.btn_start)
        controls_layout.addWidget(self.btn_graphs)
        controls_layout.addWidget(self.btn_about)

        bottom_layout.addWidget(controls_group, stretch=0)

        # --- Body 2 Parameters (Right Column) ---
        group_params2 = QGroupBox("Body 2 Parameters")
        form_params2 = QFormLayout(group_params2)
        form_params2.setContentsMargins(15, 15, 15, 15)
        form_params2.setSpacing(10)

        self.temp2_display = QLabel("0.0 °C")
        self.temp2_display.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.temp2_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temp2_display.setStyleSheet(
            """
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 4px;
                font-weight: bold;
                font-size: 13px;
                color: #212529;
            }
            """
        )

        self.spin_mass2 = QDoubleSpinBox()
        self.spin_mass2.setRange(0.01, 1000.0)
        self.spin_mass2.setDecimals(2)
        self.spin_mass2.setSingleStep(1.0)
        self.spin_mass2.setValue(10.00)
        self.spin_mass2.setSuffix(" kg")

        self.spin_hcap2 = QDoubleSpinBox()
        self.spin_hcap2.setRange(0.01, 100.0)
        self.spin_hcap2.setDecimals(2)
        self.spin_hcap2.setSingleStep(0.05)
        self.spin_hcap2.setValue(0.40)
        self.spin_hcap2.setSuffix(" J/kg°C")

        form_params2.addRow("Temp.:", self.temp2_display)
        form_params2.addRow("Mass:", self.spin_mass2)
        form_params2.addRow("H. Cap.:", self.spin_hcap2)

        bottom_layout.addWidget(group_params2, stretch=1)

        main_layout.addLayout(bottom_layout)

        # -------------------------------------------------------------
        # Signal Connections (UI Visual feedback)
        # -------------------------------------------------------------
        self.slider1.valueChanged.connect(self._on_slider1_changed)
        self.slider2.valueChanged.connect(self._on_slider2_changed)
        self.btn_start.toggled.connect(self._on_start_toggled)
        self.btn_graphs.clicked.connect(self.graph_window.show)


        self.btn_about.clicked.connect(self.about_window.show)

    def update_body_color(self, body_label, temp):
        red_val = int((temp / 200.0) * 255)
        red_val = max(0, min(255, red_val))
        body_label.setStyleSheet(f"""
            QLabel {{
                background-color: rgb({red_val}, 0, 0);
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 8px;
            }}
        """)

    def _on_slider1_changed(self, value: int):
        self.temp1_display.setText(f"{float(value):.1f} °C")
        self.update_body_color(self.body1, value)

    def _on_slider2_changed(self, value: int):
        self.temp2_display.setText(f"{float(value):.1f} °C")
        self.update_body_color(self.body2, value)

    def _on_start_toggled(self, checked: bool):
        if checked:
            self.btn_start.setText("Pause")
            self.time_elapsed = 0.0

            t1_init = float(self.slider1.value())
            t2_init = float(self.slider2.value())

            self.body_obj1 = Body(
                self.spin_mass1.value(),
                self.spin_hcap1.value(),
                t1_init
            )
            self.body_obj2 = Body(
                self.spin_mass2.value(),
                self.spin_hcap2.value(),
                t2_init
            )

            self.time_history = [0.0]
            self.body1_temp_history = [t1_init]
            self.body2_temp_history = [t2_init]

            self.timer.start(int(self.dt * 1000))
        else:
            self.btn_start.setText("Start")
            self.timer.stop()

    def timer_method(self):
        sigma = self.spin_conductivity.value()
        t1 = self.body_obj1.temperature
        t2 = self.body_obj2.temperature

        i1 = sigma * (t2 - t1)
        i2 = sigma * (t1 - t2)

        dq1 = i1 * self.dt
        dq2 = i2 * self.dt

        new_t1 = self.body_obj1.add_heat(dq1)
        new_t2 = self.body_obj2.add_heat(dq2)
        self.time_elapsed += self.dt

        self.temp1_display.setText(f"{new_t1:.1f} °C")
        self.temp2_display.setText(f"{new_t2:.1f} °C")
        self.update_body_color(self.body1, new_t1)
        self.update_body_color(self.body2, new_t2)

        self.slider1.blockSignals(True)
        self.slider1.setValue(int(round(new_t1)))
        self.slider1.blockSignals(False)

        self.slider2.blockSignals(True)
        self.slider2.setValue(int(round(new_t2)))
        self.slider2.blockSignals(False)

        self.time_history.append(self.time_elapsed)
        self.body1_temp_history.append(new_t1)
        self.body2_temp_history.append(new_t2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeatTransfer()
    window.show()
    sys.exit(app.exec())
