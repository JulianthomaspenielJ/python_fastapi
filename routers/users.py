import hashlib
import time
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import users_schema
from app.models.users_model import Users,UsersLogin
from sqlalchemy.orm import Session
from app.routers.common import get_db,create
from app.authMiddleWare.Oauth import generate_jwt_token
from app.authMiddleWare.Oauth import validate_token
from fastapi.security import HTTPBearer

token_auth_scheme = HTTPBearer()
router = APIRouter(tags=['Users'])
created_at=time.strftime("%Y-%m-%d %H:%M:%S")


@router.post("/user/register")
def user_register(request:users_schema.Register, db: Session = Depends(get_db)):
    password=hashlib.md5(request.password.encode()).hexdigest()
    new_user=Users(email_id=request.email_id, user_name=request.user_name,password=password, created_date_time=created_at,status=1)
    res_data=create(new_user,db)
    if  res_data is None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="Unable to register the user")
    response={"status_code":201,"detail":"User registered successfully"}
    return response
    

@router.post("/user/login")
def user_login(request:users_schema.Login,  db: Session = Depends(get_db)):
    password=hashlib.md5(request.password.encode()).hexdigest()
    data=db.query(Users).filter(Users.user_name==request.user_name, Users.status==1).first()
    if data is None:
        raise HTTPException (status_code=404,detail="Invalid User Name")
    if data.password!=password:
        raise HTTPException (status_code=404,detail="Invalid Password")
    token=generate_jwt_token({"username":request.user_name,"time":created_at})
    insert_user_login_details(token,data.id,db,created_at)
    res_data={"user_id":data.id, "user_name":data.user_name,'token':token}
    response={"status_code":200,"detail":"User loggedin successfully",'response_data':res_data}
    return response
    

def insert_user_login_details(token,user_id,db,created_at):
    user_login_data=UsersLogin(user_id=user_id, token=token, created_date_time=created_at,status=1)
    res_data=create(user_login_data,db)
    if not res_data:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="Unable to process your request, Please try again later")
    return res_data
    

@router.post("/user/logout")
def user_logout(request:users_schema.Logout,  db: Session = Depends(get_db),  token: str = Depends(token_auth_scheme)):
    validate_token(token.credentials,db)
    data=db.query(UsersLogin).filter(UsersLogin.user_id==request.user_id, UsersLogin.token==token.credentials,UsersLogin.status==1).first()
    if not data:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail="Token Expired / Invalid token")
    data.status=0
    db.commit()
    response={"status_code":200,"detail":"User loggedout successfully"}
    return response
    
        

