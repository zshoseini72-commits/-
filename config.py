from pathlib import Path

# پوشه اصلی پروژه
BASE_DIR = Path(__file__).resolve().parent

# پوشه داده‌ها
DATA_DIR = BASE_DIR / "data"

# اگر data وجود نداشت، بسازش
DATA_DIR.mkdir(exist_ok=True)

# فایل‌های پروژه
file_name = DATA_DIR / "books.xlsx"
file_name_member = DATA_DIR / "members.xlsx"
file_name_loan = DATA_DIR / "loans.xlsx"
last_id_file = DATA_DIR / "last_id.txt"

# فایل لاگ
LOG_FILE = BASE_DIR / "app.log"