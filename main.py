import csv
from datetime import date, datetime
from os import walk
from tkinter import *
from itertools import count
import psutil
import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import History
import Variable
class Main:
    global variable
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

    def show(self):
        fig = plt.figure(figsize=(10, 10))
        self.makeCsv()
        ani = FuncAnimation(plt.gcf(), self.animateData, interval=1000)
        plt.tight_layout()
        plt.show()

    def plotMemory(self):
        var = float(psutil.virtual_memory().percent)
        self.y_val.append(var)
        self.x_val.append(next(self.index))
        plt.cla()
        plt.plot(self.x_val, self.y_val, color="firebrick", linestyle="--")
        plt.title("Memory")
        plt.ylabel("percent")
        plt.xlabel("Time")

    def plotCPU(self):
        var = float(psutil.cpu_percent())
        self.y_val1.append(var)
        self.x_val1.append(next(self.index))
        plt.cla()
        plt.fill_between(self.x_val1, self.y_val1, alpha=0.25, color="magenta")
        plt.title("CPU percent")
        plt.ylabel("percent")
        plt.xlabel("Time")
        plt.plot(self.x_val1, self.y_val1, color="magenta")

    def plotDiskSpeed(self, i):
        var = float(self.disk_usage()[i])
        plt.cla()
        if i == 0:
            plt.title("Disk Write Speed")
            self.yDiskSpeedWrite.append(var)
            self.xDiskSpeedWrite.append(next(self.index))
            plt.fill_between(self.xDiskSpeedWrite, self.yDiskSpeedWrite, alpha=0.25, color="aquamarine")
            plt.plot(self.xDiskSpeedWrite, self.yDiskSpeedWrite, color="lawngreen")
        else:
            plt.title("Disk Read Speed")
            self.yDiskSpeedRead.append(var)
            self.xDiskSpeedRead.append(next(self.index))
            plt.plot(self.xDiskSpeedRead, self.yDiskSpeedRead, color="darkgreen")
        plt.ylabel("KB/s")
        plt.xlabel("Time")

    def plotNetSpeed(self, i):
        var = float(self.net_usage()[i])
        if i == 0:
            plt.title("Wi-fi Speed Recv")
            self.yNetSentSpeed.append(var)
            self.xNetSentSpeed.append(next(self.index))
            plt.fill_between(self.xNetSentSpeed, self.yNetSentSpeed, alpha=0.25, color="aquamarine")
            plt.plot(self.xNetSentSpeed, self.yNetSentSpeed, color="aquamarine")
        else:
            plt.title("Wi-fi Speed Sent")
            self.yNetRecvSpeed.append(var)
            self.xNetRecvSpeed.append(next(self.index))
            plt.fill_between(self.xNetRecvSpeed, self.yNetRecvSpeed, alpha=0.25, color="darkgreen")
            plt.plot(self.xNetRecvSpeed, self.yNetRecvSpeed, color="darkgreen")

        plt.ylabel("KB/s")
        plt.xlabel("Time")

    def plotDisk(self):
        disk = psutil.disk_usage('/').percent
        y = np.array([disk, 100 - disk])
        myLabels = ["Used", "Not used"]
        plt.title("Disk usage")
        myExplode = [0.2, 0]
        plt.pie(y, labels=myLabels, explode=myExplode, shadow=True, autopct='%1.2f%%')
        plt.show()

    def plotButton(self):
        #global k
        if self.k == 0:
            self.k = 1

            def savePdf():
                plt.savefig('plotTry.pdf')

            def savePng():
                plt.savefig('plotTry.png')

            b1 = Button(text="Save as Png", command=savePng)
            b1.place(x=200, y=400, width=150)
            b2 = Button(text="Save as Pdf", command=savePdf)
            b2.place(x=200, y=350, width=150)
            plt.show()

    def animateData(self, i):
        plt.subplot(2, 4, 1)
        self.plotMemory()

        plt.subplot(2, 4, 2)
        self.plotCPU()

        plt.subplot(2, 4, 3)
        self.plotDisk()

        plt.subplot(2, 4, 4)
        self.plotNetSpeed(0)

        plt.subplot(2, 4, 5)
        self.plotDiskSpeed(0)

        plt.subplot(2, 4, 7)
        self.plotNetSpeed(1)

        plt.subplot(2, 4, 6)
        self.plotDiskSpeed(1)

        plt.subplot(2, 4, 8)
        self.plotButton()
        plt.plot()
        self.dataToCsv()

    def net_usage(self, inf="Wi-Fi"):
        #self.indexNet
        #global lastNetStat
        if self.indexNet == 0:
            lastNetStat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
            net_in_1 = lastNetStat.bytes_recv
            net_out_1 = lastNetStat.bytes_sent
            net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
            net_in_2 = net_stat.bytes_recv
            net_out_2 = net_stat.bytes_sent

            net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
            net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)
            self.lastNetStat = net_stat
            self.indexNet = self.indexNet + 1
            return [net_in * 8, net_out * 8]
        else:
            net_stat = self.lastNetStat
            net_in_1 = net_stat.bytes_recv
            net_out_1 = net_stat.bytes_sent
            net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
            net_in_2 = net_stat.bytes_recv
            net_out_2 = net_stat.bytes_sent
            net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
            net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)
            self.lastNetStat = net_stat
            return [net_in * 8000, net_out * 8000]

    def disk_usage(self):
        #global indexDisk
        #global lastDiskStat
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
            disk_stat = self.lastDiskStat
            disk_in_1 = disk_stat[2]
            disk_out_1 = disk_stat[3]
            disk_stat = psutil.disk_io_counters()
            disk_in_2 = disk_stat[2]
            disk_out_2 = disk_stat[3]
            disk_in = round((disk_in_2 - disk_in_1) / 1024 / 1024, 3)
            disk_out = round((disk_out_2 - disk_out_1) / 1024 / 1024, 3)
            self.lastDiskStat = disk_stat
            return [disk_in * 8, disk_out * 8]

    def dataToCsv(self):
        #global filePath
        #global yNetRecvSpeed, yNetSentSpeed, yDiskSpeedRead, y_val, y_val1, yDiskSpeedWrite
        with open(self.filePath, 'a') as f:
            writer = csv.writer(f)
            data = [self.y_val1[-1], self.y_val[-1], psutil.disk_usage('/').percent, self.yDiskSpeedWrite[-1], self.yDiskSpeedRead[-1],
                    self.yNetRecvSpeed[-1], self.yNetSentSpeed[-1]]
            writer.writerow(data)
            f.close()

    def makeCsv(self):
        #global filePath
        time = datetime.now()
        path = time.strftime("%d") + time.strftime("%m") + time.strftime("%y")
        path = path + "hm" + time.strftime("%H%M")
        completePath = 'history/' + path + '.csv'
        header = ['CPU usage', 'Memory', 'Disk Usage', 'Disk write speed',
                  'Disk read speed', 'Wi-Fi speed receive', 'Wi-Fi speed Send']
        self.filePath = completePath
        with open(completePath, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

    def getAvailableData(self):
        f = []
        filenamesT = tuple()
        for (dirpath, dirnames, filenames) in walk('history/'):
            f.extend(filenames)
            filenamesT = filenamesT + tuple(filenames)
        return filenamesT

if __name__ == '__main__':
    root = Tk()
    root.title('Task Manager')
    root.geometry("500x500")
    main = Main()
    my_button = Button(root, text="Task manager", command=main.show)
    my_button.place(x=200, y=200, width=150)
    Variable.variable = StringVar(root)
    Variable.variable.set("Chose Date")  # default value
    choices = tuple("")
    choices = choices + main.getAvailableData()
    w = OptionMenu(root, Variable.variable, *choices)
    w.pack()
    w.place(x=100, y=300, width=150)

    v = History.History()
    button = Button(root, text="View History", command=v.plotOption)
    button.pack()
    button.place(x=290, y=300, width=150)
    root.mainloop()

