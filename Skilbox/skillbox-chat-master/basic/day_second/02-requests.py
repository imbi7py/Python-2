#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Библиотека Requests
#
#  http://python-requests.org
#  https://pypi.org/project/requests/
#
#  Работа с запросами на веб-сервер (веб-сайты)
#
#  1. pip install requests - установить пакет
#  2. import requests - подключить в файле .py
#
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users")

user_list = response.json()

# user_list[0]['name']


post_response = requests.post("https://jsonplaceholder.typicode.com/users", {
    'name': 'Andy'
})

print(post_response.json())
