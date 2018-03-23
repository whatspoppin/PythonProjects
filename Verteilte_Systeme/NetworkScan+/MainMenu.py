import NetworkScanner

class MainMenu():

	def startApplication(self):
		print("Willkommen zu NetScan+")
		n = NetworkScanner.NetworkScannerMenu()
		n.printNetworkInterfaces()
		n.getInterfaceInputFromUser()
		n.startScanProcedure()		


def main():
	MainMenu().startApplication()

if __name__ == "__main__":
	main()
