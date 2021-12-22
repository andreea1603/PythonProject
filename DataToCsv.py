import csv
from datetime import datetime
import psutil


def makeCsv():
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
    return filePath


def dataToCsv(filePath, yCpu, yMemory, yDiskSpeedWrite, yDiskSpeedRead, yNetRecvSpeed, yNetSentSpeed):
    with open(filePath, 'a') as f:
        writer = csv.writer(f)
        data = [yCpu[-1], yMemory[-1], psutil.disk_usage('/').percent, yDiskSpeedWrite[-1], yDiskSpeedRead[-1],
                yNetRecvSpeed[-1], yNetSentSpeed[-1]]
        writer.writerow(data)
        f.close()
