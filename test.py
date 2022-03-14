import struct
import random


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
            id = '0xFFFF'
            fragments.append(id + data[:max_size])
        else:
            fragments.append(format(id, '#06x') + data[:max_size])
            
        data = data[max_size:]
        id += 1
    
    
    return fragments   



def fragmentTest():
    data = [random.randint(0, 255) for _ in range(100)]
    print(bytes(data))
    print(data)
    print(len(data))
    print(sum(data))
    print('\n')
    
    
    fragments = fragment(bytes(data))
    print(fragments)
    print(len(fragment(bytes(data))))
    fragSum = 0 
    for i in fragments:
        fragSum += int.from_bytes(i, "big")
        print(int.from_bytes(i,"big")) 
        
        print('\n')
    
    print(fragSum)

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