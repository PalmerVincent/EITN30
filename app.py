import sys
import argparse
import time
import struct
from RF24 import RF24, RF24_PA_LOW

address =[b"base",b"node1"] # [Transmit address, Receive address]

def setup():

    tx_radio = RF24(17, 0)
    rx_radio = RF24(27, 60)



    if not (tx_radio.begin() and rx_radio.begin()):
        raise RuntimeError("radio hardware is not responding")

    tx_radio.setPALevel(RF24_PA_LOW)
    rx_radio.setPALevel(RF24_PA_LOW)

    #tx_radio.setAutoAck(False)
    #rx_radio.setAutoAck(False)

    tx_radio.openWritingPipe(address[1])
    rx_radio.openReadingPipe(1, address[0])

    tx_radio.enableDynamicPayloads()
    rx_radio.enableDynamicPayloads()

    tx_radio.flush_tx()
    rx_radio.flush_rx()

    tx_radio.stopListening()
    rx_radio.startListening()

    return tx_radio, rx_radio


def initialize():
    pass

def rx(rx_radio):

    payload = []

    while(True):
        has_payload, pipe_number = rx_radio.available_pipe()
        if(has_payload):
            payload_size = rx_radio.getDynamicPayloadSize()
            payload = rx_radio.read(payload_size)
            print(payload)







def tx(tx_radio):
    buffer = struct.pack(">s", "Hello")

    result = tx_radio.write(buffer)

    if (result):
        print("Sent successfully")
    else:
        print("Not successful")


def encrypt():
    pass

def decrypt():
    pass


def main():
    role = input("select role 1 tx 2 rx")
    tx_radio, rx_radio = setup()
    print(f"TX: {tx_radio}, RX: {rx_radio}")
    if role == 1:
      tx(tx_radio)
    else:
      rx(rx_radio)
#    check = True
#    while check:
#        pass
        # Kolla om transmit
        # Kolla receive
        # Om tom skicka

if __name__ == "__main__":
    main()
