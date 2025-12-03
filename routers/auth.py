# routers/auth.py
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db import get_db
from models import User
from schemas import RegisterIn, LoginIn, AuthResponse, UserOut
from security import hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _normalize_email(email: str) -> str:
    return (email or "").strip().lower()


@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    email = _normalize_email(payload.email)

    existing = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if existing:
        # el front usa este detail para mostrar mensaje
        raise HTTPException(status_code=400, detail="EMAIL_ALREADY_REGISTERED")

    user = User(
        email=email,
        password_hash=hash_password(payload.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return AuthResponse(ok=True, user=UserOut.model_validate(user))


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    email = _normalize_email(payload.email)

    user: Optional[User] = db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="INVALID_CREDENTIALS")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="USER_INACTIVE")

    return AuthResponse(ok=True, user=UserOut.model_validate(user))


# -------- Dirección de envío de usuario --------
class AddressUpdate(BaseModel):
    shipping_address: str


@router.get("/user/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
    return UserOut.model_validate(user)


@router.put("/user/{user_id}/address", response_model=UserOut)
def update_address(user_id: int, payload: AddressUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

    user.shipping_address = (payload.shipping_address or "").strip()
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut.model_validate(user)



# -------- Dirección de envío de usuario --------
# -------- Dirección de envío de usuario --------
# -------- Dirección de envío de usuario --------