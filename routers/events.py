import time,shutil
from urllib import request
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.events_schema import RegisterEvent,GetEventsByPost
from app.models.events_model import EventCreate
from sqlalchemy.orm import Session
from app.routers.common import get_db,create
from app.authMiddleWare.Oauth import validate_token
from fastapi.security import HTTPBearer
from fastapi.responses import FileResponse
from app import config


token_auth_scheme = HTTPBearer()
router=APIRouter(tags=["Events"])

created_at=time.strftime("%Y-%m-%d %H:%M:%S")

def get_storage_details():
    total, used, free = shutil.disk_usage("/")
    res={"Total_space": str((total // (2**30)))+" GB","Used":str((used // (2**30)))+" GB","Free":str((free // (2**30)))+" GB"}
    return res

@router.post("/event/register")
def event_register(request:RegisterEvent, db: Session = Depends(get_db),token: str = Depends(token_auth_scheme)):
    validate_token(token.credentials,db)
    new_event=EventCreate(event_name=request.event_name, detected_by=request.detected_by,image_url=request.image_url, created_date_time=created_at,status=1)
    res_data=create(new_event,db)
    if  res_data is None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="Unable to register the event")
    response={"status_code":201,"detail":"Event registered successfully"}
    return response
    

@router.get("/events/get/{id}")    
def get_events(id: str ,db:Session=Depends(get_db), token: str = Depends(token_auth_scheme)):
        validate_token(token.credentials,db)
        response=get_event_data(id,db,"GET")
        return response

@router.post("/events/get")    
def get_events(request:GetEventsByPost ,db:Session=Depends(get_db), token: str = Depends(token_auth_scheme)):
        validate_token(token.credentials,db)
        response=get_event_data(request,db,"POST")
        return response

def get_event_data(req,db,type:str):
    count= db.query(EventCreate).filter(EventCreate.status==1).count()
    res_data=[]
    if type=="POST":
        event_data=db.query(EventCreate).filter(EventCreate.created_date_time>=req.start_date, EventCreate.created_date_time<=req.end_date, EventCreate.status==1).all()
    else:
        if req == "all":
            event_data=db.query(EventCreate).filter(EventCreate.status==1).all()
        else:
            req=int(req)-1
            start=req*10
            event_data=db.query(EventCreate).filter(EventCreate.status==1).offset(start).limit(10).all()
    if len(event_data)==0 or not event_data:
            raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="No Data Found")
    else:
        for data in event_data:
            res_data.append({"event_name":data.event_name,'event_image_url':data.image_url})
        response={"status_code":200,"detail":"Events list","total_record": count,'response_data':res_data}

    return response


@router.get("/event/get/image/{filename}")
def getImage(filename:str):
    image_path=config.IMAGE_BASE_PATH+filename
    return FileResponse(image_path)
    
@router.get("/device/getStorageSize")    
def get_device_storage_details():
    storage_details=get_storage_details()
    response={"status_code":200,"detail":"Storage details data","storage_details": storage_details}
    return response

@router.post("/events/clear")    
def clear_events(db:Session=Depends(get_db), token: str = Depends(token_auth_scheme)):
        validate_token(token.credentials,db)
        event_data=db.query(EventCreate).filter().all()
        for data in event_data:
            data.status=0
        db.commit()
        response={"status_code":200,"detail":"Event logs cleared successfully"}
        return response


