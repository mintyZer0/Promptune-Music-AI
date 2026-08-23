from fastapi.routing import APIRouter

from promptune.web.api import monitoring, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
