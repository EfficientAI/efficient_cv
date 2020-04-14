from matplotlib import pyplot as plt


def main():
    timestamps = []
    avgs = []
    exps = []
    loads = []
    with open('output.txt', 'rb') as f:
        lines = f.readlines()
        for line in lines:
            timestamp, avg, exp, load = line.split()
            timestamps.append(int(timestamp))
            avgs.append(float(avg))
            exps.append(float(exp))
            loads.append(float(load))
    plt.plot(timestamps, loads)
    plt.plot(timestamps, avgs)
    plt.plot(timestamps, exps)
    plt.show()

if __name__ == "__main__":
    main()