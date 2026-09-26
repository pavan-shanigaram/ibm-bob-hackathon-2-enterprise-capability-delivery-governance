from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# SQLite needs connect_args={"check_same_thread": False}
_is_sqlite = settings.DATABASE_URL.startswith("sqlite")
_connect_args = {"check_same_thread": False} if _is_sqlite else {}
_kwargs = {"connect_args": _connect_args, "echo": settings.DEBUG}
if not _is_sqlite:
    _kwargs["pool_pre_ping"] = True
    _kwargs["pool_recycle"] = 300

engine = create_engine(settings.DATABASE_URL, **_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
