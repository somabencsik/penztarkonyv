from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from src.config import MONTHS
from src.db import read_db


class MonthSelectorWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.years = [year for _, yearly in read_db().items() for year in yearly]
        self.selected_months = []
        self.selected_year = ""
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Válassza ki a nyomtatni kívánt hónapokat"))

        self.dd_years = QComboBox()
        self.dd_years.addItems(self.years)
        layout.addWidget(QLabel("Év kiválasztása"))
        layout.addWidget(self.dd_years)

        for month in MONTHS.values():
            layout.addWidget(QCheckBox(month))

        btn_select_all = QPushButton("Összes kiválasztása")
        btn_select_all.pressed.connect(self.select_all)
        layout.addWidget(btn_select_all)
        btn_deselect_all = QPushButton("Összes kijelölés törlése")
        btn_deselect_all.pressed.connect(self.deselect_all)
        layout.addWidget(btn_deselect_all)
        btn_start = QPushButton("Készítés")
        btn_start.pressed.connect(self.start)
        layout.addWidget(btn_start)

        self.setLayout(layout)

    def select_all(self) -> None:
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if not isinstance(widget, QCheckBox):
                continue
            widget.setChecked(True)

    def deselect_all(self) -> None:
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if not isinstance(widget, QCheckBox):
                continue
            widget.setChecked(False)

    def start(self) -> None:
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if not isinstance(widget, QCheckBox):
                continue
            if widget.isChecked():
                self.selected_months.append(widget.text())
        self.selected_year = self.dd_years.currentText()
        self.accept()