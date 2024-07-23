from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .db import db, Base, engine
from datetime import datetime, timezone
from .crud import get_access_token, get_refresh_token, create_secret
from .api_calls import *
from .models import UserDetails, ConversationBody, Secrets
from .ai_utils import HVACMillionaireBot

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5500",
    "http://localhost:5501",

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
    Base.metadata.create_all(engine)
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
    # create a conversation
    conversation_id = await create_conversation(contact_id, access_token)
    return {"msg": "Details submitted successfully", "contact_id": contact_id, "conversation_id": conversation_id}

@app.post("/chatbot")
async def chatbot(
    conversation_details: ConversationBody,
    access_token: Annotated[str, Depends(get_token)]
):
    contact_id = conversation_details.contact_id
    conversation_id = conversation_details.conversation_id
    user_input = conversation_details.user_input

    name = await get_contact_details(contact_id, access_token)

    chat_messages = await map_messages(conversation_id, access_token)
    chat_messages.append({"role": "user", "content": user_input})
    bot = HVACMillionaireBot(
        user_context={"name": name},
        contact_id=contact_id,
        history=chat_messages,
        ACCESS_TOKEN=access_token
    )
    # send the user input
    await send_message(user_input, contact_id, access_token)
    response = await bot.execute()
    # send the bot response
    await send_message(response, contact_id, access_token)

    return {"msg": "Message sent successfully", "response": response}

@app.post("/initialize_tokens")
async def initialize_tokens(refresh_token: Secrets):

    try:
        # get a new token pair
        new_token_pair = await get_new_token_pair(refresh_token.refresh_token)
        # create a new secret pair
        await create_secret(refresh_token=new_token_pair['refresh_token'], access_token=new_token_pair['access_token'])
        return {"msg": "Tokens initialized successfully"}
    except Exception as e:
        return {"msg": "Something went wrong", "error": str(e)}

