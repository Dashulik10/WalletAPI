from fastapi import Depends, HTTPException, APIRouter, status
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.core.auth import hash_password, verify_password, create_access_token, get_current_user, oauth2_scheme
from app.core.db import SessionLocal
from app.models.user import User
from app.models.transaction import FinancialTransaction
from app.models.product import Product
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", status_code=201, tags=["auth"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'New user registered successfully'}


@router.post("/login", status_code=200, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    is_password_correct = verify_password(form_data.password, user.password_hash)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    elif not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}