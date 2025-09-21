import os
from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hashng password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# createing JWT token
def create_access_token(user_id: str, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = {"sub": user_id}
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#verifying access token
def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid JWT")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid JWT")

