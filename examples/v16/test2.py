import requests
import json
# data = {'name': 'Alice', 'age': 11}
# response = requests.post('http://localhost:8080/submit', data=data)
# print(response.text)


#remote start charging point

data = {"id_tag":'MT0009120'}
response = requests.post('http://tpterp.com:8082/remote_start', data=json.dumps(data))


# #get transaction id
# data = requests.get('http://tpterp.com:8082/remote_stop')
# print(data)
# #remote stop charging point
# data = {"transaction_id":89660}
# response = requests.post('http://tpterp.com:8082/remote_stop', data=data)
