from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    balance = Column(Integer, default=0)
    financial_transactions = relationship("FinancialTransaction", back_populates="user")