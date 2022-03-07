import requests
from pprint import pprint

# строка для получения токена
# https://oauth.vk.com/authorize?client_id=5490057&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.131

# токен для авторизации
access_token = ''

# получение списка сообществ
url = 'https://api.vk.com/method/groups.get?v=5.131&access_token=' + access_token

response = requests.get(url)

pprint(response.json())
