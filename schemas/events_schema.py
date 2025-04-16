from pydantic import BaseModel
from typing import Optional

class RegisterEvent(BaseModel):
    event_name:str
    detected_by:str
    image_url: str

class GetEventsByPost(BaseModel):
    start_date:str
    end_date: str
