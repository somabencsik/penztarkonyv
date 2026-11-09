import os
from xml.sax.saxutils import escape

from PySide6.QtCore import QDate
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.db import read_db

INCOME_HEADER = ["Sorszám", "Év", "Hó", "Nap", "Bizonylat szám", "Név", "Értékesítés", "Egyéb", "Nem adóalap", "Összesen"]
INCOME_KEYS = ["certificate_number", "title", "price", "other", "non-tax", "summary"]

EXPENSE_HEADER = ["Sorszám", "Év", "Hó", "Nap", "Anyag árú", "Egyéb", "Közvetített szolgáltatás", "Összesen"]
EXPENSE_KEYS = ["material_price", "other", "transmit_price", "summary"]


# ---------------------------------------------------------------- fonts
# Helvetica (the ReportLab default) cannot print ő and ű, so we try to register
# a TrueType font that can. If none is found, we fall back to Helvetica.
FONT_CANDIDATES = [
    # macOS
    ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf"),
    # Linux
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    # Windows
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    # Local copy next to the script / working directory
    ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"),
]


def register_fonts() -> tuple[str, str]:
    for regular_path, bold_path in FONT_CANDIDATES:
        if os.path.exists(regular_path) and os.path.exists(bold_path):
            pdfmetrics.registerFont(TTFont("AppFont", regular_path))
            pdfmetrics.registerFont(TTFont("AppFont-Bold", bold_path))
            return "AppFont", "AppFont-Bold"
    print("Warning: no Unicode TTF font found, falling back to Helvetica (ő and ű may not print).")
    return "Helvetica", "Helvetica-Bold"


FONT_REGULAR, FONT_BOLD = register_fonts()

CELL_STYLE = ParagraphStyle("cell", fontName=FONT_REGULAR, fontSize=7.5, leading=9)
HEADER_STYLE = ParagraphStyle("hdr", parent=CELL_STYLE, fontName=FONT_BOLD)
TITLE_STYLE = ParagraphStyle("title", fontName=FONT_BOLD, fontSize=18, leading=22, spaceAfter=10)
SECTION_STYLE = ParagraphStyle("section", fontName=FONT_BOLD, fontSize=13, leading=16, spaceBefore=6, spaceAfter=6)
NORMAL_STYLE = ParagraphStyle("normal", fontName=FONT_REGULAR, fontSize=10, leading=12)

# Fixed widths in points for the narrow columns (serial, year, month, day) = 116 pt
DATE_COLS = [38, 30, 24, 24]


def income_col_widths(total: float) -> list[float]:
    # certificate no., sales, other, non-tax, total
    fixed = [62, 58, 52, 58, 60]
    name_w = total - sum(DATE_COLS) - sum(fixed)  # "Név" takes the remaining space
    return [*DATE_COLS, fixed[0], name_w, *fixed[1:]]


def expense_col_widths(total: float) -> list[float]:
    amount_w = (total - sum(DATE_COLS)) / 4  # 4 equal amount columns
    return [*DATE_COLS, *[amount_w] * 4]


def build_row(record: dict, keys: list[str]) -> list[str]:
    """Serial + year/month/day + the remaining values."""
    date = QDate.fromString(record["date"])
    return [
        str(record["serial"]).rjust(3, "0"),
        str(date.year()),
        str(date.month()),
        str(date.day()),
        *(str(record[key]) for key in keys),
    ]


def build_table(header: list[str], rows: list[list[str]], col_widths: list[float]) -> Table:
    # Paragraph cells wrap inside their column instead of overflowing
    data = [[Paragraph(escape(h), HEADER_STYLE) for h in header]]
    data += [[Paragraph(escape(cell), CELL_STYLE) for cell in row] for row in rows]

    table = Table(data, colWidths=col_widths, repeatRows=1)  # header repeats on every page
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return table


def create_pdf(year: str, months: list[str], output_path: str, user: str) -> None:
    db = read_db()[user]

    user_path = os.path.join(output_path, user, f"{year}.pdf")
    os.makedirs(os.path.dirname(user_path), exist_ok=True)

    doc = SimpleDocTemplate(
        user_path,
        pagesize=A4,  # portrait: short side on top and bottom
        title=f"{user} - {year}",
        leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30,
    )
    income_expenses = db[year]
    story = []

    for index, month in enumerate(months):
        if index > 0:
            story.append(PageBreak())  # every month starts on a new page

        story.append(Paragraph(escape(f"{year} - {month}"), TITLE_STYLE))

        income_rows = [build_row(r, INCOME_KEYS) for r in income_expenses["Income"][month]]
        expense_rows = [build_row(r, EXPENSE_KEYS) for r in income_expenses["Expenses"][month]]

        story.append(Paragraph("Bevételek", SECTION_STYLE))
        income_table = build_table(INCOME_HEADER, income_rows, income_col_widths(doc.width))
        if not income_rows:
            income_table = Paragraph("Nincs adat", NORMAL_STYLE)
        story.append(income_table)

        story.append(Spacer(1, 20))

        story.append(Paragraph("Kiadások", SECTION_STYLE))
        expense_table = build_table(EXPENSE_HEADER, expense_rows, expense_col_widths(doc.width))
        if not expense_rows:
            expense_table = Paragraph("Nincs adat", NORMAL_STYLE)
        story.append(expense_table)

    doc.build(story)