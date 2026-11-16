import os

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from src.config import MONTHS, PATH_TO_SAVE_FILE
from src.db import read_db


def save_path(path: str) -> str:
    with open(PATH_TO_SAVE_FILE, "w") as f:
        f.write(path)


def read_path() -> str:
    if not os.path.exists(PATH_TO_SAVE_FILE):
        save_path(os.path.join(os.path.expanduser("~"), "Documents", "PenztarkonyvPDF"))
    with open(PATH_TO_SAVE_FILE, "r") as f:
        return f.read()


class MonthSelectorWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Hónap választás")

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

        path_layout = QHBoxLayout()
        self.path_to_save = QLineEdit()
        self.path_to_save.setText(read_path())
        btn_choose_path_to_save = QPushButton("Cél mappa kiválasztása")
        btn_choose_path_to_save.pressed.connect(self.choose_path_to_save)
        path_layout.addWidget(self.path_to_save)
        path_layout.addWidget(btn_choose_path_to_save)
        layout.addLayout(path_layout)

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

    def choose_path_to_save(self) -> None:
        dir_path = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Válassza ki a cél mappát!",
            options=QFileDialog.Option.DontUseNativeDialog,
        )
        if dir_path == "":
            return
        self.path_to_save.setText(dir_path)
        save_path(dir_path)