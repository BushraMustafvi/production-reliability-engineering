from sqlalchemy import create_engine, text

from application.database.config import DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def check_database_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
