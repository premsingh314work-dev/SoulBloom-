from fastapi import APIRouter,HTTPException,status,Header,Depends,Request
from Backend.auth import verify_jwt
from Backend.repository.bot import gemini_response
# from auth_dep import get_current_user  # JWT dependency
from Backend import schemas

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
security = HTTPBearer()




router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)



@router.post("/", response_model=schemas.ChatResponse)
async def chat_endpoint(
    request_obj: Request,
    request: schemas.ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # credentials.scheme should be 'Bearer', credentials.credentials is the token
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid token type", "code": "invalid_token_type"}
        )
    try:
        user_id = verify_jwt(credentials.credentials)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"error": e.detail, "code": "jwt_error"}
        )
    response = await gemini_response(user_id, request.message)
    return response