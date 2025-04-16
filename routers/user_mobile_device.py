import time
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_mobile_device_schema import RegisterMobile,UpdateNotificationStatus
from app.models.user_mobile_device_model import UserMobileDeviceRegister
from sqlalchemy.orm import Session
from app.routers.common import get_db,create
from app.authMiddleWare.Oauth import validate_token
from fastapi.security import HTTPBearer

token_auth_scheme = HTTPBearer()

router = APIRouter(tags=['Mobile Device'])
created_at=time.strftime("%Y-%m-%d %H:%M:%S")

@router.post("/user/registerMobileDevice")
def device_register(request:RegisterMobile, db:Session=Depends(get_db), token: str = Depends(token_auth_scheme)):
    validate_token(token.credentials,db)
    device=UserMobileDeviceRegister(user_id=request.user_id, device_name=request.device_name,device_regsitration_token=request.device_registration_token,device_unique_id=request.device_unique_id,FCM_api_key=request.FCM_api_key, created_date_time=created_at,status=1)
    res_data=create(device,db)
    if  res_data is None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="Unable to register the device, Please try again later")
    response={"status_code":201,"detail":"Device registered successfully"}
    return response


@router.get("/user/getRegisteredDevices")    
def get_registered_mobile_device(db:Session=Depends(get_db), token: str = Depends(token_auth_scheme)):
    validate_token(token.credentials,db)
    device_data=db.query(UserMobileDeviceRegister).filter().all()
    if not device_data:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="No data found")
    res_data=[]
    for data in device_data:
        res_data.append({"device_name":data.device_name,"device_unique_id":data.device_unique_id, 'register_id':data.device_regsitration_token,'FCM_API_key':data.FCM_api_key,'device_notification':data.device_notification,'allow_override_DND':data.allow_override_DND})
    response={"status_code":200,"detail":"User device list",'response_data':res_data}
    return response

@router.get("/user/getRegisteredDevices/{device_unique_id}")    
def get_registered_mobile_device(device_unique_id,db:Session=Depends(get_db), token: str = Depends(token_auth_scheme)):
    validate_token(token.credentials,db)
    data=db.query(UserMobileDeviceRegister).filter(UserMobileDeviceRegister.device_unique_id==device_unique_id).first()
    if not data:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="No data found")
    res_data={"device_name":data.device_name,"device_unique_id":data.device_unique_id, 'register_id':data.device_regsitration_token,'FCM_API_key':data.FCM_api_key,'device_notification':data.device_notification,'allow_override_DND':data.allow_override_DND}
    response={"status_code":200,"detail":"User device list",'response_data':res_data}
    return response
   
@router.post("/user/updateNotificationStaus")
def update_notification(request:UpdateNotificationStatus, db:Session=Depends(get_db), token: str = Depends(token_auth_scheme)):
    validate_token(token.credentials,db)
    notification_status=None
    DND_status=None
    if request.device_notification==0 or request.device_notification==1:
        notification_status=request.device_notification
    elif request.allow_override_DND==0 or request.allow_override_DND==1:
        DND_status=request.allow_override_DND
    else:  
        raise HTTPException (status_code=400,detail="Bad Request")
    data=db.query(UserMobileDeviceRegister).filter(UserMobileDeviceRegister.device_unique_id==request.device_unique_id).first()
    if  data is None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="Unable to register the device, Please try again later")
    if notification_status!=None:
        data.device_notification=notification_status
    elif DND_status!=None:
        data.allow_override_DND=DND_status
    db.commit()

    response={"status_code":201,"detail":"Notification status updated successfully"}
    return response


    
