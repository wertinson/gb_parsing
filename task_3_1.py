from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint
from pymongo import MongoClient


client = MongoClient('localhost', 27017)

db = client['vacancy']
vacancy_hh = db.vacancy_hh


def str_to_num(str):
    num = re.findall(r'\d+', str)
    return int(''.join(num))


def link_to_id(link):
    first_step = link.split('/')
    second_step = first_step[4].split('?')

    return second_step[0]


def db_vacancy_insert_one(job_data):

    id = link_to_id(job_data['link'])

    count_docs = vacancy_hh.count_documents({"_id": id})

    if count_docs == 0:
        # print(f'док не найден, вставляем = {count_docs}')

        vacancy_hh.insert_one({
            "_id": id
            , "name": job_data['name']
            , "link": job_data['link']
            , "site": job_data['site']
            , "salary_min": job_data['salary']['salary_min']
            , "salary_max": job_data['salary']['salary_max']
            , "salary_curr": job_data['salary']['salary_curr']
        })


def get_vacancy_with_salary(salary):
    list_vacancy = vacancy_hh.find({'$or': [{'salary_min': {'$gt': salary}}, {'salary_max': {'$gt': salary}}]})

    return list_vacancy


job_list = []
page = 0
while True:

    base_url = 'https://krasnodar.hh.ru'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    params = {'text': 'data engineer', 'page': page}


    url = f'{base_url}/search/vacancy'
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f'ошибка {response.status_code}')
        break

    print(f'получена {page} страница вакансий')

    dom = BeautifulSoup(response.text, 'html.parser')

    vacancy = dom.find_all('div', {'class': 'vacancy-serp-item-body__main-info'})

    for item in vacancy:
        job_data = {}

        name = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        # print(name)
        link = name['href']
        # print(name['href'])

        if item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}):
            salary = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
        else:
            salary = None
        # print(salary)

        if salary:
            temp = salary.split(' ')

            if temp[0] == 'от':
                salary_min = str_to_num(temp[1])
                salary_max = None
                salary_curr = temp[2]
            elif temp[0] == 'до':
                salary_min = None
                salary_max = str_to_num(temp[1])
                salary_curr = temp[2]
            else:
                salary_min = str_to_num(temp[0])
                salary_max = str_to_num(temp[2])
                salary_curr = temp[3]

        job_data['name'] = name.getText()
        job_data['salary'] = {'salary_min': salary_min, 'salary_max': salary_max, 'salary_curr': salary_curr}
        job_data['link'] = link
        job_data['site'] = base_url

        job_list.append(job_data)
        db_vacancy_insert_one(job_data)

    print(f'страница {page} успешно обработана')
    print('')

    page += 1


for doc in get_vacancy_with_salary(300000):
    pprint(doc)

# pprint(job_list)





