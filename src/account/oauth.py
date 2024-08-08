import datetime
import jwt
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN_EXPIRY_MINUTES = int(os.environ['ACCESS_TOKEN_EXPIRY_MINUTES'])
ALGORITHM = os.environ['ALGORITHM']
SECRET = os.environ['SECRET']

def create_token (payload:dict):
    copy = payload.copy()
    
    expire = datetime.datetime.now() + datetime.timedelta(minutes = ACCESS_TOKEN_EXPIRY_MINUTES)
    copy.update({"exp" : expire})
    
    encoded_jwt = jwt.encode(copy, SECRET, algorithm = ALGORITHM)
    return encoded_jwt 

def verify_token(token:str, secret:str):

    try:
        payload = jwt.decode(token, secret, algorithms = [ALGORITHM])
        email: str = payload.get("email")
        expire = datetime.datetime.now() + datetime.timedelta(minutes = ACCESS_TOKEN_EXPIRY_MINUTES)
        payload['exp'] = expire

        if not email :
            return 
    except :
        return 

    return payload

# def verify_token(token:str, credentials_exception):

#     try:
#         payload = jwt.decode(token, SECRET, algorithms = [ALGORITHM])
#         email: str = payload.get("email")

#         if email is None :
#             raise credentials_exception

#         token_data = payload(user = email)
#         print(token_data)
#     except :
#         raise credentials_exception

#     return token_data