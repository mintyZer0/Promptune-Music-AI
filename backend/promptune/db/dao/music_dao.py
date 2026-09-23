from fastapi import Depends
from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from promptune.db.dependencies import get_db_session
from promptune.db.models.music import Artist, Album, Track, Playlist, Playlist_Track
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

    async def insert_artists(self, artist_data: list[dict[str, str]]) -> None:
        """Batch insert artists into database"""
        artists = [
            Artist(name=artist.get("name"), subsonic_id=artist.get("id")) for artist in artist_data
        ]
        self.session.add_all(artists)
        
    async def insert_albums(self, album_data: list[dict[str, str]]) -> None:
        """Batch insert albums"""
        result = await self.session.execute(select(Artist.subsonic_id, Artist.id))
        artist_map = dict(result.all())
        # Match the artist_id via artist_map, use subonic id as key then match artist_id value
        albums = [
            Album(
                subsonic_id=album.get("id"), 
                artist_id=artist_map.get(album.get("artistId")), 
                title=album.get("name"),
                release=album.get("year")
                )
                for album in album_data   
        ]

        self.session.add_all(albums)

    
    async def insert_tracks(self, tracks_data: list[dict[str,str]]) -> None:
        result = await self.session.execute(select(Artist.subsonic_id, Artist.id))
        artist_map = dict(result.all())

        # For tracks that have ids that's not in the artist database (e.g. collaborators)
        result = await self.session.execute(select(Album.subsonic_id, Album.artist_id))
        album_artist_map = dict(result.all())

        result = await self.session.execute(select(Album.subsonic_id, Album.id))
        album_map = dict(result.all())

        tracks = [
            Track(
                subsonic_id=track.get("id"),
                artist_id=artist_map.get(track.get("artistId")) or album_artist_map.get(track.get("albumId")),
                album_id=album_map.get(track.get("albumId")),
                title=track.get("title"),
                duration_seconds=track.get("duration")
            )

            for track in tracks_data
        ]

        self.session.add_all(tracks)

    async def insert_playlists(self, playlist_data: list[dict[str,str]]):

        playlists = [
            Playlist(
                subsonic_id=playlist.get("id"),
                name=playlist.get("name"),
                song_count=playlist.get("songCount"),
                duration_seconds=playlist.get("duration"),
                created=playlist.get("created")
                )
            for playlist in playlist_data
        ]

        self.session.add_all(playlists)


    async def insert_playlist_tracks(self, playlists_with_tracks_data: list[dict[str,str]]):
        result = await  self.session.execute(select(Track.subsonic_id, Track.id))
        tracks_map = dict(result.all())

        result = await self.session.execute(select(Playlist.subsonic_id, Playlist.id))
        playlist_map = dict(result.all())

        playlist_tracks = [
            Playlist_Track(
                playlist_id=playlist_map.get(playlist.get("id")),
                track_id=tracks_map.get(playlist_track.get("id")),
                position=playlist_track.get("track"),
                )
            for playlist in playlists_with_tracks_data
            for playlist_track in playlist.get("entry")
        ]    

        self.session.add_all(playlist_tracks)



    async def clear_library(self) -> None:
        """Deletes entire library"""

        await self.session.execute(delete(Track))
        await self.session.execute(delete(Album))
        await self.session.execute(delete(Artist))
        await self.session.execute(delete(Playlist))
        await self.session.execute(delete(Playlist_Track))
        await self.session.flush()


