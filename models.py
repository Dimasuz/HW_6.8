import atexit
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


PG_DSN='sqlite:///sqlite3.db'


def get_engine():
    return create_engine(PG_DSN)


engine = get_engine()


Base = declarative_base()


class People(Base):

    __tablename__ = "peaple"

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(200))
    eye_color = Column(String(200))
    films = Column(String(200))
    gender = Column(String(200))
    hair_color = Column(String(200))
    height = Column(String(200))
    homeworld = Column(String(200))
    mass = Column(String(200))
    name = Column(String(200))
    skin_color = Column(String(200))
    species = Column(String(200))
    starships = Column(String(200))
    vehicles = Column(String(200))


Base.metadata.create_all(bind=engine)


def get_session_maker():
    return sessionmaker(bind=engine)


Session = get_session_maker()

atexit.register(engine.dispose)