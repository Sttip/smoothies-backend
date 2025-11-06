# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import products, orders
import json

# 🔐 Importar router de autenticación
from routers import auth  # asegúrate de tener routers/auth.py creado

app = FastAPI(title="Smoothies API")

# 🔧 Manejo robusto de CORS
try:
    if isinstance(settings.CORS_ORIGINS, str):
        CORS_LIST = json.loads(settings.CORS_ORIGINS)
    else:
        CORS_LIST = settings.CORS_ORIGINS
except Exception:
    CORS_LIST = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ]

print(f"🌐 CORS habilitado para: {CORS_LIST}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# 🔗 Routers
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(auth.router)  # 👈 se monta el router de autenticación
