from fastapi import APIRouter, Depends
from app.core.auth import get_current_user, get_db, oauth2_scheme
from sqlalchemy.orm import Session

router = APIRouter(tags=["balance"])

@router.get("/balance", status_code=200)
def get_balance(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(token=token, db=db)
    return {
        "balance" : current_user.balance
    }