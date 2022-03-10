import sys
import argparse
import time
import struct
from RF24 import RF24, RF24_PA_LOW


payload = []

def setup(role):
    # [base tx_radio, base rx_radio, node tx_radio, node rx_radio]

    addr = [b"base",b"node"]
    
    tx_radio = RF24(17, 0)
    rx_radio = RF24(27, 60)

    if not tx_radio.begin():
        raise RuntimeError("tx_radio hardware is not responding")

    if not rx_radio.begin():
        raise RuntimeError("rx_radio hardware is not responding")

    tx_radio.setPALevel(RF24_PA_LOW)
    rx_radio.setPALevel(RF24_PA_LOW)

    # tx_radio.setAutoAck(False)
    # rx_radio.setAutoAck(False)

    tx_radio.openWritingPipe(addr[not role])
    rx_radio.openReadingPipe(1, addr[role])

    tx_radio.enableDynamicPayloads()
    rx_radio.enableDynamicPayloads()
    # tx_radio.payloadSize = len(struct.pack(">f", 1.0))
    # rx_radio.payloadSize = len(struct.pack(">f", 1.0))
    tx_radio.flush_tx()
    rx_radio.flush_rx()

    
    

    return tx_radio, rx_radio


def initialize():
    pass


def rx(rx_radio):
    rx_radio.startListening()
    

    while(True):
        has_payload, pipe_number = rx_radio.available_pipe()
        if(has_payload):
            print(rx_radio.getDynamicPayloadSize())
            buffer = rx_radio.read(32)
            payload.append(struct.unpack(">s", buffer))

            print(
                "Received {} bytes on pipe {}: {}".format(
                    rx_radio.payloadSize,
                    pipe_number,
                    payload[-1]
                )
            )


def tx(tx_radio):
    tx_radio.stopListening()
    while(True):
        buffer = struct.pack(">s", b"hello")

        result = tx_radio.write(buffer)

        if (result):
            print("Sent successfully")
        else:
            print("Not successful")
        time.sleep(1)


def encrypt():
    pass


def decrypt():
    pass


def main():
    role = int(input("Select role of machine. Enter '0' for base and 1 for node: "))
    print("selected role: ", role, "NOT role: ", not role)
    tx_radio, rx_radio = setup(role)
    print(f"TX: {tx_radio}, RX: {rx_radio}")
    if not role:
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
