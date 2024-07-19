from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import db

app = FastAPI()

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware(
        allow_origins=origins,
    )
)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.get("/")
def read_root():
    return {"Hello": "HVAC_Millionaire"}