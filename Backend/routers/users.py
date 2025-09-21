from fastapi import APIRouter, HTTPException, status
import schemas
from repository import users

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/signup")
async def signup(request: schemas.UserCreate):
    result = await users.create_user(request)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    return result

@router.post("/login", response_model=schemas.Token)
async def login(request: schemas.UserLogin):
    result = await users.login_user(request)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=result["error"])
    return result
