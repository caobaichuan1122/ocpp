import asyncio
import json

import websockets

async def send_request(websocket, request):
    await websocket.send(request)
    response = await websocket.recv()
    return response

async def remote_start_transaction(websocket, id_tag, connector_id=None, charging_profile=None):
    request_id = 2
    request_payload = {
        "idTag": id_tag
    }
    if connector_id is not None:
        request_payload["connectorId"] = connector_id
    if charging_profile is not None:
        request_payload["chargingProfile"] = {
            "chargingProfileId": 1,
            "transactionId": 0,
            "chargingProfileKind": "Absolute",
            "chargingSchedule": {
                "chargingRateUnit": "A",
                "chargingSchedulePeriod": charging_profile
            }
        }
    request = [{
        "messageId": 2,
        "connectorId": str(request_id),
        "data": request_payload
    }]
    request_str = json.dumps(request)
    response = await send_request(websocket, request_str)
    response_id, status, _ = response.values()
    if response_id == request_id and status == "Accepted":
        return True
    return False

async def main():
    async with websockets.connect('ws://tpterp.com:9000/test', subprotocols=["ocpp1.6"]) as websocket:
        id_tag = "2000202204111389"
        connector_id = 2
        charging_profile = [{
            "startPeriod": 0,
            "limit": 16
        }]
        result = await remote_start_transaction(websocket, id_tag, connector_id, charging_profile)
        if result:
            print("Remote start transaction successful")
        else:
            print("Remote start transaction failed")

asyncio.run(main())