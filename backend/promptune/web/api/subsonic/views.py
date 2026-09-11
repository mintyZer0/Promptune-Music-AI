from fastapi import APIRouter, HTTPException,  status
from promptune.services.subsonic import SubsonicClient, SubsonicLoginDTO

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(payload:SubsonicLoginDTO):
    client = SubsonicClient.from_password(
        payload.server_url,
        payload.username,
        payload.password
        )
    response = await client.ping()

    if not response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not connect to subsonic server."
        )

    return {
        "status":"success"
    }
