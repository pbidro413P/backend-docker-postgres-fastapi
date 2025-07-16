# main.py
import os
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, text
app = FastAPI(
    title="Servidor Backend",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("La variable DATABASE_URL no está definida en .env")

#AQUI COMIENZA LO NUEVO
engine = create_async_engine(
    DATABASE_URL,
    echo=True,              # para ver los logs SQL en consola
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)



Base = declarative_base()


class Mascota(Base, AsyncAttrs):
    __tablename__ = "mascota"

    apodo = Column(String, nullable=False, primary_key=True)
    cuidador = Column(String, nullable=False)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


class MascotaCreate(BaseModel):
    apodo: str
    cuidador: str

class MascotaRead(BaseModel):
    apodo: str
    cuidador: str

    class Config:
        orm_mode = True


@app.on_event("startup")
async def on_startup():
    # Crea las tablas si no existen (opcional en producción → usar migraciones)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/mascota/", response_model=MascotaRead)
async def crear_mascota(mascota: MascotaCreate,session: AsyncSession = Depends(get_session)):
    nueva = Mascota(apodo=mascota.apodo, cuidador=mascota.cuidador)
    session.add(nueva)

    await session.commit()
    await session.refresh(nueva)
    return nueva

# HASTA AQUI NUEVO





@app.get("/health")  #Decorador: una función que se gatilla antes de una función
async def health(): #def_ define una funcion, health es el nombre de la funcion, async nos permite asincronía en el flujo de ejecución
    return {"status":"ok"}
