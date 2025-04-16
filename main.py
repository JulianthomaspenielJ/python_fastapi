from typing import Optional
from fastapi import FastAPI
from app.routers import users,user_mobile_device,camera,events
from app.db.database import Base,engine



app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(users.router, )
app.include_router(user_mobile_device.router)
app.include_router(camera.router)
app.include_router(events.router)