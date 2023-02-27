import asyncio
import logging
from datetime import datetime
import random

from enums import OcppMisc as oc
from enums import ConfigurationKey as ck
import websockets

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp, call
from ocpp.v16.enums import Action, RegistrationStatus, UnlockStatus, RemoteStartStopStatus, AuthorizationStatus, \
    ChargingProfileKindType, ChargingProfilePurposeType, ChargingRateUnitType, ChargingProfileStatus
from ocpp.v16 import call_result

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):

    @on(Action.StatusNotification)
    async def on_status(self,connector_id,error_code,status,**kwargs):

        print(connector_id,error_code,status)
        return call_result.StatusNotificationPayload()

    @on(Action.Authorize)
    async def on_auth(self,id_tag,**kwargs):
        if id_tag == id_tag:
            print("authorized")
            return call_result.AuthorizePayload(
                id_tag_info={oc.status.value: AuthorizationStatus.accepted.value}
            )
        else:
            print("Not Authorized")
            return call_result.AuthorizePayload(
                id_tag_info={oc.status.value: AuthorizationStatus.invalid.value}
            )

    @on(Action.BootNotification)
    def on_boot_notification(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        notification = call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )
        return notification

    @on(Action.ChangeAvailability)
    def on_change_availability(self, connectorId, type):
        return call_result.ChangeAvailabilityPayload(
            status=RegistrationStatus.accepted
        )

    @on(Action.Heartbeat)
    def on_heartbeat(self, **kwargs):
        on_heartbeat = call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat()
        )
        return on_heartbeat

    @on(Action.MeterValues)
    def on_meter_values(self, meter_value,connector_id,**kwargs):
        # print('------------------')
        print(meter_value)
        print('------------------')
        metervalues = call_result.MeterValuesPayload()
        return metervalues


    @on(Action.GetConfiguration)
    def on_get_configuration(self,configuration_key,unknown_key,**kwargs):
        getconfiguration = call_result.GetConfigurationPayload(
            configurationkey = configuration_key,
            unknownkey = unknown_key
        )
        return getconfiguration

    @on(Action.ChangeConfiguration)
    def on_change_configuration(self, key, value):
        onchangeconfiguration = call_result.ChangeConfigurationPayload(
            status=RegistrationStatus.accepted
        )
        return onchangeconfiguration

    @on(Action.ClearCache)
    def on_clear_cache(self, **kwargs):
        onclearcache = call_result.ClearCachePayload(
            status=RegistrationStatus.accepted
        )
        return onclearcache

    @on(Action.DataTransfer)
    def on_data_transfer(self, vendor_id, message_id, data):
        ondatatransfer = call_result.DataTransferPayload(
            vendorId=vendor_id,
            messageId=message_id,
            data=data
        )
        return ondatatransfer


    @on(Action.StartTransaction)
    async def on_startTX(self, id_tag, connector_id, meter_start, timestamp, **kwargs):

        print("session for user", id_tag)
        print("valid transaction for connector, ", connector_id)
        print("meter value at start of transaction ", meter_start)
        return call_result.StartTransactionPayload(
        transaction_id=random.randint(122, 6666666666),

        id_tag_info={oc.status.value: AuthorizationStatus.accepted.value}
            )

    @on(Action.StopTransaction)
    async def on_stopTX(self,meter_stop,timestamp,transaction_id, **kwargs):
        print("Transaction stopped at value", meter_stop, " for transaction id", transaction_id,"at", timestamp)
        onstoptransaction = call_result.StopTransactionPayload(
            None
        )
        return onstoptransaction


    def on_remote_start_transaction(self,  id_tag: str,**kwargs):
        remotestarttransaction = call_result.RemoteStartTransactionPayload(
            status = RemoteStartStopStatus.accepted,
            id_tag = id_tag
        )
        return remotestarttransaction


    def on_remote_stop_transaction(self, **kwargs):
        remotestoptransaction = call_result.RemoteStopTransactionPayload(
            status = RemoteStartStopStatus.accepted
        )
        return remotestoptransaction

    async def setChargingProfile(self):
        req = call.SetChargingProfilePayload(
            connector_id=1,
            cs_charging_profiles={
                oc.charging_profile_id.value: 8,
                oc.stack_level.value: 0,
                oc.charging_profile_kind.value: ChargingProfileKindType.recurring.value,
                oc.charging_profile_purpose.value: ChargingProfilePurposeType.charge_point_max_profile.value,
                oc.charging_schedule.value: {
                    oc.charging_rate_unit.value: ChargingRateUnitType.watts,
                    oc.charging_schedule_period.value: [
                        {oc.start_period.value: 0, oc.limit.value: 100}
                    ],
                },
            },
        )
        response = await self.call(req)
        if response.status == ChargingProfileStatus.accepted:
            print("Charge profile accepted")


async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint
    instance and start listening for messages.
    """
    try:
        requested_protocols = websocket.request_headers[
            'Sec-WebSocket-Protocol']
    except KeyError:
        logging.error(
            "Client hasn't requested any Subprotocol. Closing Connection"
        )
        return await websocket.close()
    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        # In the websockets lib if no subprotocols are supported by the
        # client and the server, it proceeds without a subprotocol,
        # so we have to manually close the connection.
        logging.warning('Protocols Mismatched | Expected Subprotocols: %s,'
                        ' but client supports  %s | Closing connection',
                        websocket.available_subprotocols,
                        requested_protocols)
        return await websocket.close()

    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)
    try:
        await asyncio.gather(cp.start(), cp.remote_start_transaction())
    except websockets.exceptions.ConnectionClosed:
        connected.remove(websocket)
        print("Charge Point disconnected")
    await cp.start()





async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp1.6']
    )
    logging.info("Server Started listening to new connections...")
    print('--------------------------------------------------------------------')
    await server.wait_closed()


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
