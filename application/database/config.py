import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://reliability:reliability@localhost:5433/reliability",
)
