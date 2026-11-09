from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

url = settings.sqlalchemy_url
connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
# pool_pre_ping: Neon suspends idle compute and drops connections.
engine = create_engine(url, connect_args=connect_args, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
