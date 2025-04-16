import jwt
from app import config
from fastapi import HTTPException
from app.models.users_model import UsersLogin

def generate_jwt_token(payload_data):    
    token = jwt.encode(payload=payload_data,key=config.SECRET_KEY)
    return token

def validate_token(token:str,db):
    
        data=db.query(UsersLogin).filter(UsersLogin.token==token,UsersLogin.status==1).first()
        if not data:
            raise HTTPException (status_code=401,detail="Invalid token")    
        return data
    
    

    