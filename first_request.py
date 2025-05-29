from os import write

import requests
import re
import csv
### Создаем URL
base_url = 'https://api.hh.ru/vacancies'
params = {
     "text":"Python разработчик",
     "area": 1,
     "per_page": 70,
     "page": 0
}
###Открываем блок для записи в excel
with open('hhpars.csv','w',encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';') ##Указываем разделитель ; чтобы разбить на стлобцы
    writer.writerow(['Название', 'Компания', 'Город', 'Зарплата от', 'Зарплата до', 'Валюта', 'Требования']) #указываем столбцы

    response = requests.get(base_url,params = params) #Прокидываем запрос
    hh_json = response.json().get('items', []) #Переводим в json и запрашиваем через get по ключу items
    #Создаем цикл для переборки json
    for i in hh_json:
        ### Запрашиваем требования
        requirement = i.get('snippet', {}).get('requirement')
        ###Чистим требования от не нужных знаков
        clean_requirement = re.sub(r'<\/?highlighttext>', '', requirement) if requirement else "Не указано"
        ### Обработка зарплаты, может быть none###
        salary = i.get('salary')
        ##Работаем с ценой
        salary_from = salary.get('from') if salary else "Не указано"
        salary_to = salary.get('to') if salary else "Не указано"
        currency = salary.get('currency') if salary else "Не указано"
        ### Записываем в excel
        writer.writerow([
            i['name'],
            i['employer']['name'],
            i['area']['name'],
            salary_from,
            salary_to,
            currency,
            clean_requirement
        ])
    ### Выводим в консоль
        print(f"Назввание: {i['name']}")
        print(f"Компания: {i['employer']['name']}")
        print(f"Город: {i['area']['name']}")
        print(f"Требования: {clean_requirement}")

        print("-"*50)
