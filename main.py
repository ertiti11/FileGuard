from fastapi import FastAPI
from app.api.v1.endpoints import router as api_router
from app.db import base, session

# Crea todas las tablas en la base de datos (solo para SQLite)
base.Base.metadata.create_all(bind=session.engine)

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")
