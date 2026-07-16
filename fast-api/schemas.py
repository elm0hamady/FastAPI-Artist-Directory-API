from pydantic import field_validator
from enum import Enum
from datetime import date
from typing import Optional
from sqlmodel import SQLModel , Relationship,Field

class SingerURLChoice(Enum):
    Romantic = 'romantic'
    Rap = 'rap'

class SingerChoice(Enum):
    Romantic = 'Romantic'
    Rap = 'Rap'

class AlbumBase(SQLModel):
    name : str
    relese_date : date
    band_id : int |None = Field(default=None,foreign_key="band.id")

class Album(AlbumBase,table = True ):
    id : int | None = Field(default=None , primary_key=True)
    band : "Band" = Relationship(back_populates="albums")

class singerz(SQLModel):
    name : str
    genre : SingerChoice

class createSingerz(singerz):
    albums : list[AlbumBase] | None = None

    @field_validator("genre",mode="before")
    def upper_case(cls,genre):
        return genre.title()

class Band(singerz,table= True):
    id : int = Field(default=None,primary_key=True)
    albums : list[Album] = Relationship(back_populates="band")
    birth_date : date | None = None
    
