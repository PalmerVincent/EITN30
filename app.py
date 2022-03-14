from distutils.version import Version
from pickle import NONE
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
            "Flags": "0b000",  # 0b001 when excpecting more fragments
            "FragmentOffset": "0b0000000000000",  # Used when fragmenting
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
            mutex.acquire()
            p = payload.append(struct.unpack(fString, buffer)[0])
            mutex.release()

            print(
                "Received {} bytes on pipe {}: {}".format(
                    len(buffer),
                    pipe_number,
                    p
                )
            )


def tx(packet: bytes):
    tx_radio.stopListening()
    fragments = fragment(packet)
    while(True):
        for frag in fragments:
            buffer = frag
            result = tx_radio.write(buffer)
            if (result):
                print("Sent successfully")
            else:
                print("Not successful")
        time.sleep(1)


def txBase():
    tx_radio.stopListening()
    i = 0
    while(True):
        mutex.acquire()
        if len(payload) >= i and len(payload) > 0:
            message = bytes("ping"+str(payload[i]), 'utf-8')
            mutex.release()
            pSize = len(message)

            fString = ">"+str(pSize)+"s"
            buffer = struct.pack(fString, message)

            result = tx_radio.write(buffer)
            if (result):
                i += 1
                print("Sent successfully")
            else:
                print("Not successful")
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
    data = bytes(input("Enter the data: "), 'utf-8')
    packet = create_packet(destIp, data)
    
    print(packet)
    rxThread = threading.Thread(target=rx, args=())
    txThread = threading.Thread(target=tx, args=[packet])

    rxThread.start()
    time.sleep(0.5)
    txThread.start()

    rxThread.join()
    txThread.join()


def create_packet(dest: str, data: bytes):
    
    header = {
            "VERSION": 0b0100, # 4 bits
            "IHL": 0b0101, # 4 bis
            "DSCP": 0b000000, # 6 bits
            "ECN": 0b00, # 2 bits
            "TotLen": 0x003c, # 2 bytes 
            "Identification": 0x2c2d, # 2 bytes
            "Flags": 0b000, # 3 bits
            "FragmentOffset": 0b0000000000000, # 13 bits
            "TTL": 0x80, # 1 byte
            "Protocol": 0x01, # 1 byte
            "Checksum": 0x0000, # 2 bytes
            "Source": 0x0000, # 4 bytes
            "Destination": 0x0000 # 4 bytes
    }
    
    header["Destination"] = bytes(map(int, dest.split(".")))
    
    header_bytes = [
        ((header["VERSION"] << 4) + header["IHL"]).to_bytes(1,'big'),
        ((header["DSCP"] << 2) + header["ECN"]).to_bytes(1, 'big'),
        header["TotLen"].to_bytes(2,'big'),
        header["Identification"].to_bytes(2,'big'),
        ((header["Flags"] << 13) + header["FragmentOffset"]).to_bytes(2,'big'), 
        header["TTL"].to_bytes(1,'big'),
        header["Protocol"].to_bytes(1,'big'),
        header["Checksum"].to_bytes(1,'big'),
        (header["Source"] & 0xFFFF).to_bytes(4,'big'),
        header["Destination"]
    ]
    #header_bytes.append(bytes(payload))
    
    header_bytes.append(data)
    packet = b''.join(header_bytes)
    
    return packet

def fragment(data) -> list:
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
    
   # nbrParts = 0
    
    
    max_size = 30
    
    #if ((dataLength % max_size) == 0):
        #nbrParts = dataLength / max_size
        
  #  else:
        #nbrParts = int((dataLength - (dataLength % max_size)) / max_size) + 1

      #  padding = [0 for _ in range(max_size - (dataLength % max_size))]
        
      #  padding[len(padding) - 1] += len(padding)
        
    #    data += bytes(padding)
    id = 1
    
    while data:
        if (len(data) < 30):
            id = 65535
            fragments.append(id.to_bytes(2, 'big') + data[:max_size])
        else:
            fragments.append(id.to_bytes(2, 'big') + data[:max_size])
            
        data = data[max_size:]
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
