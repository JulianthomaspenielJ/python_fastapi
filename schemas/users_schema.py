from pydantic import BaseModel
from typing import Optional

class Register(BaseModel):
    email_id:Optional[str]
    user_name: str
    password: str

class Login(BaseModel):
    user_name: str
    password: str

class Logout(BaseModel):
    user_id: str
   

