from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db, oauth2_scheme
from app.models.user import User
from app.models.transaction import FinancialTransaction, TransactionKind

router = APIRouter(tags=["pay"])

@router.post("/pay", status_code=200, tags=["pay"])
def pay(payload: dict, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(token=token, db=db)
    to_username = payload.get("to")
    amt = payload.get("amt")

    if not isinstance(to_username, str) or not isinstance(amt, int) or amt <= 0:
        raise HTTPException(status_code=400, detail="Invalid input")

    if current_user.username == to_username:
        raise HTTPException(status_code=400, detail="Cannot pay yourself")

    receiver = db.query(User).filter(User.username == to_username).first()

    if not receiver:
        raise HTTPException(status_code=400, detail="Recipient does not exist")

    if current_user.balance < amt:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    current_user.balance -= amt
    receiver.balance += amt

    sender_txn = FinancialTransaction(
        user_id=current_user.id,
        kind=TransactionKind.DEBIT,
        amt=amt,
        updated_bal=current_user.balance
    )

    receiver_txn = FinancialTransaction(
        user_id=receiver.id,
        kind=TransactionKind.CREDIT,
        amt=amt,
        updated_bal=receiver.balance
    )

    db.add_all([sender_txn, receiver_txn])
    db.commit()
    db.refresh(current_user)

    return {"balance": current_user.balance}