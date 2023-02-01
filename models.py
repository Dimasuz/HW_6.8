from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import PG_DSN_ASYNC





engine = create_async_engine(PG_DSN_ASYNC)


Base = declarative_base()


class People(Base):

    __tablename__ = "peaple"

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(200))
    eye_color = Column(String(200))
    films = Column(String(400))
    gender = Column(String(200))
    hair_color = Column(String(200))
    height = Column(String(200))
    homeworld = Column(String(200))
    mass = Column(String(200))
    name = Column(String(200))
    skin_color = Column(String(200))
    species = Column(String(300))
    starships = Column(String(300))
    vehicles = Column(String(300))


Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
