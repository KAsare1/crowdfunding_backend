import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    DB_URL = os.getenv("DB_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    REFRESH_KEY = os.getenv("REFRESH_KEY")
    REFRESH_EXPIRES = os.getenv("REFRESH_EXPIRES")
    ACCESS_EXPIRES = os.getenv("ACCESS_EXPIRES")
    ALGORITHM = os.getenv("ALGORITHM")
    


