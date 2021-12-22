import csv
import numpy as np
from matplotlib import pyplot as plt
import main
import Variable
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
        path = 'history/' + Variable.variable.get()
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
        plt.title(Variable.variable.get())
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

