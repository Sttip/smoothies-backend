# Smoothies Backend (FastAPI + PostgreSQL)

## Requisitos
- Python 3.11+
- PostgreSQL
- (Opcional) Docker, VS Code

## Configuración local
1. Crear y activar un entorno virtual
2. `pip install -r requirements.txt`
3. Crear `.env` a partir de `.env.example` y poner tu `DATABASE_URL`
4. Ejecutar: `uvicorn app.main:app --reload`
5. Probar: `http://127.0.0.1:8000/health` → `{"status":"ok"}`

## Estructura
- `app/main.py`: arranque FastAPI + CORS + routers
- `app/config.py`: variables de entorno
- `app/db.py`: conexión a DB y sesión
- `app/models.py`: Base de SQLAlchemy (tablas más adelante)
- `app/schemas.py`: Pydantic (contratos de API)
- `app/routers/`: endpoints (`products`, `orders`)

## Próximos pasos
- Definir modelos (Product, Order, OrderLine) y migraciones con Alembic
- Implementar `/api/products` y `/api/orders`
- Seeds de productos
- Deploy en Render/Railway + PostgreSQL gestionado
# smoothies-backend
