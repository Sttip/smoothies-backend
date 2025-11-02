from fastapi import APIRouter

router = APIRouter(prefix="/api/products", tags=["products"])

# Más adelante:
# @router.get("", response_model=list[ProductOut])
# def list_products(...): ...
#
# @router.get("/{slug}", response_model=ProductOut)
# def get_product(slug: str, ...): ...

