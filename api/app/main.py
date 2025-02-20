from fastapi import FastAPI
from .routers import products
from .db import engine, Base

app = FastAPI(title="E-Commerce API")

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
