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
tun = TunTap(nic_type="Tun", nic_name="longge")
FRAG_SIZE = 30


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

        tun.config(ip="192.168.1.2", mask="255.255.255.0")

    if role == 0:
        # Base
        tun.config(ip="192.168.1.1", mask="255.255.255.0")

    # tx_radio.setAutoAck(False)
    # rx_radio.setAutoAck(False)

    tx_radio.openWritingPipe(addr[role])
    rx_radio.openReadingPipe(1, addr[not role])

    tx_radio.enableDynamicPayloads()
    rx_radio.enableDynamicPayloads()

    tx_radio.flush_tx()
    rx_radio.flush_rx()


def fragment(data: bytes) -> list:
    """ Fragments incoming binary data in bytes

    Args:
        data (bytes): Binary data converted with "bytes"

    Returns:
        list: list of fragments 
    """

    fragments = []
    dataLength = len(data)

    if (dataLength == 0):
        return

    id = 1

    while data:
        if (len(data) < 30):
            id = 65535

        fragments.append(id.to_bytes(2, 'big') + data[:FRAG_SIZE])
        data = data[FRAG_SIZE:]
        id += 1

    return fragments


def tx(packet: bytes):
    tx_radio.stopListening()
    fragments = fragment(packet)

    for frag in fragments:
        result = tx_radio.write(frag)
        if (result):
            print("Frag sent id: ", frag[:2])
        else:
            print("Frag not sent: ", frag[:2])


def tx2():
    # wait for new data from tun -> send the data over radio
    while True:
        buffer = tun.read()
        if len(buffer):
            print("Got package from tun interface:\n\t", buffer, "\n")
            tx(buffer)


def rx2():
    # wait for incoming data on radio -> send the data to tun interface
    rx_radio.startListening()
    buffer = []
    while True:
        has_payload, pipe_number = rx_radio.available_pipe()
        if has_payload:
            pSize = rx_radio.getDynamicPayloadSize()
            fragment = rx_radio.read(pSize)
            id = int.from_bytes(fragment[:2], 'big')
            print("Frag received with id: ", id)

            buffer.append(fragment[2:])

            if id == 0xFFFF:  # packet is fragmented and this is the first fragment
                packet = b''.join(buffer)
                print("Packet received:\n\t", packet, "\n")
                buffer.clear()
                tun.write(packet)


def main():
    tx_thread = threading.Thread(target=tx2, args=())
    rx_thread = threading.Thread(target=rx2, args=())

    rx_thread.start()
    tx_thread.start()

    tx_thread.join()
    rx_thread.join()


if __name__ == "__main__":
    role = int(
        input("Select role of machine. Enter '0' for base and 1 for node: "))
    setup(role)
    main()
