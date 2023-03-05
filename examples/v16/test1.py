import asyncio
import logging
import random
import websockets
import json
from datetime import datetime, timezone

#
# async def authenticate_and_send_remote_start():
#     async with websockets.connect('ws://tpterp.com:9000/TA2200001', subprotocols=["ocpp1.6"]) as websocket:
#         #send user verification
#         auth_payload = [
#             2,"TA2200001",'Authorize',{"idTag": "2000202204111389"}]
#         await websocket.send(json.dumps(auth_payload))
        #
        # # Charging
        # charge_payload = [
        #     2,"TA2200001",'StatusNotification',{'connectorId':2,'errorCode':'NoError',"status": "Charging",
        #                                       'timestamp':datetime.now(timezone.utc).isoformat()}]
        # await websocket.send(json.dumps(charge_payload))
        #
        # Start Charging
        # start_payload = [
        #     2,'StartTransaction',{'connectorId':2,
        #                                         'meterStart':15813,
        #                                         "idTag": "2000202204111389",
        #                                       'timestamp':datetime.now(timezone.utc).isoformat()}]
        # await websocket.send(json.dumps(start_payload))

        #Stop Charging
        # stop_payload =  [2,"20230228134641182","StatusNotification",
        #                  {"connectorId":2,"errorCode":"NoError","status":"Finishing","timestamp":datetime.now(timezone.utc).isoformat()}]
        # await websocket.send(json.dumps(stop_payload))
        # auth_response = await websocket.recv()
        # print(f"Received auth response: {auth_response}")
        # Check if authentication was successful
        # auth_response_json = json.loads(auth_response)
        # if auth_response_json['payload']['idTagInfo']['status'] == "Accepted":
        #     print("Authentication successful!")
        #     start_payload = [
        #     3, "TA2200001",{"status": "Accepted"}]
        #     await websocket.send(json.dumps(start_payload))
        #     start_response = await websocket.recv()
        #     print(f"Received start response: {start_response}")
        # else:
        #     print("Authentication failed.")

# asyncio.run(authenticate_and_send_remote_start())
#



# async def send_call():
#     async with websockets.connect('ws://tpterp.com:9000/testCCSII30SCTEST', subprotocols=["ocpp1.6"]) as websocket:
#
#         # request = [2,'','StopTransaction',{
#         #     # 'connectorId':1,
#         #     'idTag':'2000202204111389',
#         #     'meterStop': 16567,
#         #     'timestamp':datetime.now(timezone.utc).isoformat(),
#         #     "transactionId": 16567
#         #     }]
#         # request = [2,'testCCSII30SCTEST','Authorize',{
#         #     "idTag":"4548fc69"
#         #     }]
#         # request1 = [2,'testCCSII30SCTEST','StatusNotification',{
#         #     'connectorId' :1,
#         #     'errorCode':"OtherError",
#         #     'status':'Charging'
#         # }]
#         request2 = [2,'CCSII30SCTEST','RemoteStartTransaction',{
#             "idTag":"4548fc69"
#             }]
#
#         # call.RemoteStartTransactionPayload(id_tag='2000202204111389')
#
#         # message = json.dumps(request)
#         # await websocket.send(message)
#         # message1 = json.dumps(request1)
#         # await websocket.send(message1)
#         message2 = json.dumps(request2)
#         await websocket.send(message2)
#
#
#         # response = await websocket.recv()
#         # print(response)
#
#
# asyncio.run(send_call())


from aiohttp import web



# async def handler(request):
#     return web.Response(text="Hello, World!")
#
# app = web.Application()
# app.add_routes([web.post('/handler', handler)])
#
# if __name__ == "__main__":
#     web.run_app(app,host='localhost')

from aiohttp import web

async def handle_post(request):
    data = await request.post()  # 获取POST请求体中的数据
    name = data.get('name')  # 获取名为"name"的字段
    age = data.get('age')  # 获取名为"age"的字段

    if not name or not age:
        return web.Response(text='Missing required fields', status=400)

    response_data = {
        'message': f'Hello, {name}! You are {age} years old.'
    }
    return web.json_response(response_data)

app = web.Application()
app.add_routes([web.post('/submit', handle_post)])

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=8080)
