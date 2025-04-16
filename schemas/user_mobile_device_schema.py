from pydantic import BaseModel
from typing import Optional

class RegisterMobile(BaseModel):
    user_id:int
    device_name:str
    device_unique_id:str
    device_registration_token:str
    FCM_api_key:str

class UpdateNotificationStatus(BaseModel):
    device_unique_id:str
    device_notification:Optional[int] = None
    allow_override_DND:Optional[int] = None


    
    
    
   