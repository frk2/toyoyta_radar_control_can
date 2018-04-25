#!/usr/bin/python3

import cantools
import can
import time


"""
This file assumes that can1 is connected to the RADAR can bus (Pin 5/6 on the radar unit) and can0 to the CAR CAN bus. (pin 3/2)
"""
class OnCan(can.Listener):
    def __init__(self):
        self.db = cantools.db.load_file('opendbc/toyota_prius_2017_adas.dbc')

    def on_message_received(self, boo):
        if 0x210 <= boo.arbitration_id < 0x21F:
            msg = self.db.decode_message(boo.arbitration_id, boo.data)
            if msg["VALID"] == 1:
                print("Got VALID track at dist: " + str(msg["LONG_DIST"]))


class ECU:
    CAM = 0  # camera
    DSU = 1  # driving support unit
    APGS = 2  # advanced parking guidance system


class CAR:
    PRIUS = 0
    LEXUS_RXH = 1
    RAV4 = 2
    RAV4H = 3
    COROLLA = 4


STATIC_MSGS = [(0x141, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH, CAR.RAV4, CAR.COROLLA), 1, 2, '\x00\x00\x00\x46'),
               (0x128, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH, CAR.RAV4, CAR.COROLLA), 1, 3,
                '\xf4\x01\x90\x83\x00\x37'),
               (0x283, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH, CAR.RAV4, CAR.COROLLA), 0, 3,
                '\x00\x00\x00\x00\x00\x00\x8c'),
               # (0x2E6, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH), 0,   3, '\xff\xf8\x00\x08\x7f\xe0\x00\x4e'),
               # (0x2E7, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH), 0,   3, '\xa8\x9c\x31\x9c\x00\x00\x00\x02'),
               (0x344, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH, CAR.RAV4, CAR.COROLLA), 0, 5,
                '\x00\x00\x01\x00\x00\x00\x00\x50'),
               (0x160, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH, CAR.RAV4, CAR.COROLLA), 1, 7,
                '\x00\x00\x08\x12\x01\x31\x9c\x51'),
               (0x161, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH, CAR.RAV4, CAR.COROLLA), 1, 7,
                '\x00\x1e\x00\x00\x00\x80\x07'),
               # (0x33E, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH), 0,  20, '\x0f\xff\x26\x40\x00\x1f\x00'),
               # (0x365, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH), 0,  20, '\x00\x00\x00\x80\x03\x00\x08'),
               (0x365, ECU.DSU, (CAR.RAV4, CAR.COROLLA), 0, 20, '\x00\x00\x00\x80\xfc\x00\x08'),
               # (0x366, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH), 0,  20, '\x00\x00\x4d\x82\x40\x02\x00'),
               (0x366, ECU.DSU, (CAR.RAV4, CAR.COROLLA), 0, 20, '\x00\x72\x07\xff\x09\xfe\x00'),
               (0x4CB, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH, CAR.RAV4, CAR.COROLLA), 0, 100,
                '\x0c\x00\x00\x00\x00\x00\x00\x00'),
               # (0x470, ECU.DSU, (CAR.PRIUS, CAR.RAV4H, CAR.LEXUS_RXH), 1, 100, '\x00\x00\x02\x7a'),
               ]

if __name__ == '__main__':
    can_bus1 = can.interface.Bus(bustype='socketcan_native', channel='can0', extended=False)
    can_bus2 = can.interface.Bus(bustype='socketcan_native', channel='can1', extended=False)
    db = cantools.db.load_file('opendbc/toyota_prius_2017_pt_generated.dbc')

    # Send one time messages
    notifier = can.Notifier(can_bus2, [OnCan()], timeout=0.1)
    acc_message = db.get_message_by_name('ACC_CONTROL')
    frame = 0.
    msg = db.get_message_by_name("SPEED")
    can_bus1.send(can.Message(arbitration_id=msg.frame_id,
                              data=msg.encode({
                                  "ENCODER": 0,
                                  "SPEED": 1.44,
                                  "CHECKSUM": 0}),
                              extended_id=False))

    cruise_message = db.get_message_by_name('PCM_CRUISE')
    active_message = cruise_message.encode({"CRUISE_STATE": 9,
                                            "GAS_RELEASED": 0,
                                            "STANDSTILL_ON": 0,
                                            "ACCEL_NET": 0,
                                            "CHECKSUM": 0})
    msg = can.Message(arbitration_id=cruise_message.frame_id, data=active_message, extended_id=False)
    can_bus1.send(msg)

    msg = db.get_message_by_name("PCM_CRUISE_2")
    can_bus1.send(can.Message(arbitration_id=msg.frame_id,
                              data=msg.encode({
                                  "MAIN_ON": 0,
                                  "LOW_SPEED_LOCKOUT": 0,
                                  "SET_SPEED": 0,
                                  "CHECKSUM": 0}),
                              extended_id=False))

    msg = db.get_message_by_name("ACC_CONTROL")
    can_bus1.send(can.Message(arbitration_id=msg.frame_id,
                              data=msg.encode({
                                  "ACCEL_CMD": 0,
                                  "SET_ME_X63": 0,
                                  "RELEASE_STANDSTILL": 0,
                                  "SET_ME_1": 0,
                                  "CANCEL_REQ": 0,
                                  "CHECKSUM": 0}),
                              extended_id=False))

    msg = db.get_message_by_name("PCM_CRUISE_SM")
    can_bus1.send(can.Message(arbitration_id=msg.frame_id,
                              data=msg.encode({
                                  "MAIN_ON": 0,
                                  "CRUISE_CONTROL_STATE": 0,
                                  "UI_SET_SPEED": 0}),
                              extended_id=False))

    while True:
        # Mostly copypasted code from toyota car controller in openpilot
        if frame % 1 == 0:
            # can_bus2.send(msg)
            acc_msg = acc_message.encode(
                {"ACCEL_CMD": 0.0, "SET_ME_X63": 0x63, "SET_ME_1": 1, "RELEASE_STANDSTILL": 1, "CANCEL_REQ": 0,
                 "CHECKSUM": 113})
            msg = can.Message(arbitration_id=acc_message.frame_id, data=acc_msg, extended_id=False)
            # print("sending control command {} on bus: {}, vl: {}".format(acc_message.frame_id, 0, acc_msg))
            can_bus1.send(msg)

        for (addr, ecu, cars, bus, fr_step, vl) in STATIC_MSGS:
            if frame % fr_step == 0:
                if addr in (0x489, 0x48a) and bus == 0:
                    # add counter for those 2 messages (last 4 bits)
                    cnt = ((frame / 100) % 0xf) + 1
                    if addr == 0x48a:
                        # 0x48a has a 8 preceding the counter
                        cnt += 1 << 7
                    vl += chr(cnt)
                can_bus = None
                if bus == 0:
                    can_bus = can_bus1
                else:
                    can_bus = can_bus2
                tosend = bytearray()
                tosend.extend(map(ord, vl))
                message = can.Message(arbitration_id=addr, data=tosend, extended_id=False)
                can_bus.send(message)
                # print("sending id {} on bus: {}, vl: {}".format(addr, bus, tosend))
        frame += 1.
        time.sleep(1. / 100)
