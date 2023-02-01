import asyncio
from aiohttp import ClientSession
import datetime
from more_itertools import chunked
import requests
from models import engine, Session, People, Base
from config import CHUNK_SIZE, URL


def max_people_count() -> int:
    return requests.get(URL).json()['count']


async def get_item(i: int, client: ClientSession):
    k = 0
    while i and k < 10:
        k += 1
        # async with client.get(f'{URL}/{i}/') as item:
        #     print(f'people_id {i}, status {item.status}, attempt {k} from 10')
        #     if item.status == 200:
        #         i = 0
        #         item_json = await item.json()
        item = await client.get(f'{URL}/{i}/')
        print(f'people_id {i}, status {item.status}, attempt {k} from 10')
        if item.status == 200:
            i = 0
            item_json = await item.json()
            for key in ['created', 'edited', 'url']:
                item_json.pop(key)
            d = {'films': 'title', 'species': 'name', 'starships': 'name', 'vehicles': 'name'}
            for k in d:
                if item_json[k]:
                    l = []
                    for u in item_json[k]:
                        res = await client.get(u)
                        if res.status == 200:
                            res_json = await res.json()
                            l.append(res_json[d[k]])
                    item_json[k] = ', '.join(l)
                else:
                    item_json[k] = ''
        else:
            item_json = None
    return item_json


async def add_to_db(items):
    async with Session() as session:
        # list = [People(**item) for item in items if item]
        # list = []
        # for item in items:
        #     if item:
        #         list.append(People(**item))
        # session.add_all(list)
        session.add_all([People(**item) for item in items if item])
        await session.commit()


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    max_people = max_people_count()
    async with ClientSession() as client:
        for id_chunk in chunked(range(1, max_people + 2), CHUNK_SIZE):
            items_caro = [get_item(i, client) for i in id_chunk]
            items = await asyncio.gather(*items_caro)
            items_task = asyncio.create_task(add_to_db(items))
    tasks = set(asyncio.all_tasks()) - {asyncio.current_task()}
    for task in tasks:
        await task


start = datetime.datetime.now()
asyncio.run(main())
print(f'all time: {datetime.datetime.now() - start}')
