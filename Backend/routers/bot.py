from fastapi import APIRouter,HTTPException,status,Header,Depends,Request
from Backend.auth import verify_jwt
from repository.bot import gemini_response
# from auth_dep import get_current_user  # JWT dependency
from Backend import schemas




router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)



@router.post("/", response_model=schemas.ChatResponse)
async def chat_endpoint(request_obj: Request, request: schemas.ChatRequest, authorization: str | None = Header(None)):
    print("All headers:", request_obj.headers)
    print("Authorization header param:", authorization)
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Authorization header missing", "code": "auth_header_missing"}
        )

    try:
        token_type, token = authorization.split(" ")
        if token_type.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid token type", "code": "invalid_token_type"}
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid authorization header format", "code": "invalid_header_format"}
        )

    try:
        user_id = verify_jwt(token)
    except HTTPException as e:
        # Forward friendly error messages from verify_jwt
        raise HTTPException(
            status_code=e.status_code,
            detail={"error": e.detail, "code": "jwt_error"}
        )

    # Call Gemini response
    response = await gemini_response(user_id, request.message)
    return response