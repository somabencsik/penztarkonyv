import os

MONTHS = {
    1: "Január",
    2: "Február",
    3: "Március",
    4: "Április",
    5: "Május",
    6: "Június",
    7: "Július",
    8: "Augusztus",
    9: "Szeptember",
    10: "Október",
    11: "November",
    12: "December"
}

DB_PATH = os.path.join(os.path.expanduser("~"), ".penztarkonyv", "db.json")
DEFAULT_PDF_PATH = os.path.join(os.path.expanduser("~"), "Documents")