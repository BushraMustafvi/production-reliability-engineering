from application.database.engine import engine
from application.database.models import Base


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("DATABASE_SCHEMA=READY")
