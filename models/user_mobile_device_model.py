from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship
from app.models.users_model import Users

class UserMobileDeviceRegister(Base):

    __tablename__="user_registered_device"
    __table_args__ = {'extend_existing': True}
    id=Column(Integer, primary_key=True, autoincrement=True)
    user_id=Column(String, ForeignKey('users.id'),nullable=False)
    device_name=Column(String)
    device_unique_id=Column(String,nullable=False)
    FCM_api_key=Column(String,nullable=False)
    device_regsitration_token=Column(String,nullable=False)
    device_notification=Column(Integer,nullable=True)
    allow_override_DND=Column(Integer,nullable=True)
    created_date_time=Column(Integer,nullable=False)
    status=Column(Boolean,nullable=False)
    mobile=relationship('Users')