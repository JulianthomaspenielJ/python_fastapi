from pydantic import BaseModel
from typing import Optional

class RegisterCamera(BaseModel):
    camera_id:int
    device_label:str
    device_streaming_url:str
    streaming_username: Optional[str] = None
    streaming_password: Optional[str] = None
   
class UpdateCamera(BaseModel):
    camera_id:int
    device_label:str
    device_streaming_url:str
    streaming_username: Optional[str] = None
    streaming_password: Optional[str] = None
    
class DeleteCamera(BaseModel):
    camera_id:int