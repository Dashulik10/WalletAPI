from sqlalchemy import (Column, Integer, String, ForeignKey,
                        DateTime, Enum as SQLAlchemyEnum)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum

from app.core.db import Base

class TransactionKind(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"

class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    kind = Column(SQLAlchemyEnum(TransactionKind), nullable=False)
    amt = Column(Integer)
    updated_balance = Column(Integer)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="financial_transactions")
