from time import gmtime, strftime
import threading
import queue
import socket
import os
import time


class Worker(threading.Thread):
    workerNumber = 0
    workerNumberFinished = 0
    portWorkers = []
    portWorkerScanStatus = {}
    openPortsByIP = {}
    ipResult = []
    portLock = threading.Lock()
    resultLock = threading.Lock()
    ipQueue = queue.Queue()
    # Default Port which are open on Linux, Mac, Windows and iOS
    openPorts = [20, 21, 22, 23, 25, 80, 111, 135, 137, 138, 139, 443, 445, 548, 631, 993, 995, 49152, 62078]

    def run(self):
        while not Worker.ipQueue.empty():
            ip = Worker.ipQueue.get()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.2)
            result = None
            for port in self.openPorts:
                result = s.connect_ex((ip, port))
                if result == 0:
                    print("Host unter folgender IP erreichbar: " + ip)
                    chunkedParts = self.chunkIt(range(1024), 10)
                    for part in chunkedParts:
                        p = threading.Thread(target=self.scanPorts, args=(ip,part))
                        p.start()
                        self.portWorkers.append(p)
                    Worker.resultLock.acquire()
                    Worker.ipResult.append(ip)
                    Worker.resultLock.release()
                    Worker.ipQueue.task_done()
                    break
            if result != 0:
                Worker.ipQueue.task_done()
        self.increaseFinishedThreadNumber()
        Worker.ipQueue.join()

    def increaseFinishedThreadNumber(self):
        Worker.workerNumberFinished = Worker.workerNumberFinished+ 1
        if Worker.workerNumberFinished == Worker.workerNumber:
            self.buildResultFile()

    def checkPortScanStatus(self):
        for k, v in Worker.portWorkerScanStatus.items():
            if v in "In Bearbeitung":
                return False
        print("Port-Scan abgeschlossen")
        return True

    def chunkIt(self, seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        return out

    def closePortWorkerThreads(self):
        pass

    def buildResultFile(self):
        while self.checkPortScanStatus() == False:
            time.sleep(5)
        self.closePortWorkerThreads()
        print("IP-Scan abgeschlossen")
        print(str(len(Worker.ipResult)) + " IP-Adressen sind erreichbar")
        currentTime = strftime('%Y-%m-%d %H:%M:%S', gmtime()).replace(":", "").replace(":", "")
        fileName = "scanresult_" + currentTime + ".txt"
        f = open(fileName, "w+")
        f.write("Scan-Ergebnis\n")
        for index, r in enumerate(Worker.ipResult):
            f.write(str(index) + ". " + r + " ist verfügbar\n")
            f.write("Folgende Ports sind offen:\n")
            for k, v in Worker.openPortsByIP.items():
                if r in k:
                    f.write("- " + str(v) + "\n")
        f.close()
        print("Log-Datei wurde erzeugt")

    def scanPorts(self, ip, part):
        self.portLock.acquire()
        Worker.portWorkerScanStatus[ip + str(part)] = "In Bearbeitung"
        self.portLock.release()
        for i in part:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.2)
            result = s.connect_ex((ip, i))
            if result == 0:
                print("Port offen! IP: " + ip + " Port: " + str(i))
                self.portLock.acquire()
                Worker.openPortsByIP[ip + str(i)] = i
                self.portLock.release()
        self.portLock.acquire()
        print("- Port Scan von " + ip + " auf "+ str(part) + " abgeschlossen")
        Worker.portWorkerScanStatus[ip + str(part)] = "Erledigt"
        self.portLock.release()
