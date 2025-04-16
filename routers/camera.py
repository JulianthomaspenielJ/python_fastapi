import time
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import camera_schema
from app.models.camera_model import RegisterCameraDevice
from sqlalchemy.orm import Session
from app.routers.common import get_db,create
from app.authMiddleWare.Oauth import validate_token
from fastapi.security import HTTPBearer

token_auth_scheme = HTTPBearer()
router=APIRouter(tags=["Camera"])

created_at=time.strftime("%Y-%m-%d %H:%M:%S")

@router.post("/camera/register")
def camera_register(request:camera_schema.RegisterCamera, db: Session = Depends(get_db),token: str = Depends(token_auth_scheme)):
    validate_token(token.credentials,db)
    new_camera=RegisterCameraDevice(device_id=request.camera_id,device_label=request.device_label, device_streaming_url=request.device_streaming_url,streaming_username=request.streaming_username, streaming_password=request.streaming_password, created_date_time=created_at,status=1)
    res_data=create(new_camera,db)
    if  res_data is None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="Unable to register the Camera device")
    response={"status_code":201,"detail":"Camera registered successfully"}
    return response
    

@router.get("/camera/getRegisteredDevices")    
def get_registered_camera_device(db:Session=Depends(get_db),token: str = Depends(token_auth_scheme)):
    validate_token(token.credentials,db)
    camera_data=db.query(RegisterCameraDevice).filter(RegisterCameraDevice.status==1).all()
    if not camera_data:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="No data found")
    res_data=[]
    for data in camera_data:
        res_data.append({"id":data.id,"camera_id":data.device_id,"device_label":data.device_label,"streaming_url":data.device_streaming_url,"streaming_username":data.streaming_username,"streaming_password":data.streaming_password})
    response={"status_code":200,"detail":"Camera device list",'response_data':res_data}
    return response
    

@router.post("/camera/details/update")    
def camera_details_update(request:camera_schema.UpdateCamera,db:Session=Depends(get_db),token: str = Depends(token_auth_scheme)):
    validate_token(token.credentials,db)
    camera_data=db.query(RegisterCameraDevice).filter(RegisterCameraDevice.device_id==request.camera_id,RegisterCameraDevice.status==1).first()
    if not camera_data:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="No data found")
    camera_data.device_label=request.device_label
    camera_data.device_streaming_url=request.device_streaming_url
    camera_data.streaming_username=request.streaming_username
    camera_data.streaming_password=request.streaming_password
    camera_data.created_date_time=created_at
    db.commit()
    # db.refresh()
    response={"status_code":200,"detail":"Camera details updated successfully"}
    return response


@router.post("/camera/delete")    
def camera_delete(request:camera_schema.DeleteCamera,db:Session=Depends(get_db),token: str = Depends(token_auth_scheme)):
    validate_token(token.credentials,db)
    camera_data=db.query(RegisterCameraDevice).filter(RegisterCameraDevice.device_id==request.camera_id,RegisterCameraDevice.status==1).first()
    if not camera_data:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="No data found")
    camera_data.status=0
    db.commit()
    response={"status_code":200,"detail":"camera details removed successfully"}
    return response

