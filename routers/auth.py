# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from db import get_db
from models import User
from schemas import RegisterIn, LoginIn, AuthResponse, UserOut
from security import hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    # ¿Existe?
    existing = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if existing:
        return AuthResponse(ok=False, error="El correo ya está registrado")

    # Crear
    u = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_active=True,  # ← IMPORTANTE: evitar NOT NULL en la DB
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return AuthResponse(ok=True, user=UserOut.model_validate(u))

@router.post("/login", response_model=AuthResponse)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    u = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if not u or not verify_password(payload.password, u.password_hash):
        return AuthResponse(ok=False, error="Credenciales inválidas")
    return AuthResponse(ok=True, user=UserOut.model_validate(u))

# --- mini healthcheck para auth / tabla users ---
from sqlalchemy import inspect

@router.get("/_dbcheck")
def auth_dbcheck(db: Session = Depends(get_db)):
    """
    Verifica que la tabla 'users' exista y la conexión a DB esté OK.
    Se muestra en Swagger como GET /api/auth/_dbcheck
    """
    try:
        inspector = inspect(db.bind)
        tables = set(inspector.get_table_names())
        exists = "users" in tables
        return {"users_table": "ok" if exists else "missing"}
    except Exception:
        return {"users_table": "missing or error"}
