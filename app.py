from distutils.version import Version
import sys
import threading
import argparse
import time
import struct

from importlib_metadata import version
from RF24 import RF24, RF24_PA_LOW

tx_radio = RF24(17, 0)
rx_radio = RF24(27, 60)
payload = []


def setup(role):
    addr = [b"base", b"node"]

    if not tx_radio.begin():
        tx_radio.printPrettyDetails()
        raise RuntimeError("tx_radio hardware is not responding")

    if not rx_radio.begin():
        rx_radio.printPrettyDetails()
        raise RuntimeError("rx_radio hardware is not responding")

    tx_radio.setPALevel(RF24_PA_LOW)
    rx_radio.setPALevel(RF24_PA_LOW)
    
    if role == 1:
        # Node

        IPv4 = {
            "VERSION": b"0100", 
            
            
        }
    
    if role == 0:
        # Base
        IPv4 = {
            
        }

    # tx_radio.setAutoAck(False)
    # rx_radio.setAutoAck(False)

    tx_radio.openWritingPipe(addr[role])
    rx_radio.openReadingPipe(1, addr[not role])

    tx_radio.enableDynamicPayloads()
    rx_radio.enableDynamicPayloads()

    tx_radio.flush_tx()
    rx_radio.flush_rx()


def initialize():
    pass


def rx():
    rx_radio.startListening()

    while(True):
        has_payload, pipe_number = rx_radio.available_pipe()
        if(has_payload):
            payload_size = rx_radio.getDynamicPayloadSize()
            payload = rx_radio.read(payload_size)
            print(payload)
    
            pSize = rx_radio.getDynamicPayloadSize()
            print(pSize)
            buffer = rx_radio.read(pSize)
            print(buffer)
            fString = ">" + str(pSize) + "s"
            payload.append(struct.unpack(fString, buffer)[0])

            print(
                "Received {} bytes on pipe {}: {}".format(
                    rx_radio.payloadSize,
                    pipe_number,
                    payload[-1]
                )
            )


def tx():
    tx_radio.stopListening()
    message = b'hello'
    pSize = len(message)
    fString = ">"+str(pSize)+"s"
    buffer = struct.pack(fString, message)

    while(True):

        if (result):
            print("Sent successfully")
        else:
            print("Not successful")
        time.sleep(1)


def base():
    
    pass


def node():
    pass


def encrypt():
    pass


def decrypt():
    pass


def main():
    role = int(
        input("Select role of machine. Enter '0' for base and 1 for node: "))
    setup(role)

    if not role:
        base()
    else:
        node()
#    check = True
#    while check:
#        pass
        # Kolla om transmit
        # Kolla receive
        # Om tom skicka


if __name__ == "__main__":
    main()
