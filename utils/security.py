import jwt
from params import JWT_SECRET
from datetime import datetime, timedelta

ALGORITHM = "HS256"

def create_access_token(data: dict, expire:int=60):
    to_encode = data.copy() 
    expire = datetime.now() + timedelta(minutes=expire) 
    to_encode.update({"exp": expire}) 
    return jwt.encode(to_encode,JWT_SECRET, algorithm=ALGORITHM)


token = create_access_token({"user_id": 42}) 
print(token)
    