from sqlalchemy import create_engine, text
from app.core.db import Base
from app.models.user import User
from app.models.transaction import FinancialTransaction
from app.models.product import Product

DATABASE_URL = "postgresql://postgres:123456@postgres_db:5432/wallet"
engine = create_engine(DATABASE_URL)


def init_db():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1;"))
    except Exception as e:
        return

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        return


if __name__ == "__main__":
    init_db()
