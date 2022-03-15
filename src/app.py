
import threading
import time
from tuntap import TunTap
from RF24 import RF24, RF24_PA_LOW, RF24_2MBPS, RF24_CRC_16, RF24_CRC_8

# Constants used in setup
FRAG_SIZE = 30
CHANNEL_NUMBER = 100
RADIO_POWER = RF24_PA_LOW
DATA_RATE = RF24_2MBPS
RETRIES_COUNT = 15
RETRIES_DELAY = 5  # 0-15
AUTO_ACK = True
CRC_LENGTH = RF24_CRC_16

# Define radios
tx_radio = RF24(17, 0)
rx_radio = RF24(27, 10)

# Define tun device
tun = TunTap(nic_type="Tun", nic_name="longge")


cond_in = threading.Condition()
tun_in_queue = []

cond_out = threading.Condition()
tun_out_queue = []


def setup(role):

    # configure tun device
    if role == 1:
        # Node
        tun.config(ip="192.168.1.2", mask="255.255.255.0")

    if role == 0:
        # Base
        tun.config(ip="192.168.1.1", mask="255.255.255.0")

    # start radios and configure values
    if not tx_radio.begin():
        tx_radio.printPrettyDetails()
        raise RuntimeError("tx_radio hardware is not responding")

    if not rx_radio.begin():
        rx_radio.printPrettyDetails()
        raise RuntimeError("rx_radio hardware is not responding")

    tx_radio.setPALevel(RADIO_POWER)
    rx_radio.setPALevel(RADIO_POWER)

    tx_radio.setRetries(RETRIES_DELAY, RETRIES_COUNT)
    rx_radio.setRetries(RETRIES_DELAY, RETRIES_COUNT)

    tx_radio.setChannel(CHANNEL_NUMBER)
    rx_radio.setChannel(CHANNEL_NUMBER)

    tx_radio.setDataRate(DATA_RATE)
    rx_radio.setDataRate(DATA_RATE)

    tx_radio.enableDynamicPayloads()
    rx_radio.enableDynamicPayloads()

    tx_radio.setAutoAck(AUTO_ACK)
    rx_radio.setAutoAck(AUTO_ACK)

    tx_radio.setCRCLength(CRC_LENGTH)
    rx_radio.setCRCLength(CRC_LENGTH)

    # Set addresses for writing and reading pipes
    addr = [b"base", b"node"]

    tx_radio.openWritingPipe(addr[role])
    rx_radio.openReadingPipe(1, addr[not role])

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
    """ Transmit packet to the active writing pipe. Fragments bytes if needed.

    Args:
        packet (bytes): bytes to be transmitted

    """
    tx_radio.stopListening()
    fragments = fragment(packet)

    for frag in fragments:
        result = tx_radio.write(frag)
        if (result):
            print("Frag sent id: ", frag[:2])
        else:
            print("Frag not sent: ", frag[:2])


def radio_tx():
    while True:
        with cond_in:
            cond_in.wait_for(len(tun_in_queue) > 0)
            packet = tun_in_queue.pop()
        tx(packet)


def tun_rx():
    """ Waits for new packets from tun device
    and forwards the packet to radio writing pipe
    """
    while True:
        buffer = tun.read()
        cond_in.acquire()
        tun_in_queue.append(buffer)
        cond_in.release()
        cond_in.notify_all()
        print("Got package from tun interface:\n\t", buffer, "\n")


def radio_rx():
    """ Waits for incoming packet on reading pipe 
    and forwards the packet to tun interface
    """
    rx_radio.startListening()
    buffer = []
    while True:
        has_payload, _ = rx_radio.available_pipe()
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
                cond_out.acquire()
                tun_out_queue.append(packet)
                cond_out.release()
                cond_out.notify_all()


def tun_tx():

    while True:
        with cond_out:
            cond_out.wait_for(len(tun_out_queue) > 0)
            packet = tun_out_queue.pop()
        tun.write(packet)


def main():
    radio_rx_t = threading.Thread(target=radio_rx, args=())
    radio_tx_t = threading.Thread(target=radio_tx, args=())
    tun_rx_t = threading.Thread(target=tun_rx, args=())
    tun_tx_t = threading.Thread(target=tun_tx, args=())

    radio_rx_t.start()
    radio_tx_t.start()
    time.sleep(0.05)
    tun_rx_t.start()
    tun_tx_t.start()

    radio_rx_t.join()
    radio_tx_t.join()
    tun_rx_t.join()
    tun_tx_t.join()


if __name__ == "__main__":
    role = int(
        input("Select role of machine. Enter '0' for base and '1' for node: "))
    setup(role)
    main()
