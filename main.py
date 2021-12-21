from tkinter import *
from itertools import count
from time import sleep
import psutil
import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation
import numpy as np

y_val = []
x_val = []
y_val1 = []
x_val1 = []
yDiskSpeedWrite = []
xDiskSpeedWrite = []
yDiskSpeedRead = []
xDiskSpeedRead = []
yNetSentSpeed = []
xNetSentSpeed = []
yNetRecvSpeed = []
xNetRecvSpeed = []
lastDiskWrite = 0
lastNetStat = 0
indexNet = 0
index = count()
indexDisk = 0
lastDiskStat = 0

def show():
    plt.figure(figsize=(10, 10))
    ani = FuncAnimation(plt.gcf(), animateData, interval=1000)
    plt.tight_layout()
    plt.show()


def plotMemory():
    var = float(psutil.virtual_memory().percent)
    y_val.append(var)
    x_val.append(next(index))
    plt.cla()
    plt.plot(x_val, y_val, color="firebrick", linestyle="--")
    plt.title("Memory")
    plt.ylabel("percent")
    plt.xlabel("Time")


def plotCPU():
    var = float(psutil.cpu_percent())
    y_val1.append(var)
    x_val1.append(next(index))
    plt.cla()
    plt.fill_between(x_val1, y_val1, alpha=0.25, color="magenta")
    plt.title("CPU percent")
    plt.ylabel("percent")
    plt.xlabel("Time")
    plt.plot(x_val1, y_val1, color="magenta")


def plotDiskSpeed(i):
    var = float(disk_usage()[i])
    plt.cla()
    if i == 0:
        plt.title("Disk Write Speed")
        yDiskSpeedWrite.append(var)
        xDiskSpeedWrite.append(next(index))
        plt.fill_between(xDiskSpeedWrite, yDiskSpeedWrite, alpha=0.25, color="aquamarine")
        plt.plot(xDiskSpeedWrite, yDiskSpeedWrite, color="lawngreen")
    else:
        plt.title("Disk Read Speed")
        yDiskSpeedRead.append(var)
        xDiskSpeedRead.append(next(index))
        plt.plot(xDiskSpeedRead, yDiskSpeedRead, color="darkgreen")
    plt.ylabel("KB/s")
    plt.xlabel("Time")


def plotNetSpeed(i):
    var = float(net_usage()[i])
    if i == 0:
        plt.title("Wi-fi Speed Recv")
        yNetSentSpeed.append(var)
        xNetSentSpeed.append(next(index))
        plt.fill_between(xNetSentSpeed, yNetSentSpeed, alpha=0.25, color="aquamarine")
        plt.plot(xNetSentSpeed, yNetSentSpeed, color="aquamarine")
    else:
        plt.title("Wi-fi Speed Sent")
        yNetRecvSpeed.append(var)
        xNetRecvSpeed.append(next(index))
        plt.fill_between(xNetRecvSpeed, yNetRecvSpeed, alpha=0.25, color="darkgreen")
        plt.plot(xNetRecvSpeed, yNetRecvSpeed, color="darkgreen")

    plt.ylabel("KB/s")
    plt.xlabel("Time")


def plotDisk():
    disk = psutil.disk_usage('/').percent
    y = np.array([disk, 100 - disk])
    myLabels = ["Used", "Not used"]
    plt.title("Disk usage")
    myExplode = [0.2, 0]
    plt.pie(y, labels=myLabels, explode=myExplode, shadow=True, autopct='%1.2f%%')
    plt.show()


def animateData(i):
    plt.subplot(2, 4, 1)
    plotMemory()

    plt.subplot(2, 4, 2)
    plotCPU()

    plt.subplot(2, 4, 3)
    plotDisk()

    plt.subplot(2, 4, 4)
    plotNetSpeed(0)

    plt.subplot(2, 4, 5)
    plotDiskSpeed(0)

    plt.subplot(2, 4, 7)
    plotNetSpeed(1)

    plt.subplot(2, 4, 6)
    plotDiskSpeed(1)

    plt.plot()


def net_usage(inf="Wi-Fi"):
    global indexNet
    global lastNetStat
    if indexNet == 0:
        lastNetStat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
        net_in_1 = lastNetStat.bytes_recv
        net_out_1 = lastNetStat.bytes_sent
        net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
        net_in_2 = net_stat.bytes_recv
        net_out_2 = net_stat.bytes_sent

        net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
        net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)
        lastNetStat = net_stat
        indexNet = indexNet + 1
        return [net_in * 8, net_out * 8]
    else:
        net_stat = lastNetStat
        net_in_1 = net_stat.bytes_recv
        net_out_1 = net_stat.bytes_sent
        net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
        net_in_2 = net_stat.bytes_recv
        net_out_2 = net_stat.bytes_sent
        net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
        net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)
        lastNetStat = net_stat
        print(f"Current net-usage:\n IIOIOIOIO IN: {net_in * 8 * 1000} MB/s, OUT: {net_out * 8*1000} MB/s")
        return [net_in * 8000, net_out * 8000]


def disk_usage():
    global indexDisk
    global lastDiskStat
    if indexDisk == 0:
        lastDiskStat = psutil.disk_io_counters()
        diskIn1 = lastDiskStat[2]
        diskOut1 = lastDiskStat[3]
        diskStat = psutil.disk_io_counters()
        diskIn2 = diskStat[2]
        diskOut2 = diskStat[3]
        diskIn = round((diskIn2 - diskIn1) / 1024 / 1024, 3)
        diskOut = round((diskOut2 - diskOut1) / 1024 / 1024, 3)
        lastDiskStat = diskStat
        indexDisk = indexDisk + 1
        return [diskIn * 8000, diskOut * 8000]
    else:
        disk_stat = lastDiskStat
        print(disk_stat)
        disk_in_1 = disk_stat[2]
        disk_out_1 = disk_stat[3]
        disk_stat = psutil.disk_io_counters()
        disk_in_2 = disk_stat[2]
        disk_out_2 = disk_stat[3]
        disk_in = round((disk_in_2 - disk_in_1) / 1024 / 1024, 3)
        disk_out = round((disk_out_2 - disk_out_1) / 1024 / 1024, 3)
        lastDiskStat = disk_stat
        return [disk_in * 8, disk_out * 8]
# def disk_usage235():
#     disk_stat = psutil.disk_io_counters()
#     disk_in_1 = disk_stat[2]
#     disk_out_1 = disk_stat[3]
#     sleep(1)
#     disk_stat = psutil.disk_io_counters()
#     disk_in_2 = disk_stat[2]
#     disk_out_2 = disk_stat[3]
#
#     disk_in = round((disk_in_2 - disk_in_1) / 1000 / 1000 , 3)
#     disk_out = round((disk_out_2 - disk_out_1) / 1000 / 1000, 3)
#     print(f"Current DISK :\nIN: {disk_in*8} MB/s, OUT: {disk_out*8} MB/s")
#     return [disk_in * 8, disk_out * 8]
# def net_usage235(inf="Wi-Fi"):
#     net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
#     net_in_1 = net_stat.bytes_recv
#     net_out_1 = net_stat.bytes_sent
#
#     sleep(1)
#     net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
#     net_in_2 = net_stat.bytes_recv
#     net_out_2 = net_stat.bytes_sent
#
#     net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
#     net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)
#     #print(f"Current net-usage:\nIN: {net_in*8} MB/s, OUT: {net_out*8} MB/s")
#     return [net_in * 8000, net_out * 8000]


if __name__ == '__main__':
    root = Tk()
    root.title('Task Manager')
    root.geometry("500x500")

    my_button = Button(root, text="Task manager", command=show)
    my_button.place(x=200, y=200, width=150)

    my_button2 = Button(root, text="History", command=show)
    my_button2.place(x=200, y=250, width=150)
    root.mainloop()
    for i in range(0, 10000):
        print("Net usage",net_usage235())
