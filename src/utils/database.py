from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import Config

engine = create_engine(Config.get('DATABASE_URL'))
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Database:
    """
    Database class to get a database session

    This class is used so the database session is only created in one place
    """
    @staticmethod
    def get_session():
        db_session: Session = session()
        try:
            yield db_session
        finally:
            db_session.close()

    @staticmethod
    def get_engine():
        return engine