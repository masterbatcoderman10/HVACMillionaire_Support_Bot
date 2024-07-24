import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
import os
from pprint import pprint

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
location_id = os.getenv('LOCATION_ID')


async def create_contact(name, email, phone, access_token):

    url = "https://services.leadconnectorhq.com/contacts/"

    payload = {
        "firstName": "",
        "lastName": " ",
        "name": name,
        "email": email,
        "locationId": location_id,
        "gender": " ",
        "phone": phone,
        "address1": "",
        "city": "",
        "state": "",
        "postalCode": "",
        "website": "",
        "timezone": "",
        "dnd": False,
        "dndSettings": {
            "Call": {"status": "inactive"},
            "Email": {"status": "inactive"},
            "SMS": {"status": "inactive"},
            "WhatsApp": {"status": "inactive"},
            "GMB": {"status": "inactive"},
            "FB": {"status": "inactive"},
        },
        "inboundDndSettings": {"all": {"status": "inactive"}},
        "tags": ["chatbot", "chatbot"],
        "customFields": [],
        "source": "chatbot",
        "country": "India",
        "companyName": "",
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Version': '2021-07-28'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code == 400:
            # Contact already exists, the error response body contains a `meta` object with existing contact id return that
            response_body = response.json()
            meta = response_body['meta']
            return meta['contactId']
        else:
            response_body = response.json()
            contact = response_body['contact']
            return contact['id']
        
async def search_conversations(contact_id, access_token):

    url = "https://services.leadconnectorhq.com/conversations/search"

    params = {
        "contactId": contact_id,
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Version': '2021-04-15'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response_body = response.json()
        conversations = response_body["conversations"]
        if conversations:
            return conversations[0]['id']
        else:
            return None

async def send_message(user_input, contact_id, access_token):

    url = "https://services.leadconnectorhq.com/conversations/messages"

    payload = {
        "contactId": contact_id,
        "message": user_input,
        "type": "WebChat",
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Version': '2021-04-15',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        return response.json()


async def get_new_token_pair(refresh_token):
    url = "https://services.leadconnectorhq.com/oauth/token"

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        return response.json()


async def get_pipelines(access_token):
    url = "https://services.leadconnectorhq.com/opportunities/pipelines"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Version': '2021-07-28'
    }

    query_params = {
        'locationId': location_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=query_params)
        return response.json()


# Create oppotunity function: TBD

async def create_conversation(contact_id, access_token):

    url = "https://services.leadconnectorhq.com/conversations/"

    payload = {
        "contactId": contact_id,
        "locationId": location_id,
    }
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Version': '2021-04-15'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code == 400:
            return await search_conversations(contact_id=contact_id, access_token=access_token)
        response_data = response.json()
        return response_data['conversation']['id']


async def get_all_messages(conversation_id, access_token):
    url = f"https://services.leadconnectorhq.com/conversations/{conversation_id}/messages?limit=20"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Version": "2021-04-15",
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()


async def map_messages(conversation_id, access_token):
    chat_messages = []
    response = await get_all_messages(conversation_id=conversation_id, access_token=access_token)
    messages = response.get('messages').get('messages')
    messages = messages[::-1]
    messages = [msg_obj['body'] for msg_obj in messages]
    chat_messages = [{"role": "user", "content": text}
                     for text in messages]
    for i, chat_message in enumerate(chat_messages):
        if i % 2 != 0:
            chat_message['role'] = "assistant"
    pprint(chat_messages)
    if len(chat_messages) % 2 != 0:
        chat_messages.pop(0)
    return chat_messages

async def get_contact_details(contact_id, access_token):
    url = f"https://services.leadconnectorhq.com/contacts/{contact_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Version": "2021-04-15",
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    #get the name and return
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()['contact']['firstName']

