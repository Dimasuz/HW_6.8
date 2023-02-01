from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import People
from config import PG_DSN

engine = create_engine(PG_DSN)

Session = sessionmaker(bind=engine)


def get_people_count():
    with Session() as session:
        return session.query(People).count()


if __name__ == '__main__':
    print(get_people_count())
