from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Dependencia para inyectar sesión en los endpoints
from contextlib import contextmanager
def get_db():
    @contextmanager
    def _ctx():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    return _ctx()

