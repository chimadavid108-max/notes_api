import os

APP_NAME = "Notes API"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///notes.db")
LIST_LIMIT = int(os.getenv("LIST_LIMIT", "10"))
