from fastapi import APIRouter, HTTPException,  status
from pydantic import BaseModel
from services import subsonic

router = APIRouter()

### to do figure out routes for ping
# @router.get("/ping", status_code=status.HTTP_200_OK)
# async def ping()