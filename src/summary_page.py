from PySide6.QtCore import Slot, Signal

from src.config import MONTHS
from src.utils import create_centered_label, create_spin_box

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy


class SummaryPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QHBoxLayout()

        monthly_summary_widget = SummaryMonthly()
        quarter_summary_widget = SummaryQuarters()

        layout.addWidget(monthly_summary_widget)
        layout.addWidget(quarter_summary_widget)

        self.setLayout(layout)


class SummaryMonthly(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        header_row = QHBoxLayout()
        header_row.addWidget(create_centered_label("Havi összes", set_bold=True))
        header_row.addWidget(create_centered_label("Bevétel", set_bold=True))
        header_row.addWidget(create_centered_label("Támogatás", set_bold=True))
        header_row.addWidget(create_centered_label("Kiadás", set_bold=True))
        header_row.addWidget(create_centered_label("Összes", set_bold=True))
        layout.addLayout(header_row)

        for _, month in MONTHS.items():
            new_widget = SummaryMonthRow(month)
            new_widget.update_quarter_summary.connect(self.update_quarter_summary)
            layout.addLayout(new_widget)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)

    @Slot()
    def update_quarter_summary(self) -> None:
        income_expense = {
            1: {"income": 0, "support": 0, "expense": 0},
            2: {"income": 0, "support": 0, "expense": 0},
            3: {"income": 0, "support": 0, "expense": 0},
            4: {"income": 0, "support": 0, "expense": 0}
        }
        for monthly in SummaryMonthRow.objects:
            if monthly.month in ("Január", "Február", "Március"):
                quarter_number = 1
            elif monthly.month in ("Április", "Május", "Június"):
                quarter_number = 2
            elif monthly.month in ("Július", "Augusztus", "Szeptember"):
                quarter_number = 3
            else:  # monthly.month in ("Október", "November", "December"):
                quarter_number = 4
            income_expense[quarter_number]["income"] += monthly.income.value()
            income_expense[quarter_number]["support"] += monthly.support.value()
            income_expense[quarter_number]["expense"] += monthly.expense.value()

        for summary in SummaryQuarterRow.objects:
            for quarter, summaries in income_expense.items():
                if quarter != summary.quarter:
                    continue
                summary.income.setValue(summaries["income"])
                summary.support.setValue(summaries["support"])
                summary.expense.setValue(summaries["expense"])


class SummaryMonthRow(QHBoxLayout):

    objects = []
    update_quarter_summary = Signal()

    def __init__(self, month: str) -> None:
        super().__init__()
        self.month = month
        self.setup_ui()

        SummaryMonthRow.objects.append(self)

    def setup_ui(self) -> None:
        self.addWidget(QLabel(self.month))
        self.income = create_spin_box()
        self.income.valueChanged.connect(self.value_changed)
        self.addWidget(self.income)
        self.support = create_spin_box()
        self.support.valueChanged.connect(self.value_changed)
        self.addWidget(self.support)
        self.expense = create_spin_box()
        self.expense.valueChanged.connect(self.value_changed)
        self.addWidget(self.expense)
        self.summary = create_spin_box(allow_minus=True)
        self.summary.valueChanged.connect(self.value_changed)
        self.addSpacing(20)
        self.addWidget(self.summary)

    @Slot()
    def value_changed(self) -> None:
        self.summary.setValue(self.income.value() + self.support.value() - self.expense.value())
        self.update_quarter_summary.emit()


class SummaryQuarters(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout()

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        header_row = QHBoxLayout()
        header_row.addWidget(create_centered_label("Negyedéves Összesen", set_bold=True, align_center=True))
        layout.addLayout(header_row)

        sub_header_row = QHBoxLayout()
        sub_header_row.addWidget(create_centered_label("", set_bold=True))
        sub_header_row.addWidget(create_centered_label("Bevétel", set_bold=True))
        sub_header_row.addWidget(create_centered_label("Támogatás", set_bold=True))
        sub_header_row.addWidget(create_centered_label("Kiadás", set_bold=True))
        sub_header_row.addWidget(create_centered_label("Összes", set_bold=True))
        layout.addLayout(sub_header_row)

        for i in range(4):
            layout.addLayout(SummaryQuarterRow(i + 1))

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(layout)


class SummaryQuarterRow(QHBoxLayout):

    objects = []

    def __init__(self, quarter: int) -> None:
        super().__init__()
        self.quarter = quarter
        self.setup_ui()

        SummaryQuarterRow.objects.append(self)

    def setup_ui(self) -> None:
        self.addWidget(QLabel(f"{self.quarter}. negyed év"))
        self.income = create_spin_box()
        self.income.valueChanged.connect(self.value_changed)
        self.addWidget(self.income)
        self.support = create_spin_box()
        self.support.valueChanged.connect(self.value_changed)
        self.addWidget(self.support)
        self.expense = create_spin_box()
        self.expense.valueChanged.connect(self.value_changed)
        self.addWidget(self.expense)
        self.summary = create_spin_box(allow_minus=True)
        self.summary.valueChanged.connect(self.value_changed)
        self.addSpacing(20)
        self.addWidget(self.summary)

    @Slot()
    def value_changed(self) -> None:
        self.summary.setValue(self.income.value() + self.support.value() - self.expense.value())