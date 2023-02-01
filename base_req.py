import atexit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import People
from pprint import pprint
from config import PG_DSN

engine = create_engine(PG_DSN)

Session = sessionmaker(bind=engine)


def get_people_list():
    with Session() as session:
        people_list = session.query(People.name).order_by(People.name).all()
    return people_list

if __name__ == '__main__':
    people_list = get_people_list()
    pprint(people_list)
    print(len(people_list))

    atexit.register(engine.dispose)