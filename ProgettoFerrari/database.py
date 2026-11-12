
import os
import pymysql
from pathlib import Path
from dotenv import load_dotenv

# Carica le informazioni dal file .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

def connect_db():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "Progettoferrari"),
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection
