from os import write

import requests
import re
import csv

base_url = 'https://api.hh.ru/vacancies'
params = {
     "text":"Python разработчик",
     "area": 1,
     "per_page": 70,
     "page": 0
}
with open('hhpars.csv','w',encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Название', 'Компания', 'Город', 'Зарплата', 'Требования'])
response = requests.get(base_url,params = params)
hh_json = response.json().get('items', [])
for i in hh_json:
    requirement = i.get('snippet', {}).get('requirement')
    clean_requirement = re.sub(r'<\/?highlighttext>', '', requirement) if requirement else "Не указано"
    print(f"Назввание: {i['name']}")
    print(f"Компания: {i['employer']['name']}")
    print(f"Город: {i['area']['name']}")
    print(f"Требования: {clean_requirement}")
    if i['salary']:
        salary = i['salary']
        print(f"Зарплата: {i['salary']['from']} {i['salary']['currency']}")
    else:
        print("Зарплата не указана")
    if i['salary']:
        max_salary = i['salary']
        print(f"Макс Зарплата: {i['salary']['to']}")
    print("-"*50)
