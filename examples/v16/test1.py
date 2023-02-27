import asyncio
import websockets
import json
from datetime import datetime, timezone

async def authenticate_and_send_remote_start():
    async with websockets.connect('ws://tpterp.com:9000', subprotocols=["ocpp1.6"]) as websocket:
        # send user verification
        auth_payload = [
            2,"TA2200001",'Authorize',{"idTag": "2000202204111389"}]
        await websocket.send(json.dumps(auth_payload))

        # Charging
        charge_payload = [
            2,"TA2200001",'StatusNotification',{'connectorId':2,'errorCode':'NoError',"status": "Charging",
                                              'timestamp':datetime.now(timezone.utc).isoformat()}]
        await websocket.send(json.dumps(charge_payload))

        # Start Charging
        start_payload = [
            2,"TA2200001",'2000202204111389','StartTransaction',{'connectorId':2,
                                                'meterStart':15813,
                                                "idTag": "2000202204111389",
                                              'timestamp':datetime.now(timezone.utc).isoformat()}]
        await websocket.send(json.dumps(start_payload))

        # Stop Charging
        stop_payload = [
            2, "TA2200001",'RemoteStopTransaction', {'connectorId': 2, "idTag": "2000202204111389",}]
        await websocket.send(json.dumps(start_payload))
        auth_response = await websocket.recv()
        print(f"Received auth response: {auth_response}")
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

asyncio.run(authenticate_and_send_remote_start())

