from sqlalchemy import Column,Integer,String,Boolean
from app.db.database import Base

class EventCreate(Base):

    __tablename__="events"
    __table_args__ = {'extend_existing': True}
    id=Column(Integer, primary_key=True, autoincrement=True)
    event_name=Column(String)
    detected_by=Column(String, nullable=False)
    image_url=Column(String, nullable=False)
    created_date_time=Column(Integer, nullable=False)
    status=Column(Boolean, nullable=False)
   