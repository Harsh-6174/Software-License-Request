import psycopg2, os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_DATABASE"),
    )
