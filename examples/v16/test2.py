import requests
import json
# data = {'name': 'Alice', 'age': 11}
# response = requests.post('http://localhost:8080/submit', data=data)
# print(response.text)


# data = {"id_tag":'testCCSII30SCTEST'}
# response = requests.post('http://tpterp.com:8082/remote_start', data=json.dumps(data))
# print(response.content)

data = {"transaction_id":'testCCSII30SCTEST'}
response = requests.post('http://tpterp.com:8082/remote_stop', data=json.dumps(data))
print(response.content)