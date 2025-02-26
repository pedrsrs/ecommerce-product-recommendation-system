from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .routers import products
from .db import engine, Base

app = FastAPI(title="E-Commerce API")

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(products.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "E-Commerce API is running"}
