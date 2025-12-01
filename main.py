# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import products, orders, auth

app = FastAPI(title="Smoothies API")

# ---------------------------
# 🔧 CORS
# ---------------------------
origins = settings.CORS_ORIGINS
if isinstance(origins, str):
    # por si viene como JSON en texto
    try:
        import json
        origins = json.loads(origins)
    except Exception:
        origins = [origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------
# 🔎 Health
# ---------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------
# 🔗 Routers
# ---------------------------
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(auth.router)
