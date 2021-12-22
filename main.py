import csv
from datetime import date, datetime
from os import walk
from tkinter import *
from itertools import count
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
filePath = ''
k = 0


def show():
    fig = plt.figure(figsize=(10, 10))
    makeCsv()
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


def plotButton():
    global k
    if k == 0:
        k = 1

        def savePdf():
            plt.savefig('plotTry.pdf')

        def savePng():
            plt.savefig('plotTry.png')

        b1 = Button(text="Save as Png", command=savePng)
        b1.place(x=200, y=400, width=150)
        b2 = Button(text="Save as Pdf", command=savePdf)
        b2.place(x=200, y=350, width=150)
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

    plt.subplot(2, 4, 8)
    plotButton()
    plt.plot()
    dataToCsv()


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
        disk_in_1 = disk_stat[2]
        disk_out_1 = disk_stat[3]
        disk_stat = psutil.disk_io_counters()
        disk_in_2 = disk_stat[2]
        disk_out_2 = disk_stat[3]
        disk_in = round((disk_in_2 - disk_in_1) / 1024 / 1024, 3)
        disk_out = round((disk_out_2 - disk_out_1) / 1024 / 1024, 3)
        lastDiskStat = disk_stat
        return [disk_in * 8, disk_out * 8]


def dataToCsv():
    global filePath
    global yNetRecvSpeed, yNetSentSpeed, yDiskSpeedRead, y_val, y_val1, yDiskSpeedWrite
    with open(filePath, 'a') as f:
        writer = csv.writer(f)
        data = [y_val1[-1], y_val[-1], psutil.disk_usage('/').percent, yDiskSpeedWrite[-1], yDiskSpeedRead[-1],
                yNetRecvSpeed[-1], yNetSentSpeed[-1]]
        writer.writerow(data)
        f.close()


def makeCsv():
    global filePath
    time = datetime.now()
    path = time.strftime("%d") + time.strftime("%m") + time.strftime("%y")
    path = path + "hm" + time.strftime("%H%M")
    completePath = 'history/' + path + '.csv'
    header = ['CPU usage', 'Memory', 'Disk Usage', 'Disk write speed',
              'Disk read speed', 'Wi-Fi speed receive', 'Wi-Fi speed Send']
    filePath = completePath
    with open(completePath, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)


def getAvailableData():
    f = []
    filenamesT = tuple()
    for (dirpath, dirnames, filenames) in walk('history/'):
        f.extend(filenames)
        filenamesT = filenamesT + tuple(filenames)
    return filenamesT


class History:
    xMemory = []
    xCpu = []
    xNetSentSpeed = []
    xNetRecvSpeed = []
    xDiskSpeedWrite = []
    xDiskSpeedRead = []
    xDiskUsage = []

    def clearValues(self):
        self.xMemory = []
        self.xCpu = []
        self.xNetSentSpeed = []
        self.xNetRecvSpeed = []
        self.xDiskSpeedWrite = []
        self.xDiskSpeedRead = []
        self.xDiskUsage = []

    def plotOption(self):
        path = 'history/' + variable.get()
        self.clearValues()
        file = open(path)
        csvReader = csv.reader(file)
        ok = 0
        for row in csvReader:
            if len(row) > 1 and ok == 1:
                self.xCpu.append(float(row[0]))
                self.xMemory.append(float(row[1]))
                self.xDiskUsage.append(float(row[2]))
                self.xDiskSpeedWrite.append(float(row[3]))
                self.xDiskSpeedRead.append(float(row[4]))
                self.xNetRecvSpeed.append(float(row[5]))
                self.xNetSentSpeed.append(float(row[6]))
            ok = 1
        self.plotTry()
    def plotDisk(self):
        y = np.array([float(self.xDiskUsage[-1]), float(100-self.xDiskUsage[-1])])
        myLabels = ["Used", "Not used"]
        plt.title("Disk usage")
        myExplode = [0.2, 0]
        plt.pie(y, labels=myLabels, explode=myExplode, shadow=True, autopct='%1.2f%%')

    def plotData(self, data):
        y = []
        for i in range(0, len(self.xMemory)):
            y.append(i)
        yPoints = np.array(y)

        if data == "Memory":
            xPoints = np.array(self.xMemory)
            plt.plot(yPoints, xPoints, color="firebrick", linestyle="--")
        elif data == "Cpu":
            xPoints = np.array(self.xCpu)
            plt.fill_between(yPoints,xPoints, alpha=0.25, color="magenta")
            plt.plot(yPoints,xPoints, color="magenta")
        elif data == "NetRec":
            xPoints = np.array(self.xNetRecvSpeed)
            plt.plot(yPoints,xPoints, color="darkviolet")
        elif data == "NetSend":
            xPoints = np.array(self.xNetSentSpeed)
            plt.fill_between(yPoints, xPoints, alpha=0.25, color="salmon")
            plt.plot(yPoints,xPoints, color="magenta", linestyle="--")
        elif data == "DiskRead":
            xPoints = np.array(self.xDiskSpeedRead)
            plt.fill_between(yPoints,xPoints, alpha=0.45, color="dodgerblue")
            plt.plot(yPoints,xPoints, color="dodgerblue", linestyle="-.")
        else:
            xPoints = np.array(self.xDiskSpeedWrite)
            plt.plot(yPoints, xPoints, color="deeppink", linestyle="-.")
        plt.title(data)
        plt.ylabel("percent")
        plt.xlabel("Time")

    def plotTry(self):
        fig = plt.figure(figsize=(11, 8))
        fig.canvas.set_window_title('Setting up window title.')
        fig.subplots_adjust(bottom=0.020, left=0.20, top=0.900, right=0.800)
        plt.title(variable.get())
        plt.subplot(3, 2, 1)
        self.plotData("Memory")

        plt.subplot(3, 2, 2)
        self.plotData("Cpu")

        plt.subplot(3, 3, 4)
        self.plotData("NetRec")

        plt.subplot(3, 3, 5)
        self.plotData("NetSend")

        plt.subplot(3, 3, 6)
        self.plotData("DiskRead")


        plt.subplot(3, 2, 5)
        self.plotData("DiscWrite")

        plt.subplot(3, 2, 6)
        self.plotDisk()

        plt.show()


if __name__ == '__main__':
    root = Tk()
    root.title('Task Manager')
    root.geometry("500x500")

    my_button = Button(root, text="Task manager", command=show)
    my_button.place(x=200, y=200, width=150)
    global variable
    variable = StringVar(root)
    variable.set("Chose Date")  # default value
    choices = tuple("")
    choices = choices + getAvailableData()
    w = OptionMenu(root, variable, *choices)
    w.pack()
    w.place(x=100, y=300, width=150)

    v = History()
    button = Button(root, text="View History", command=v.plotOption)
    button.pack()
    button.place(x=290, y=300, width=150)
    root.mainloop()
    # v.plotTry()
