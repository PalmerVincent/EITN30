import struct
import random

def fragment(data):
    
    fragments = []
    
    nbrParts = 0
    dataLength = len(data)
    
    max_size = 30
    
    if ((dataLength % max_size) == 0):
        nbrParts = dataLength / max_size
        
    else:
        nbrParts = int((dataLength - (dataLength % max_size)) / max_size) + 1

        padding = [0 for _ in range(max_size - (dataLength % max_size))]
        
        padding[len(padding) - 1] += len(padding)
        
        data += bytes(padding)
    
    while data:
        fragments.append(data[:max_size])
        data = data[max_size:]
    
    return fragments   


if __name__ == '__main__':
    data = [random.randint(0, 255) for _ in range(100)]
    print(bytes(data))
    print('\n')
    print(fragment(bytes(data)))