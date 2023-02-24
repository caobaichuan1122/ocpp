import asyncio
import websockets
import json

async def authenticate_and_send_remote_start():
    async with websockets.connect('ws://tpterp.com:9000', subprotocols=["ocpp1.6"]) as websocket:
        # 发送身份验证请求
        auth_payload = {
            # "messageTypeId": "Call",
            # "uniqueId": "unique_request_id",
            # "action": "Authorize",
            # "payload": {
            #     "idTag": "2000202204111389"
            # }
        }
        await websocket.send(json.dumps(auth_payload))
        auth_response = await websocket.recv()
        print(f"Received auth response: {auth_response}")

        # 检查身份验证是否成功
        auth_response_json = json.loads(auth_response)
        if auth_response_json['payload']['idTagInfo']['status'] == "Accepted":
            print("Authentication successful!")
            start_payload = {
                "messageTypeId": "Call",
#                 "uniqueId": "unique_request_id",
                "action": "RemoteStartTransaction",
                "payload": {
                    "connectorId": 1
                }
            }
            await websocket.send(json.dumps(start_payload))
            start_response = await websocket.recv()
            print(f"Received start response: {start_response}")
#         else:
#             print("Authentication failed.")

asyncio.run(authenticate_and_send_remote_start())