from typing import Optional
import secrets
import hashlib
from httpx import AsyncClient, RequestError, Response
from pydantic import BaseModel
from fastapi import HTTPException, status, Request
import asyncio
class SubsonicLoginDTO(BaseModel):
    server_url: str
    username: str
    password: str


class SubsonicClient:

    def __init__(self, server_url:str, username:str, token:str, salt:str, client: AsyncClient) -> None:
        self.server_url = server_url.rstrip("/")
        self.username = username
        self.token = token
        self.salt = salt
        self.client = client
        self.sephamore = asyncio.Semaphore(3)

    
    @classmethod
    def from_password(cls,server_url:str, username:str, password:str):
        salt:str = secrets.token_hex(6)
        # Convert to byte by encoding
        token = hashlib.md5((password + salt).encode("utf-8")).hexdigest()
        return cls(server_url=server_url, username=username, token=token, salt=salt)

    def __build_params(self, extra_params:dict | None = None):

        params:dict = {
            "u":self.username,
            "t":self.token,
            "s": self.salt,
            "v": "1.16.1",
            "c": "PrompTune",
            "f": "json"
        }
        if extra_params:
            params.update(extra_params)
        return params

    async def __get(self, endpoint:str, params: dict | None = None) -> dict:
        """get request helper function"""
        url = f"{self.server_url}/rest/{endpoint}"
        created_params = self.__build_params(params)

        async with self.sephamore:
            for attempt in range(3):
                try:
                                    response: Response = await self.client.get(url, params=created_params, timeout=15.0)
                                    response.raise_for_status()
                                    data = response.json()
                                    return data
                except RequestError as e:
                    if attempt == 3:
                        raise RuntimeError(f"Failed to connect to Navidrome: {e}")
                    asyncio.sleep(0.5)


        
    async def ping(self):
        data = await self.__get("ping")
        response_status = data.get("subsonic-response", {}).get("status", {})
        if response_status == "ok":
            return True
        else:
            return False

    async def get_artists(self):
        data = await self.__get("getArtists")
        index_list = data.get("subsonic-response", {}).get("artists", {}).get("index", [])
        artists = []
        for group in index_list:
            for artist in group.get("artist"):
                artists.append({"id":artist.get("id"), "name":artist.get("name")})
        return artists

    async def get_albums(self, size: int = 500):
        all_albums = []
        offset = 0

        while True:
            data = await self.__get("getAlbumList2", {"type":"alphabeticalByName",
                                                       "size": size,
                                                       "offset": offset
                                                       })
            
            if not data:
                break

            albums = [album for album in data.get("subsonic-response", {}).get("albumList2", {}).get("album", [])]
            all_albums.extend(albums)
            offset += len(albums)

            # no more albums if less then offset
            if len(albums) < size:
                break

        print(len(all_albums))
        return all_albums


    async def get_tracks(self):
        albums = await self.get_albums(500)

        album_ids = [album.get("id") for album in albums]

        tasks = [self.__get("getAlbum", {"id":album_id}) for album_id in album_ids]
        tracks_responses = await asyncio.gather(*tasks)

        tracks = [
             track
             for res in tracks_responses
             for track in res.get("subsonic-response", {}).get("album", {}).get("song", [])
        ]

        return tracks
