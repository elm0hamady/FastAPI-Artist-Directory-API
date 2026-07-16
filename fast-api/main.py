from fastapi import FastAPI,HTTPException,Query,Path,Depends
from typing import List, Optional , Annotated
from schemas import SingerURLChoice,singerz,createSingerz,Band,Album
from db import get_session
from sqlmodel import Session,select
from sqlalchemy.orm import selectinload



app = FastAPI()

# singers = [{'id' :1 ,'name':'amr diab' , 'genre': 'Romantic'},
#            {'id' :2 ,'name':'sherien' , 'genre': 'Romantic','album' : [
#                 {'name' : '3la 3eny' , 'relese_date' : "2000-05-13"},
#                 {'name' : 'زي م بقولك' , 'relese_date' : "1919-05-23"}
#            ] },
#            {'id' :3 ,'name':'marawan pablo' , 'genre': 'Rap'},
#            {'id' :4 ,'name':'abysif' , 'genre': 'Rap'},
#            {'id' :5 ,'name':'wegz' , 'genre': 'Rap'},
#           ]   

@app.get('/')
async def index():
    return {'hello' : 'fastapi'}

@app.get('/about')
async def about() -> str:
    return "about our company"

@app.get('/singers') #query paramater
async def get_singers(genre: Optional[SingerURLChoice] = None,
                      has_album : bool = False,
                      q:Annotated[Optional[str],Query(max_length=10)] = None,
                      session : Session = Depends(get_session)
                      ) -> List[Band]:
    varSinger = session.exec(
                select(Band).options(selectinload(Band.albums))
                ).all()
    if genre:
        varSinger = [
            t for t in varSinger if t.genre.value.lower() == genre.value
        ]
    if has_album:
        varSinger = [
            t for t in varSinger if len(t.albums) > 0
        ]
    if q:
        varSinger = [
            t for t in   varSinger if q.lower() in t.name.lower()
        ]
    return varSinger


@app.get('/singers/{singer_id}') #Path Paramater
async def singer(singer_id : Annotated[int,Path(title="This Is Singer ID",ge=1)], session : Session = Depends(get_session)) -> Band:
    singer = session.get(Band,singer_id)

    if singer is None:
        raise HTTPException(status_code=404,detail='singer not found')
    return singer

# @app.get('/singers/genre/{sin_genre}')
# async def singer_genre(sin_genre: SingerURLChoice) -> List[singerz] :
#     return [
#         singerz(**t) for t in singers if t['genre'].lower() == sin_genre.value
#     ]

@app.post('/singers')
async def create_band(bandData : createSingerz , session : Session = Depends(get_session)) -> Band :
    
    band = Band(name = bandData.name , genre = bandData.genre)
    session.add(band)

    if bandData.albums:
        for album_data in bandData.albums:
            album_obj = Album(name = album_data.name , relese_date = album_data.relese_date , band = band)
            session.add(album_obj)
            session.commit()

    session.commit()
    session.refresh(band)
    return band

