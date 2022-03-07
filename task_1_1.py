import requests
from pprint import pprint

url = 'https://api.github.com/users/wertinson/repos'

response = requests.get(url)

resp_json = response.json()

# pprint(resp_json)

for el in resp_json:
    print(el['svn_url'])
