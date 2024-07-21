import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
import os

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
            # Handle the 400 error, e.g., log it, raise an exception, etc.
            raise HTTPException(status_code=400, detail=response.json())
        else:
            response_body = response.json()
            contact = response_body['contact']
            return contact['id']

async def create_conversation(contact_id, access_token):
    
    url = "https://services.leadconnectorhq.com/conversations/"

    payload = {
        "contactId": contact_id,
        "locationId": location_id,
        "unreadCount": 0,  # Modify as needed
        "starred": False,  # Modify as needed
        "inbox": False,  # Modify as needed
        "deleted": False  # Modify as needed
    }
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Version': '2021-04-15'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        return response.json()

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

#Create oppotunity function: TBD



    



