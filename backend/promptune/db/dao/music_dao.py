from fastapi import Depends
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from promptune.db.dependencies import get_db_session
from promptune.db.models.music import Artist, Album, Track
from typing import Optional

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
        

    # async def get_by_username(self, username:str) ->  User | None:
    #     """Find a user by their username"""
    #     query = select(User).where(User.subsonic_username == username)
    #     result = await self.session.execute(query)
    #     return result.scalar_one_or_none()

    # async def create_user(self, server_url:str, username:str, token:str, salt:str, email:str, hashed_password:str) -> None:
    #     new_user = User(
    #         subsonic_server_url=server_url,
    #         subsonic_username=username,
    #         subsonic_token=token,
    #         subsonic_salt=salt,
    #         email=email,
    #         hashed_password=hashed_password
    #     )

    #     self.session.add(new_user)

    #     await self.session.commit()


    # async def update_user(self, server_url:str, username:str, token:str, salt:str) -> None:
    #     statement = (update(User)
    #                  .where(User.subsonic_username == username)
    #                  .values(
    #                     subsonic_server_url=server_url,
    #                     subsonic_username=username,
    #                     subsonic_token=token,
    #                     subsonic_salt=salt
    #                     )
    #                 )
    #     await self.session.execute(statement)
    #     await self.session.commit()
        