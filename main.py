from fastapi import FastAPI, Depends

from app.core.db import Base, engine
from app.routes import auth
from app.routes import balance
from app.routes import buy
from app.routes import fund
from app.routes import pay
from app.routes import product
from app.routes import stmt
from app.core.auth import get_current_user, oauth2_scheme
from app.models.user import User
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


app = FastAPI(title="WalletAPI", tags=["home"])
app.include_router(auth.router)
app.include_router(balance.router)
app.include_router(buy.router)
app.include_router(fund.router)
app.include_router(pay.router)
app.include_router(product.router)
app.include_router(stmt.router)


@app.get("/")
async def home():
    return {"message": "Wallet API is running 🚀"}

@app.get("/protected")
async def protected_root(token: str = Depends(oauth2_scheme)):
    return {"token": token}


