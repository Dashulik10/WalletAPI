from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException
from app.core.auth import get_current_user, get_db, oauth2_scheme
from app.models.user import User
from app.models.product import Product
from app.models.transaction import FinancialTransaction, TransactionKind

router = APIRouter(tags=["buy"])

@router.post("/buy", status_code=200, tags=["buy"])
def buy_product(payload: dict, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(token=token, db=db)
    product_id = payload.get("product_id")

    if not isinstance(product_id, int):
        raise HTTPException(
            status_code=400,
            detail="Invalid product id"
        )

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if current_user.balance < product.price:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    current_user.balance -= product.price

    txn = FinancialTransaction(
        user_id=current_user.id,
        kind=TransactionKind.DEBIT,
        amt=product.price,
        updated_bal=current_user.balance
    )

    db.add(txn)
    db.commit()
    db.refresh(current_user)

    return {
        "message": "Product purchased successfully",
        "balance": current_user.balance
    }