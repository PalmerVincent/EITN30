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
    
    x = np.linspace(1.005, 0.055, 95)

    x = np.append(x, np.linspace(0.052275, 0.0005, 20))
    
    print(latency)
    print(packet)
    print(len(latency))
    print(len(packet))
    print(len(x))
    
    fig, axs = plt.subplots(nrows=2, ncols=1)
        
    axs[0].plot(x, latency)
    axs[0].set_xlim(0.03, -0.01)
    axs[0].set_ylim(-1000, 15000)
    axs[0].set_ylabel("Average latency (ms)")
    
    axs[1].plot(x, packet)
    axs[1].set_xlim(0.03, -0.01)
    axs[1].set_ylim(-10, 100)
    axs[1].set_ylabel("Average packet loss (%)")
    
    axs[1].set_xlabel("Time per packet")
    
    plt.show()

    fig.suptitle("Plots")
    

if __name__ == "__main__":
    main()
    