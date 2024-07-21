from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .db import db
from datetime import datetime, timezone
from .crud import get_access_token, get_refresh_token, create_secret
from .api_calls import *
from .models import UserDetails

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_token():
    # get access token and creation time
    access_token, creation_time = await get_access_token()
    # if token is older than 20 hours, get a new token pair
    if (datetime.now(timezone.utc) - creation_time).total_seconds() > 72000:
        # fetch the refresh token
        refresh_token = await get_refresh_token()
        # get a new token pair
        new_token_pair = await get_new_token_pair(refresh_token)
        # create a new secret pair
        await create_secret(refresh_token=new_token_pair['refresh_token'], access_token=new_token_pair['access_token'])
        # return the new access token
        return new_token_pair['access_token']

    return access_token


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
def read_root():
    return {"Hello": "HVAC_Millionaire"}


@app.post("/submit_details")
async def submit_details(user_details: UserDetails, access_token: Annotated[str, Depends(get_token)]):
    contact_id = await create_contact(
        name=user_details.name, 
        email=user_details.email, 
        phone=user_details.phone, 
        access_token=access_token)
    return {"msg": "Details submitted successfully", "contact_id": contact_id}
