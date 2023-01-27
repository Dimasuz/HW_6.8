# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import requests
import datetime
from models import Session, People


def max_people_count() -> int:
    return requests.get('https://swapi.dev/api/people/').json()['count']


def get_item(i: int):
    response = requests.get(f'https://swapi.dev/api/people/{i}/')
    if response.status_code == 200:
        res = response.json()
        d = {'films': 'title', 'species': 'name', 'starships': 'name', 'vehicles': 'name'}
        for k in d:
            if res[k]:
                l = []
                for u in res[k]:
                    response = requests.get(u)
                    if response.status_code == 200:
                        l.append(response.json()[d[k]])
                        res[k] = ', '.join(l)
                    else:
                        res[k] = ''
            else:
                res[k] = ''
    else:
        res = None
    return res


def fill_b_d(max_peaple):
    k = 0
    for i in range(1, max_peaple + 2):
        item = get_item(i)
        print(item)
        if item:
            k += 1
            [item.pop(key) for key in ['created', 'edited', 'url']]
            with Session() as session:
                new_people = People(**item)
                session.add(new_people)
                session.commit()
                print(f'в БД добавлен {k} из {i}')
    return 'OK'


if __name__ == '__main__':
    start = datetime.datetime.now()

    print(start)

    max_peaple = max_people_count()

    print(max_peaple)

    print(fill_b_d(max_peaple))

    print(datetime.datetime.now() - start)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
