from pydantic import BaseModel, EmailStr

class UserDetails(BaseModel):
    name: str
    email: EmailStr
    phone: str

class ConversationBody(BaseModel):
    contact_id: str
    conversation_id: str
    user_input: str

class Secrets(BaseModel):
    refresh_token: str
