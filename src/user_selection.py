from datetime import datetime

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from src.utils import create_centered_label


class UserSelection(QWidget):

    add_user_to_db = Signal(str)
    switch_to_input_page = Signal(str, int)

    def __init__(self, users: list[str]) -> None:
        super().__init__()
        self.users = users

        self.setup_ui()

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout()
        user_select = QVBoxLayout()

        user_select.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        user_select.addWidget(create_centered_label("Válasszon évszámot", align_center=True))
        self.date_selector = QComboBox()
        self.date_selector.addItems([f"{y}" for y in range(1950, 2150)])
        self.date_selector.setCurrentText(f"{datetime.now().year}")
        user_select.addWidget(self.date_selector)

        user_select.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        user_select.addWidget(create_centered_label("Válasszon felhasználót", align_center=True))
        self.user_selector = QComboBox()
        self.user_selector.addItems(self.users)
        user_select.addWidget(self.user_selector)
        user_select.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        new_user = QVBoxLayout()

        new_user.addWidget(create_centered_label("Felhasználó hozzáadása", align_center=True))
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Felhasználó neve:"))
        self.user_input = QLineEdit()
        input_layout.addWidget(self.user_input)
        new_user.addLayout(input_layout)
        user_select.addLayout(new_user)
        btn_add_user = QPushButton("Hozzáadás")
        btn_add_user.pressed.connect(self.add_user)
        user_select.addWidget(btn_add_user)

        user_select.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        date_select = QVBoxLayout()
        date_select.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        date_select.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        main_layout.addLayout(user_select, stretch=1)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        btn_go_to_input_page = QPushButton("GO")
        btn_go_to_input_page.pressed.connect(self.go_to_input_page)
        main_layout.addWidget(btn_go_to_input_page)

        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(main_layout)

    @Slot()
    def add_user(self) -> None:
        new_user = self.user_input.text()
        if new_user.strip() == "":
            return
        self.add_user_to_db.emit(new_user)
        self.user_selector.addItem(new_user)

    @Slot()
    def go_to_input_page(self) -> None:
        self.switch_to_input_page.emit(self.user_selector.currentText(), int(self.date_selector.currentText()))
