from pydantic import BaseModel, EmailStr

class UserDetails(BaseModel):
    name: str
    email: EmailStr
    phone: str
