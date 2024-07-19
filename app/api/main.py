from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware(
        allow_origins=origins,
    )
)

@app.get("/")
def read_root():
    return {"Hello": "HVAC_Millionaire"}