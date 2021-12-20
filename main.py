# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from time import sleep

import psutil
def net_usage(inf = "Wi-Fi"):   #change the inf variable according to the interface
    net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
    net_in_1 = net_stat.bytes_recv
    net_out_1 = net_stat.bytes_sent
    sleep(0.6)
    net_stat = psutil.net_io_counters(pernic=True, nowrap=True)[inf]
    net_in_2 = net_stat.bytes_recv
    net_out_2 = net_stat.bytes_sent

    net_in = round((net_in_2 - net_in_1) / 1024 / 1024, 3)
    net_out = round((net_out_2 - net_out_1) / 1024 / 1024, 3)
    return [net_in*8, net_out*8]
def getMemory():
    var = float(psutil.virtual_memory().percent)
    return var
def getCpu():
    var = float(psutil.cpu_percent())
    return var
def getDiskWriteSpeed():
    var = float(psutil.disk_usage()[0])
    return var
def getDiskReadSpeed():
    var = float(psutil.disk_usage()[1])
    return var
def getNetSentSpeed():
    var = float(net_usage()[0])
    return var
def getNetRecvSpeed():
    var = float(net_usage()[0])
    return var
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
