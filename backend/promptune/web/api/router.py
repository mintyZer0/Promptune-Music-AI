from fastapi.routing import APIRouter

from promptune.web.api import monitoring, users, playlist, subsonic

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(playlist.router, prefix="/playlist", tags=["playlist"])
api_router.include_router(subsonic.router, prefix="/subsonic", tags=["subsonic"])
