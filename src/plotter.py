import numpy as np
import matplotlib.pyplot as plt

def main():
    print("Hit")
    delay = []
    packet = []
    
    with open("test2.txt", "r") as f:
        for line in f:
            print(line)
            l = line.split()[3].split("/")
            print(l[1])
            delay.append(float(l[1]))
    
    with open("test.txt", "r") as f:
        for line in f:
            print(line)
            l = line.split()
            print(l)
            packet.append(float(l[5][:-1]))
            
    
    x = np.linspace(0.005, 1.005, 100)
    
    print(delay)
    print(packet)
    #plt.plot(x, delay)
    #plt.plot(x, packet)
    #plt.show()

if __name__ == "__main__":
    main()
    