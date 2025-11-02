# routers/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from db import get_db
from models import Product
from schemas import ProductOut

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    try:
        stmt = select(Product).where(Product.active == True)
        rows = db.execute(stmt).scalars().all()  # <- clave: .scalars()
        return [ProductOut.model_validate(r) for r in rows]  # valida explícito
    except Exception as e:
        # Log al server y error claro
        print("❌ /api/products error:", repr(e))
        raise HTTPException(status_code=500, detail="PRODUCTS_QUERY_FAILED")

# Endpoint de salud de DB para diagnosticar rápido
# routers/products.py
@router.get("/_dbcheck")
def db_check(db: Session = Depends(get_db)):
    from sqlalchemy import text
    try:
        db.execute(text("SELECT 1"))
        return {"db": "ok"}
    except Exception as e:
        import traceback
        print("❌ DB check error:", repr(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="DB_ERROR")

