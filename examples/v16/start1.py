import asyncio
import logging
import random
#just import selec-em2m-main script here and use readvoltage function for reading meter values
#from selec import readVoltage # change com7 port number in the selec script
#import RPi.GPIO as GPIO



import websockets
from datetime import datetime
from ocpp.v16 import call
from ocpp.v16.enums import AuthorizationStatus
from ocpp.v16 import ChargePoint as cp
from ocpp.routing import on
from ocpp.v16.enums import Action, AuthorizationStatus, RemoteStartStopStatus
from datetime import datetime
from ocpp.v16 import call
from ocpp.v16.enums import AuthorizationStatus
from ocpp.v16 import ChargePoint as cp
from ocpp.routing import on
from ocpp.v16.enums import Action, AuthorizationStatus, RemoteStartStopStatus, ConfigurationStatus, ReservationStatus, \
    AvailabilityType, AvailabilityStatus, ClearCacheStatus, ResetStatus, UnlockStatus, ReadingContext, Measurand, Location, \
    UnitOfMeasure
from ocpp.v16 import call_result
from enums import ConfigurationKey as ck
from central_system_DC import CentralSystem,ChargePoint
# class ChargePoint(cp):
#     async def send_heartbeat(self):
#         req = call.HeartbeatPayload()
#         res = await self.call(req)
#
#         print("current time received from CMS, ", res.current_time)
#
#
#     async def send_boot_notification(self):
#         request = call.BootNotificationPayload(
#             charge_point_model="Optimus", charge_point_vendor="The Mobility"
#         )
#         response = await self.call(request)
#
#         if response.status == 'Accepted':
#             print("Boot confirmed.")
#
#     @on(Action.RemoteStartTransaction)
#     async def remote_start_transaction(self, id_tag):
#
#
#         if id_tag == '2000202204111389':
#             print("Charging started remotely by CMS")
#
#             return call_result.RemoteStartTransactionPayload(status=RemoteStartStopStatus.accepted)
#
#         else:
#             return call_result.RemoteStartTransactionPayload(status=RemoteStartStopStatus.rejected)
#             print("stopped charging")

async def main():
    async with websockets.connect(
            'ws://meloongtech.com:9000/TA2200001',
            subprotocols=['ocpp1.6']
    ) as ws:


        cp = CentralSystem('TA2200001', ws)
        print(cp)

        await asyncio.gather(cp.remote_start_transaction(
            {
                'id_tag':'2000202204111389'
            }
        ))


if __name__ == '__main__':
    asyncio.run(main())