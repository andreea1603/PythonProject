import csv
from datetime import datetime
import psutil


def makeCsv():
    """ Description: this function creates a file with the name of the current date and time and
    writes the first line in it
            """
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


def dataToCsv(file_path, y_cpu, y_memory, y_disk_speed_write, y_disk_speed_read, y_net_recv_speed, y_net_sent_speed):
    """ Description: this function adds the data at each iteration in the csv
            """
    with open(file_path, 'a') as f:
        writer = csv.writer(f)
        data = [y_cpu[-1], y_memory[-1], psutil.disk_usage('/').percent, y_disk_speed_write[-1], y_disk_speed_read[-1],
                y_net_recv_speed[-1], y_net_sent_speed[-1]]
        writer.writerow(data)
        f.close()
