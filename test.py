import struct
import random


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
    
    max_size = 30
    
    id = 1
    
    while data:
        if (len(data) < 30):
            id = 65535
           
        fragments.append(id.to_bytes(2, 'big') + data[:max_size])    
        data = data[max_size:]
        id += 1
    
    
    return fragments   



def fragmentTest():
    data = [random.randint(0, 255) for _ in range(100)]
    print(bytes(data))
    print(type(bytes(data)))
    print(len(data))
    print('\n')
    
    fragments = fragment(bytes(data))
    print(type(fragments))
    print(fragments)   
    print('\n')


def packetTest():
    header = {
            "VERSION": 0b0100, # 4 bits
            "IHL": 0b0101, # 4 bits
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
    
    #header["Destination"] = bytes(map(int, dest.split(".")))
    
    header_bytes = [
        (header["VERSION"] << 4) + header["IHL"],
        (header["DSCP"] << 2) + header["ECN"],
        header["TotLen"],
        header["Identification"],
        ((header["Flags"] << 13) + header["FragmentOffset"]), 
        header["TTL"],
        header["Protocol"],
        header["Checksum"],
        header["Source"] & 0xFFFF,
        header["Destination"]
    ]
    
    print([hex(x) for x in header_bytes])
    header_bytes.append(8)
    packet = header_bytes
    print(packet)
    
  
    
    

    
if __name__ == '__main__':
    fragmentTest()
    #packetTest()
    
    
    
    '''
mutex = threading.Lock()
payload = []
handled_packet = -1


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


def node2():
    buffer = tun.read(1522)
    print(buffer)
    tx(buffer)
    

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
'''