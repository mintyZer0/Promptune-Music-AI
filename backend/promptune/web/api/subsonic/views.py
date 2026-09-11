from fastapi import APIRouter, HTTPException,  status
from promptune.services.subsonic import SubsonicClient, SubsonicLoginDTO
from httpx import RequestError

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(payload:SubsonicLoginDTO):
    client = SubsonicClient.from_password(
        payload.server_url,
        payload.username,
        payload.password
        )
    try:
        is_valid = await client.ping()

    except RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not connect to subsonic server. {e}"
        )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
       