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
mutex = threading.Lock()
payload = []
handled_packet = -1
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


def initialize():
    pass


def rx_tun():
    buffer = tun.read(1522)
    print(buffer)
    tx(buffer)


def rx():
    rx_radio.startListening()
    global handled_packet
    buffer = []
    while(True):
        has_payload, pipe_number = rx_radio.available_pipe()
        if has_payload:
            pSize = rx_radio.getDynamicPayloadSize()
            fragment = rx_radio.read(pSize)
            print("Frag recieved: ", fragment)

            id = int.from_bytes(fragment[:2], 'big')

            buffer.append(fragment[2:])

            if id == 0xFFFF:  # packet is fragmented and this is the first fragment
                mutex.acquire()
                handled_packet += 1
                payload.append(b''.join(buffer))

                print("Payload added: ", payload[-1])
                mutex.release()
                buffer.clear()
                
        tun.write(payload[-1])
    


def tx(packet: bytes):
    tx_radio.stopListening()
    fragments = fragment(packet)

    for frag in fragments:

        result = tx_radio.write(frag)
        if (result):
            print("Sent successfully frag: ", frag)
        else:
            print("Not successful frag: ", frag)


def txNode(packet: bytes):
    while True:
        tx(packet)
        time.sleep(1)
    

def txBase():
    tx_radio.stopListening()
    global handled_packet
    while(True):
        mutex.acquire()
        if handled_packet >= 0 and len(payload) > handled_packet:
            message = (b''.join([b'ping: ', payload[handled_packet]]))
            mutex.release()
            tx(message)
        else:
            mutex.release()
        time.sleep(0.01)


def base():
    rxThread = threading.Thread(target=rx, args=())
    txThread = threading.Thread(target=txBase, args=())

    rxThread.start()
    time.sleep(0.5)
    txThread.start()

    rxThread.join()
    txThread.join()


def node():
    destIp = input("Enter the ipv4 adress you want to ping: ")
    data = bytes(input("Enter message: "), 'utf-8')

    rxThread = threading.Thread(target=rx, args=())
    txThread = threading.Thread(
        target=txNode, args=[create_packet(destIp, data)])

    rxThread.start()
    time.sleep(0.5)
    txThread.start()

    rxThread.join()
    txThread.join()


def create_packet(dest: str, data: list) -> bytes:

    header = {
        "VERSION": 0b0100,  # 4 bits
        "IHL": 0b0101,  # 4 bits
        "DSCP": 0b000000,  # 6 bits
        "ECN": 0b00,  # 2 bits
        "TotLen": 0x003c,  # 2 bytes
        "Identification": 0x2c2d,  # 2 bytes
        "Flags": 0b000,  # 3 bits
        "FragmentOffset": 0b0000000000000,  # 13 bits
        "TTL": 0x80,  # 1 byte
        "Protocol": 0x01,  # 1 byte
        "Checksum": 0x0000,  # 2 bytes
        "Source": 0x0000,  # 4 bytes
        "Destination": 0x0000  # 4 bytes
    }

    header["Destination"] = bytes(map(int, dest.split(".")))

    header_bytes = [
        ((header["VERSION"] << 4) + header["IHL"]).to_bytes(1, 'big'),
        ((header["DSCP"] << 2) + header["ECN"]).to_bytes(1, 'big'),
        header["TotLen"].to_bytes(2, 'big'),
        header["Identification"].to_bytes(2, 'big'),
        ((header["Flags"] << 13) +
         header["FragmentOffset"]).to_bytes(2, 'big'),
        header["TTL"].to_bytes(1, 'big'),
        header["Protocol"].to_bytes(1, 'big'),
        header["Checksum"].to_bytes(1, 'big'),
        (header["Source"] & 0xFFFF).to_bytes(4, 'big'),
        header["Destination"]
    ]
    # header_bytes.append(bytes(payload))

    header_bytes.append(data)
    packet = b''.join(header_bytes)

    return packet


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


#
# def encrypt():
#    pass


# def decrypt():
#    pass
#

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
