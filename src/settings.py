import os

from dotenv import load_dotenv

load_dotenv()


DB_URL = os.getenv("DB_URL", "sqlite:///database.sqlite3")

ENV = os.getenv("ENV", "DEV")
