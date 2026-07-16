from sqlmodel import Session,SQLModel,create_engine


databaseURL = 'sqlite:///db.sqlite'
engine = create_engine(databaseURL,echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

