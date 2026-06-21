from pydantic import BaseModel,field_validator
from enum import Enum
from datetime import date

class SingerURLChoice(Enum):
    Romantic = 'romantic'
    Rap = 'rap'

class SingerChoice(Enum):
    Romantic = 'Romantic'
    Rap = 'Rap'

class albums(BaseModel):
    name : str
    relese_date : date

class singerz(BaseModel):
    name : str
    genre : SingerChoice
    album : list = []

class createSingerz(singerz):
    @field_validator("genre",mode="before")
    def upper_case(cls,genre):
        return genre.title()

class singerzWithID(singerz):
    id : int
    
