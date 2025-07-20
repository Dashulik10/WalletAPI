from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db, oauth2_scheme
from app.models.product import Product
from app.models.user import User

router = APIRouter(tags=["product"])

@router.post("/product", status_code=201, tags=["product"])
def add_product(payload: dict, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme),):

    name = payload.get("name")
    price = payload.get("price")
    description = payload.get("description")

    if not name or not isinstance(price, int) or price <= 0:
        raise HTTPException(status_code=400, detail="Invalid input")

    product = Product(name=name, price=price, description=description)
    db.add(product)
    db.commit()
    db.refresh(product)

    return {"id": product.id, "message": "Product added"}

@router.get("/product", tags=["product"])
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description
        }
        for p in products
    ]