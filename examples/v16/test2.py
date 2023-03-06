import requests
import json
# data = {'name': 'Alice', 'age': 11}
# response = requests.post('http://localhost:8080/submit', data=data)
# print(response.text)


data = {"id_tag":'2000202204111389'}
response = requests.post('http://tpterp.com:8082/remote_start', data=json.dumps(data))
print(response.content)