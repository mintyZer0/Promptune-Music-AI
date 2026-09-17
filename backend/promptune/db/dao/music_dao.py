from fastapi import Depends
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from promptune.db.dependencies import get_db_session
from promptune.db.models.music import Artist, Album, Track
from typing import Optional, TypedDict


class MusicLibraryDAO:
    """Class for music library database operations."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def insert_artist(self, name: str, subsonic_id: str, ) -> None:
        """Insert artist into database"""
        new_artist = Artist(
            name=name,
            subsonic_id=subsonic_id
        )
        self.session.add(new_artist)

    async def insert_artists(self, artist_data: list[dict[str, str]]):
        """Batch insert artists into database"""
        artists = [
            Artist(name=artist["name"], subsonic_id=artist["subsonic_id"]) for artist in artist_data
        ]
        self.session.add_all(artists)
        
    async def insert_albums(self, album_data: list[dict[str, str]]):
        """Batch insert albums"""
        result = await self.session.execute(select(Artist.subsonic_id, Artist.id))
        artist_map = dict(result.all())
        # Match the artist_id via artist_map, use subonic id as key then match artist_id value
        albums = [
            Album(
                subsonic_id=album.get("id"), 
                artist_id=artist_map.get(album.get("artist_id")), 
                title=album.get("name"),
                release_date=album.get("year")
                )
                for album in album_data   
        ]

        self.session.add_all(albums)

