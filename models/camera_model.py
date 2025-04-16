from sqlalchemy import Column,Integer,String,Boolean
from app.db.database import Base

class RegisterCameraDevice(Base):

    __tablename__="camera_device"
    __table_args__ = {'extend_existing': True}
    id=Column(Integer, primary_key=True, autoincrement=True)
    device_id=Column(Integer)
    device_label=Column(String)
    device_streaming_url=Column(String,nullable=False)
    streaming_username=Column(String)
    streaming_password=Column(String)
    created_date_time=Column(Integer,nullable=False)
    status=Column(Boolean,nullable=False)
