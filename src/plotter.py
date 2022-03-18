import numpy as np
import matplotlib.pyplot as plt

def main():
    print("Hit")
    latency = []
    packet = []
    
    with open("latency.txt", "r") as f:
        for line in f:
            l = line.split(":")[1:]
            for i in l:
                i = i.split()[3].split("/")[1]
                latency.append(float(i))
    
    with open("packets.txt", "r") as f:
        for line in f:
            l = line.split(":")[1:]
            for i in l:
                packet.append(float(i.split()[5][:-1]))            
    
    x = np.linspace(1.005, 0.005, 100)
    
    print(latency)
    print(packet)
    
    fig, axs = plt.subplots(nrows=2, ncols=1)
        
    axs[0].plot(x, latency)
    axs[0].set_xlim(1.005, 0.005)
    axs[0].set_ylabel("Average latency (ms)")
    
    axs[1].plot(x, packet)
    axs[1].set_xlim(1.005, 0.005)
    axs[1].set_ylabel("Average packet loss (%)")
    
    axs[1].set_xlabel("Test")
    
    plt.show()

    fig.suptitle("Plots")

if __name__ == "__main__":
    main()
    