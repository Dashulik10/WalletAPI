from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db, oauth2_scheme
from app.models.user import User
from app.models.transaction import FinancialTransaction, TransactionKind

router = APIRouter(tags=["fund"])

@router.post("/fund", status_code=200, tags=["fund"])
def fund_account(payload: dict, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(token=token, db=db)
    amt = payload.get("amt")

    if not isinstance(amt, int) or amt <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid amount"
        )

    current_user.balance += amt

    txn = FinancialTransaction(
        user_id=current_user.id,
        kind=TransactionKind.CREDIT,
        amt=amt,
        updated_bal=current_user.balance
    )

    db.add(txn)
    db.commit()
    db.refresh(current_user)

    return {"balance": current_user.balance}