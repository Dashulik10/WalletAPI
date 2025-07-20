from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db, oauth2_scheme
from app.models.transaction import FinancialTransaction, TransactionKind

router = APIRouter()

@router.get("/stmt")
def get_statement(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(token=token, db=db)
    transactions = db.query(FinancialTransaction).filter(FinancialTransaction.user_id == current_user.id).order_by(FinancialTransaction.timestamp.desc()).all()

    return [
        {
            "kind": txn.kind,
            "amt": txn.amt,
            "updated_bal": txn.updated_bal,
            "timestamp": txn.timestamp.isoformat()
        }
        for txn in transactions
    ]