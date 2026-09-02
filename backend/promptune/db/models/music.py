from datetime import datetime
import uuid
from sqlalchemy import (
    String,
    Integer,
    Float,
    Float,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    func,   
)
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from promptune.db.base import Base

class Artist(Base):
    __tablename__ = "artists"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    #Relationships
    albums: Mapped[list["Album"]] = relationship(back_populates="artist", cascade="all, delete-orphan")
    tracks: Mapped[list["Track"]] = relationship(back_populates="artist")

class Album(Base):
    __tablename__ = "albums"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    artist_id: Mapped[int] = mapped_column(
        ForeignKey("artists.id", ondelete="CASCADE"),
        nullable=False
        )
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    release: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cover_art_url: Mapped[Optional[str]] = mapped_column(String(500))
    #Relationships
    artist: Mapped["Artist"] = relationship(back_populates="albums")
    

class Track(Base):
    __tablename__ = "tracks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    artist_id: Mapped[int] = mapped_column(
        ForeignKey("artists.id"),
        nullable=False
    )
    album_id: Mapped[int] = mapped_column(
        ForeignKey("albums.id", ondelete="cascade"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)
    #Relationships
    album: Mapped["Album"] = relationship(back_populates="albums")
    artist: Mapped["Artist"] = relationship(back_populates="tracks")    