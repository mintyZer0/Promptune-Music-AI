from typing import Optional
import secrets
import hashlib
from httpx import AsyncClient, RequestError, Response
from pydantic import BaseModel
from fastapi import HTTPException, status
class SubsonicLoginDTO(BaseModel):
    server_url: str
    username: str
    password: str


class SubsonicClient:

    def __init__(self, server_url:str, username:str, token:str, salt:str) -> None:
        self.server_url = server_url.rstrip("/")
        self.username = username
        self.token = token
        self.salt = salt

    
    @classmethod
    def from_password(cls,server_url:str, username:str, password:str):
        salt:str = secrets.token_hex(6)
        # Convert to byte by encoding
        token = hashlib.md5((password + salt).encode("utf-8")).hexdigest()
        return cls(server_url=server_url, username=username, token=token, salt=salt)

    def __build_params(self, username:str, token:str, salt:str):

        params:dict = {
            "u":username,
            "t":token,
            "s": salt,
            "v": "1.16.1",
            "c": "PrompTune",
            "f": "json"
        }

        return params

    async def ping(self):
        ping_params =  self.__build_params(self.username,self.token,self.salt)
        url = f"{self.server_url}/rest/ping.view"
        async with AsyncClient() as client:
            response = await client.get(url, params=ping_params, timeout=5.0)
            data = response.json()
            response_status = data.get("subsonic-response", {}).get("status", {})
            if response_status == "ok":
                return True
            else:
                return False

    async def getArtists(self):
        params = self.__build_params(self.username, self.token, self.salt)
        url = f"{self.server_url}/rest/getArtists"

        async with AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            return data
