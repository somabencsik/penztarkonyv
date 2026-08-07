from datetime import datetime

from PySide6.QtCore import QDate, Qt, Slot, Signal
from PySide6.QtWidgets import (
    QDateTimeEdit,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src import config
from src.utils import create_centered_label, create_spin_box
from src.summary_page import SummaryMonthRow


class MonthlyPage(QWidget):

    INCOME_COLUMN_WIDTH = [50, 140, 80, 220, 100, 100, 100, 100]
    EXPENSE_COLUMN_WIDTH = [50, 140, 100, 100, 100, 100]
    INCOME_SERIAL_NUMBER = 0
    EXPENSE_SERIAL_NUMBER = 0

    def __init__(self, year: int, month: str) -> None:
        super().__init__()
        self.year = year
        self.month = month

        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        title = QLabel(self.month)
        title.setAlignment(Qt.AlignmentFlag.AlignRight)
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.tabBar().setExpanding(True)
        tabs.setStyleSheet("QTabBar::tab { width: 420px }")
        income_tab = self.income_tab_widget()
        expense_tab = self.expense_tab_widget()
        tabs.addTab(income_tab, "Bevétel")
        tabs.addTab(expense_tab, "Kiadás")

        layout.addWidget(tabs)

        self.setLayout(layout)

    def income_tab_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setSpacing(4)

        header_labels = []
        headers = [
            "Sorszám",
            "Dátum",
            "Bizonylat szám",
            "Név",
            "Értékesítés",
            "Egyéb",
            "Adóalapjába be nem számító bevétel",
            "Összesen",
        ]

        for col, text in enumerate(headers):
            label_width = self.INCOME_COLUMN_WIDTH[col]
            if col == 5:
                label_width -= 20
            if col == 6:
                label_width += 25
            lbl = create_centered_label(text, label_width)
            header_layout.addWidget(lbl)#, 0, col)
            header_labels.append(lbl)

        layout.addWidget(header_widget)

        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.Shape.HLine)
        horizontal_line.setFrameShadow(QFrame.Shadow.Plain)
        layout.addWidget(horizontal_line)

        income_widget = QWidget()

        income_scroll_area = QScrollArea()
        income_scroll_area.setWidgetResizable(True)
        income_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.income_layout = QGridLayout(income_widget)
        self.income_layout.setSpacing(4)
        self.income_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        income_scroll_area.setWidget(income_widget)
        layout.addWidget(income_scroll_area)

        btn_add = QPushButton("Bevétel Hozzáadás")
        btn_add.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        btn_add.pressed.connect(self.add_income)
        layout.addWidget(btn_add, 0, Qt.AlignmentFlag.AlignCenter)

        self.add_income()

        widget.setLayout(layout)
        return widget

    def expense_tab_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        header_widget = QWidget()
        header_layout = QGridLayout(header_widget)
        header_layout.setSpacing(4)

        header_labels = []
        headers = [
            "Sorszám",
            "Dátum",
            "Anyag árú",
            "Egyéb",
            "Közvetített szolgáltatás",
            "Összesen"
        ]
        for col, text in enumerate(headers):
            lbl = create_centered_label(text, self.EXPENSE_COLUMN_WIDTH[col])

            header_layout.addWidget(lbl, 0, col)
            header_labels.append(lbl)

        layout.addWidget(header_widget)

        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.Shape.HLine)
        horizontal_line.setFrameShadow(QFrame.Shadow.Plain)
        layout.addWidget(horizontal_line)

        expense_widget = QWidget()

        expense_scroll_area = QScrollArea()
        expense_scroll_area.setWidgetResizable(True)
        expense_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.expense_layout = QGridLayout(expense_widget)
        self.expense_layout.setSpacing(4)
        self.expense_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        expense_scroll_area.setWidget(expense_widget)
        layout.addWidget(expense_scroll_area)

        btn_add = QPushButton("Kiadás Hozzáadás")
        btn_add.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        btn_add.pressed.connect(self.add_expense)
        layout.addWidget(btn_add, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.add_expense()

        widget.setLayout(layout)
        return widget

    def add_income(self) -> None:
        new_widget = MonthlyIncomeWidget(
            self.year,
            self.month,
            self.INCOME_SERIAL_NUMBER,
            self.INCOME_COLUMN_WIDTH
        )
        new_widget.update_summary.connect(self.update_summary_page)
        self.income_layout.addWidget(new_widget)
        self.INCOME_SERIAL_NUMBER += 1

    def add_expense(self) -> None:
        new_widget = MonthlyExpanseWidget(
            self.year,
            self.month,
            self.EXPENSE_SERIAL_NUMBER,
            self.EXPENSE_COLUMN_WIDTH
        )
        new_widget.update_summary.connect(self.update_summary_page)
        self.expense_layout.addWidget(new_widget)
        self.EXPENSE_SERIAL_NUMBER += 1

    @Slot()
    def update_summary_page(self) -> None:
        for summary_month in SummaryMonthRow.objects:
            monthly_income = 0
            monthly_support = 0
            for monthly in MonthlyIncomeWidget.objects:
                if summary_month.month != monthly.month:
                    continue
                monthly_income += monthly.price.value() + monthly.other.value()
                monthly_support += monthly.non_tax.value()
            summary_month.income.setValue(monthly_income)
            summary_month.support.setValue(monthly_support)

            monthly_expense = 0
            for monthly in MonthlyExpanseWidget.objects:
                if summary_month.month != monthly.month:
                    continue
                monthly_expense += (
                        monthly.material_price.value() + monthly.other.value() + monthly.transmit_price.value()
                )
            summary_month.expense.setValue(monthly_expense)


class MonthlyIncomeWidget(QWidget):

    objects = []
    update_summary = Signal()

    def __init__(self, year: int, month: str, serial_number: int, column_width: list[int]) -> None:
        super().__init__()
        self.year = year
        self.month = month
        self.serial_number = serial_number
        self.column_width = column_width

        self.setup_ui()
        MonthlyIncomeWidget.objects.append(self)

    def setup_ui(self) -> None:
        layout = QHBoxLayout()

        serial_label = QLabel(str(self.serial_number).rjust(3, "0"))
        serial_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        serial_label.setFixedWidth(self.column_width[0])
        layout.addWidget(serial_label)

        today_date = datetime.now()
        today_date = QDate(self.year, [i for i, month in config.MONTHS.items() if self.month == month][0], today_date.day)
        date_widget = QDateTimeEdit(today_date)
        date_widget.setFixedWidth(self.column_width[1])
        layout.addWidget(date_widget)

        layout.addWidget(create_spin_box(self.column_width[2]))

        title_input = QLineEdit()
        title_input.setFixedWidth(self.column_width[3])
        layout.addWidget(title_input)

        self.price = create_spin_box(self.column_width[4])
        self.price.valueChanged.connect(self.price_changed)

        self.other = create_spin_box(self.column_width[5])
        self.other.valueChanged.connect(self.price_changed)

        self.non_tax = create_spin_box(self.column_width[6])
        self.non_tax.valueChanged.connect(self.price_changed)

        self.summary = create_spin_box(self.column_width[7], allow_minus=True)
        self.summary.valueChanged.connect(self.price_changed)

        layout.addWidget(self.price)
        layout.addWidget(self.other)
        layout.addWidget(self.non_tax)
        layout.addSpacing(20)
        layout.addWidget(self.summary)

        self.setLayout(layout)

    @Slot()
    def price_changed(self):
        self.summary.setValue(self.price.value() + self.other.value() + self.non_tax.value())
        self.update_summary.emit()


class MonthlyExpanseWidget(QWidget):
    
    objects = []
    update_summary = Signal()

    def __init__(self, year: int, month: str, serial_number: int, column_width: list[int]) -> None:
        super().__init__()
        self.year = year
        self.month = month
        self.serial_number = serial_number
        self.column_width = column_width

        self.setup_ui()
        MonthlyExpanseWidget.objects.append(self)

    def setup_ui(self) -> None:
        layout = QHBoxLayout()

        serial_label = QLabel(str(self.serial_number).rjust(3, "0"))
        serial_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        serial_label.setFixedWidth(self.column_width[0])
        layout.addWidget(serial_label)

        today_date = datetime.now()
        today_date = QDate(self.year, [i for i, month in config.MONTHS.items() if self.month == month][0], today_date.day)
        date_widget = QDateTimeEdit(today_date)
        date_widget.setFixedWidth(self.column_width[1])
        layout.addWidget(date_widget)

        self.material_price = create_spin_box(self.column_width[2])
        self.material_price.valueChanged.connect(self.price_changed)

        self.other = create_spin_box(self.column_width[3])
        self.other.valueChanged.connect(self.price_changed)

        self.transmit_price = create_spin_box(self.column_width[4])
        self.transmit_price.valueChanged.connect(self.price_changed)

        self.summary = create_spin_box(self.column_width[5])
        self.summary.valueChanged.connect(self.price_changed)


        layout.addWidget(self.material_price)
        layout.addWidget(self.other)
        layout.addWidget(self.transmit_price)
        layout.addSpacing(20)
        layout.addWidget(self.summary)

        self.setLayout(layout)

    @Slot()
    def price_changed(self) -> None:
        summary = self.material_price.value() + self.other.value() + self.transmit_price.value()
        summary = min(2_000_000_000, summary)
        self.summary.setValue(summary)
        self.update_summary.emit()
