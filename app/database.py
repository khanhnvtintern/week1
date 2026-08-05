from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

dir = Path(__file__).resolve().parent.parent/"data"
dir.mkdir(exist_ok = True)
DB_URL = f"sqlite:///{dir}/books.db"

engine = create_engine(
    DB_URL,
    connect_args = {"check_same_thread": False} # nhiều reqs chạy trên nhiều thread khác
    )
SessionLocal = sessionmaker(
    autocommit = False, # gọi .commit để save
    autoflush = False,# ORM -> DB trước khi query
    bind = engine # kn db
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()