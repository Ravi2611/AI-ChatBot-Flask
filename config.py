import os
from dotenv import load_dotenv

# Folder to watch
WATCH_FOLDER = os.path.join(os.path.dirname(__file__), "input_files")

# Supported file types
SUPPORTED_EXTENSIONS = [".csv", ".xlsx", ".xls", ".pdf", ".docx"]

# Scheduler interval (in seconds)
SCHEDULE_INTERVAL = 300  # 5 mins

# Load environment variables
load_dotenv()

class Config:
    PGHOST = os.getenv("PGHOST", "localhost")
    PGPORT = os.getenv("PGPORT", "5432")
    PGUSER = os.getenv("PGUSER", "postgres")
    PGPASSWORD = os.getenv("PGPASSWORD", "postgres")
    PGDATABASE = os.getenv("PGDATABASE", "vector_db")

    # DB connection string
    DATABASE_URL = (
        f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
    )
