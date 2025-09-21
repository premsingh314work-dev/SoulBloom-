from datetime import datetime
from bson import ObjectId
from database import db
import schemas
from auth import hash_password, verify_password, create_access_token

# signup
async def create_user(request: schemas.UserCreate):
    user = await db["users"].find_one({"email": request.email})
    if user:
        return {"error": "Email already registered"}

    new_user = {
        "name": request.name,
        "email": request.email,
        "password": hash_password(request.password),
        "createdAt": datetime.utcnow()
    }
    result = await db["users"].insert_one(new_user)
    return {"id": str(result.inserted_id), "email": request.email}

# login
async def login_user(request: schemas.UserLogin):
    user = await db["users"].find_one({"email": request.email})
    if not user:
        return {"error": "Invalid email or password"}

    if not verify_password(request.password, user["password"]):
        return {"error": "Invalid email or password"}

    # Pass user_id as string
    token = create_access_token(str(user["_id"]))
    return {"access_token": token, "token_type": "bearer"}
