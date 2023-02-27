import asyncio
import json
import websockets

async def send_request(websocket, request):
    await websocket.send(request)
    response = await websocket.recv()
    return response

async def remote_stop_transaction(websocket, transaction_id, id_tag=None, meter_stop=None):
    request_id = 2
    request_payload = {
        "transactionId": transaction_id
    }
    if id_tag is not None:
        request_payload["idTag"] = id_tag
    if meter_stop is not None:
        request_payload["meterStop"] = meter_stop
    request = [
        {"messageId": "RemoteStopTransaction",
        "uniqueId": str(request_id),
        "payload": request_payload}
    ]
    request_str = json.dumps(request)
    response = await send_request(websocket, request_str.encode())
    response_data = json.loads(response)
    response_id, status, _ = response_data.values()
    if response_id == request_id and status == "Accepted":
        return True
    return False

async def main():
    async with websockets.connect('ws://tpterp.com:9000', subprotocols=["ocpp1.6"]) as websocket:
        transaction_id = 1981070030
        result = await remote_stop_transaction(websocket, transaction_id)
        if result:
            print("Remote stop transaction successful")
        else:
            print("Remote stop transaction failed")

asyncio.run(main())