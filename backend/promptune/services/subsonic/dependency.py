from fastapi import Depends, requests, Request
from promptune.db.models.users import User, current_active_user
from promptune.services.subsonic import SubsonicClient

def create_subsonic_client(request: Request, user: User = Depends(current_active_user)):
    client = request.app.state.http_client
    return SubsonicClient(server_url=user.subsonic_server_url,
                          username=user.subsonic_username,
                          token=user.subsonic_token,
                          salt=user.subsonic_salt,
                          client=client
                          )