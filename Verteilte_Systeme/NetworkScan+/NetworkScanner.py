import netifaces
import winreg as wr
from Scan import NetworkScanner


class NetworkScannerMenu():
    ipadress = None
    netmask = None
    usedInterfaces = []

    def __init__(self):
        pass

    def printNetworkInterfaces(self):
        print("########################################")
        print("Bitte wählen Sie eine Netzwerkkarte aus:")
        allInterfaces = netifaces.interfaces()
        index = 0
        for interface in allInterfaces:
            checkIP = False
            try:
                ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            except KeyError:
                checkIP = True
                continue
            finally:
                if checkIP is False:
                    if ip != '127.0.0.1':
                        self.usedInterfaces.append(interface)
                        print(index, 'Interface: ' + self.getConnectionNameFromGuID(interface))
                        mac = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
                        print('Mac addr: ' + mac)
                        print('IP addr: {0} '.format(ip))
                        index += 1

    def getInterfaceInputFromUser(self):
        print("########################################")
        chooseNetworkInterface = int(input("Eingabe: "))
        print("########################################")
        choosenNetworkInterface = netifaces.ifaddresses(self.usedInterfaces[chooseNetworkInterface])
        self.ipadress = choosenNetworkInterface[netifaces.AF_INET][0]['addr']
        self.netmask = choosenNetworkInterface[netifaces.AF_INET][0]['netmask']

    def startScanProcedure(self):
        NetworkScanner(self.ipadress, self.netmask)

    # Windows only
    def getConnectionNameFromGuID(self, interfaceGUID):
        iface_name = ""
        reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
        reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
        try:
            reg_subkey = wr.OpenKey(reg_key, interfaceGUID + r'\Connection')
            iface_name = wr.QueryValueEx(reg_subkey, 'Name')[0]
        except FileNotFoundError:
            pass
        return iface_name
