from distutils.version import Version
import sys
import threading
import argparse
import time
import struct

from importlib_metadata import version
from tuntap import TunTap
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
        nodeTun = TunTap(nic_type="Tun", nic_name="longge")
        nodeTun.config(ip="192.168.1.2", mask="255.255.255.0")
        header = {
            "VERSION": "0b0100", 
            "IHL": "0b0101",
            "DSCP": "0b000000",
            "ECN": "0b00",
            "TotLen": "0x003c",
            "Identification": "0x2c2d",
            "Flags": "0b000",
            "FragmentOffset": "0b0000000000000",
            "TTL": "0x80",
            "Protocol": "0x01",
            "Checksum": "0x0000",
            "Source": "0xc0a80102",
            "Destination": "0xc0a80101"
        }

    if role == 0:
        # Base
        baseTun = TunTap(nic_type="Tun", nic_name="longge")
        baseTun.config(ip="192.168.1.1", mask="255.255.255.0")
        header = {
            "VERSION": "0b0100", 
            "IHL": "0b0101",
            "DSCP": "0b000000",
            "ECN": "0b00",
            "TotLen": "0x003c",
            "Identification": "0x2c2d",
            "Flags": "0b000", # 0b001 when excpecting more fragments
            "FragmentOffset": "0b0000000000000", # Used when fragmenting
            "TTL": "0x80",
            "Protocol": "0x01",
            "Checksum": "0x0000",
            "Source": "0xc0a80101",
            "Destination": "0xc0a80102"
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
            pSize = rx_radio.getDynamicPayloadSize()
            buffer = rx_radio.read(pSize)
            fString = ">" + str(pSize) + "s"
            payload.append(struct.unpack(fString, buffer)[0])

            print(
                "Received {} bytes on pipe {}: {}".format(
                    len(buffer),
                    pipe_number,
                    payload[-1]
                )
            )


def tx():
    tx_radio.stopListening()
    message = b'hi'
    pSize = len(message)
    fString = ">"+str(pSize)+"s"
    buffer = struct.pack(fString, message)

    while(True):
        result = tx_radio.write(buffer)
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
        tx()
    else:
        rx()
#    check = True
#    while check:
#        pass
        # Kolla om transmit
        # Kolla receive
        # Om tom skicka


if __name__ == "__main__":
    main()
