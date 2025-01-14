import os

from pydantic import BaseModel

BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class DBSettings(BaseModel):
    DB_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/data/db.sqlite3"
