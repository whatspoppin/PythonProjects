import ipaddress
import _thread
from Worker import *
from netaddr import *


class NetworkScanner:
    workerThreads = []
    ipList = []

    def __init__(self, ip, netmask):
        ipNetwork = IPNetwork((ip + "/" + netmask))
        self.ipList = list(ipNetwork)
        self.createJobs()
        self.startThreads()

    def startThreads(self):
        self.workerThreads = [Worker() for i in range(30)]
        Worker.workerNumber = len(self.workerThreads)
        print("Scanvorgang wird gestartet")
        print(str(Worker.ipQueue.qsize() - 2) + " IP-Adressen werden untersucht")
        for index, thread in enumerate(self.workerThreads):
            thread.start()

    def createJobs(self):
        for ip in self.ipList:
            Worker.ipQueue.put(str(ip))
