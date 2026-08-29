from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from promptune.services.gemini import GeminiService, Playlist

router = APIRouter()

gemini_service = GeminiService()

@router.post("/generate", response_model=Playlist, status_code=200, summary=("Returns a json file of a generated playlist"))
async def generate_playlist(payload: str) -> Playlist:
        return await gemini_service.generate_playlist(prompt=payload)
