import csv
from datetime import date, datetime
from os import walk
from tkinter import *
from itertools import count
import psutil
import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation
import numpy as np

import DataToCsv
import History
import Variable
import SavePlot


def plotDisk():
    disk = psutil.disk_usage('/').percent
    y = np.array([disk, 100 - disk])
    myLabels = ["Used", "Not used"]
    plt.title("Disk usage")
    myExplode = [0.2, 0]
    plt.pie(y, labels=myLabels, explode=myExplode, shadow=True, colors=['darkorchid', 'plum'], autopct='%1.2f%%')
    plt.show()


def getAvailableData():
    f = []
    filenamesT = tuple()
    for (dirpath, dirnames, filenames) in walk('history/'):
        f.extend(filenames)
        filenamesT = filenamesT + tuple(filenames)
    return filenamesT


class Main:
    global variable
    yMemory = []
    xMemory = []
    yCpu = []
    xCpu = []
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
    filePath = ''
    k = 0

    def clearValues(self):
        self.xMemory = []
        self.xCpu = []
        self.xNetSentSpeed = []
        self.xNetRecvSpeed = []
        self.xDiskSpeedWrite = []
        self.xDiskSpeedRead = []
        self.yMemory = []
        self.yCpu = []
        self.yNetSentSpeed = []
        self.yNetRecvSpeed = []
        self.yDiskSpeedWrite = []
        self.yDiskSpeedRead = []

    def show(self):
        self.clearValues()
        fig = plt.figure(figsize=(10, 10))
        self.filePath = DataToCsv.makeCsv()
        ani = FuncAnimation(plt.gcf(), self.animateData, interval=1000)
        plt.tight_layout()
        plt.show()

    def plotMemory(self):
        var = float(psutil.virtual_memory().percent)
        self.yMemory.append(var)
        self.xMemory.append(next(self.index))
        plt.cla()
        plt.plot(self.xMemory, self.yMemory, color="magenta", linestyle="--")
        plt.fill_between(self.xMemory, self.yMemory, alpha=0.45, color="magenta")

        plt.title("Memory")
        plt.ylabel("percent")
        plt.xlabel("Time")

    def plotCPU(self):
        var = float(psutil.cpu_percent())
        self.yCpu.append(var)
        self.xCpu.append(next(self.index))
        plt.cla()
        plt.fill_between(self.xCpu, self.yCpu, alpha=0.25, color="mediumvioletred")
        plt.title("CPU percent")
        plt.ylabel("percent")
        plt.xlabel("Time")
        plt.plot(self.xCpu, self.yCpu, color="mediumvioletred")

    def plotDiskSpeed(self, i):
        var = float(self.diskUsage()[i])
        plt.cla()
        if i == 0:
            plt.title("Disk Write Speed")
            self.yDiskSpeedWrite.append(var)
            self.xDiskSpeedWrite.append(next(self.index))
            plt.fill_between(self.xDiskSpeedWrite, self.yDiskSpeedWrite, alpha=0.65, color="lightseagreen")
            plt.plot(self.xDiskSpeedWrite, self.yDiskSpeedWrite, color="lightseagreen")
        else:
            plt.title("Disk Read Speed")
            self.yDiskSpeedRead.append(var)
            self.xDiskSpeedRead.append(next(self.index))
            plt.plot(self.xDiskSpeedRead, self.yDiskSpeedRead, color="darkgreen")
        plt.ylabel("KB/s")
        plt.xlabel("Time")

    def plotNetSpeed(self, i):
        var = float(self.netUsage()[i])
        if i == 0:
            plt.title("Wi-fi Speed Recv")
            self.yNetSentSpeed.append(var)
            self.xNetSentSpeed.append(next(self.index))
            plt.fill_between(self.xNetSentSpeed, self.yNetSentSpeed, alpha=0.25, color="deepskyblue")
            plt.plot(self.xNetSentSpeed, self.yNetSentSpeed, color="deepskyblue")
        else:
            plt.title("Wi-fi Speed Sent")
            self.yNetRecvSpeed.append(var)
            self.xNetRecvSpeed.append(next(self.index))
            plt.fill_between(self.xNetRecvSpeed, self.yNetRecvSpeed, alpha=0.25, color="darkmagenta")
            plt.plot(self.xNetRecvSpeed, self.yNetRecvSpeed, color="darkmagenta")

        plt.ylabel("KB/s")
        plt.xlabel("Time")

    def animateData(self, i):
        plt.subplot(3, 2, 1)
        self.plotMemory()

        plt.subplot(3, 2, 2)
        self.plotCPU()

        plt.subplot(3, 3, 4)
        plotDisk()

        plt.subplot(3, 3, 5)
        self.plotNetSpeed(0)

        plt.subplot(3, 2, 5)
        self.plotDiskSpeed(0)

        plt.subplot(3, 3, 6)
        self.plotNetSpeed(1)

        plt.subplot(3, 2, 6)
        self.plotDiskSpeed(1)

        SavePlot.plotButton(self.k)
        plt.plot()
        DataToCsv.dataToCsv(self.filePath, self.yCpu, self.yMemory, self.yDiskSpeedWrite, self.yDiskSpeedRead, self.yNetRecvSpeed, self.yNetSentSpeed)

    def netUsage(self, inf="Wi-Fi"):
        if self.indexNet == 0:
            lastNetStat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
            netIn1 = lastNetStat.bytes_recv
            netOut1 = lastNetStat.bytes_sent
            netStat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
            netIn2 = netStat.bytes_recv
            netOut2 = netStat.bytes_sent

            netIn = round((netIn2 - netIn1) / 1024 / 1024, 3)
            netOut = round((netOut2 - netOut1) / 1024 / 1024, 3)
            self.lastNetStat = netStat
            self.indexNet = self.indexNet + 1
            return [netIn * 8, netOut * 8]
        else:
            netStat = self.lastNetStat
            netIn1 = netStat.bytes_recv
            netOut1 = netStat.bytes_sent
            netStat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
            netIn2 = netStat.bytes_recv
            netOut2 = netStat.bytes_sent
            netIn = round((netIn2 - netIn1) / 1024 / 1024, 3)
            netOut = round((netOut2 - netOut1) / 1024 / 1024, 3)
            self.lastNetStat = netStat
            return [netIn * 8000, netOut * 8000]

    def diskUsage(self):
        if self.indexDisk == 0:
            lastDiskStat = psutil.disk_io_counters()
            diskIn1 = lastDiskStat[2]
            diskOut1 = lastDiskStat[3]
            diskStat = psutil.disk_io_counters()
            diskIn2 = diskStat[2]
            diskOut2 = diskStat[3]
            diskIn = round((diskIn2 - diskIn1) / 1024 / 1024, 3)
            diskOut = round((diskOut2 - diskOut1) / 1024 / 1024, 3)
            self.lastDiskStat = diskStat
            self.indexDisk = self.indexDisk + 1
            return [diskIn * 8000, diskOut * 8000]
        else:
            diskStat = self.lastDiskStat
            diskIn1 = diskStat[2]
            diskOut1 = diskStat[3]
            diskStat = psutil.disk_io_counters()
            diskIn2 = diskStat[2]
            diskOut2 = diskStat[3]
            diskIn = round((diskIn2 - diskIn1) / 1024 / 1024, 3)
            diskOut = round((diskOut2 - diskOut1) / 1024 / 1024, 3)
            self.lastDiskStat = diskStat
            return [diskIn * 8, diskOut * 8]


def Buttons(root, main):

    my_button = Button(root, text="Task manager", command=main.show)
    my_button.place(x=200, y=200, width=150)

    Variable.variable = StringVar(root)
    Variable.variable.set("Choose Date")
    choices = tuple("")
    choices = choices + getAvailableData()
    w = OptionMenu(root, Variable.variable, *choices)
    w.pack()
    w.place(x=100, y=300, width=150)
    v = History.History()
    button = Button(root, text="View History", command=v.plotOption)
    button.pack()
    button.place(x=290, y=300, width=150)


def Menu():
    root = Tk()
    root.title('Task Manager')
    root.geometry("500x500")
    main = Main()
    Buttons(root, main)
    root.mainloop()


if __name__ == '__main__':
    Menu()
