import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Config class to get environment variables

    This class is used so the dotenv package is only imported in one place
    """
    @staticmethod
    def get(key: str) -> str:
        return str(os.getenv(key))