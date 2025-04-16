
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class Users(Base):

    __tablename__="users"
    __table_args__ = {'extend_existing': True}
    id=Column(Integer, primary_key=True, autoincrement=True)
    email_id=Column(String)
    user_name=Column(String, nullable=False)
    password=Column(String, nullable=False)
    created_date_time=Column(Integer, nullable=False)
    status=Column(Boolean, nullable=False)
    user=relationship("UsersLogin", back_populates="login")
   

class UsersLogin(Base):
    __tablename__="user_login_details"
    __table_args__ = {'extend_existing': True}
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer, ForeignKey('users.id'), nullable=False)
    token=Column(String, nullable=False)
    created_date_time=Column(Integer, nullable=False)
    status=Column(Boolean, nullable=False)
    login=relationship("Users", back_populates="user")
    




