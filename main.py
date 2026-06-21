from fastapi import FastAPI,HTTPException,Query,Path
from typing import List, Optional , Annotated
from schemas import SingerURLChoice,singerz,createSingerz,singerzWithID


app = FastAPI()

singers = [{'id' :1 ,'name':'amr diab' , 'genre': 'Romantic'},
           {'id' :2 ,'name':'sherien' , 'genre': 'Romantic','album' : [
                {'name' : '3la 3eny' , 'relese_date' : "2000-05-13"},
                {'name' : 'زي م بقولك' , 'relese_date' : "1919-05-23"}
           ] },
           {'id' :3 ,'name':'marawan pablo' , 'genre': 'Rap'},
           {'id' :4 ,'name':'abysif' , 'genre': 'Rap'},
           {'id' :5 ,'name':'wegz' , 'genre': 'Rap'},
          ]   

@app.get('/')
async def index():
    return {'hello' : 'fastapi'}

@app.get('/about')
async def about() -> str:
    return "about our company"

@app.get('/singers') #query paramater
async def get_singers(genre: Optional[SingerURLChoice] = None,
                      has_album : bool = False,
                      q:Annotated[Optional[str],Query(max_length=10)] = None
                      ) -> List[singerzWithID]:
    varSinger = [singerzWithID(**t) for t in singers]
    if genre:
        varSinger = [
            t for t in varSinger if t.genre.value.lower() == genre.value
        ]
    if has_album:
        varSinger = [
            t for t in varSinger if len(t.album) > 0
        ]
    if q:
        varSinger = [
            t for t in varSinger if q.lower() in t.name.lower()
        ]
    return varSinger


@app.get('/singers/{singer_id}') #Path Paramater
async def singer(singer_id : Annotated[int,Path(title="This Is Singer ID",ge=1)]) -> singerzWithID:
    singer = next((singerzWithID(**s) for s in singers if s['id'] == singer_id),None)

    if singer is None:
        raise HTTPException(status_code=404,detail='singer not found')
    return singer

# @app.get('/singers/genre/{sin_genre}')
# async def singer_genre(sin_genre: SingerURLChoice) -> List[singerz] :
#     return [
#         singerz(**t) for t in singers if t['genre'].lower() == sin_genre.value
#     ]

@app.post('/singers')
async def create_band(bandData : createSingerz) -> singerzWithID:
    id = singers[-1]['id'] +1
    band = singerzWithID(id=id,**bandData.model_dump()).model_dump()
    singers.append(band)
    return band

