from threading import Thread
import math

class PiCalculation:
	sum = 0
	
	def setSum(self, subTotal):
		self.sum += subTotal

	def calculateSum(self, n, numberOfThreads):
		threads = []

		# Spawning threads
		for i in range(numberOfThreads):
			t = Thread(target=self.calculateSubTotal(i, n), args=())
			threads.append(t)

		# Starting threads
		for i in range(numberOfThreads):
			threads[i].start()

		# Locking the script until all threads complete
		for i in range(numberOfThreads):
			threads[i].join()

	def calculateSubTotal(self, threadId, n):
		for i in range(n):
			if(i % n == threadId):
				self.setSum(math.pow(-1, i) / (2 * i + 1))


def main():
	n = int(input("Wie viele Teilsummen sollen genutzt werden? ")) 
	numberOfThreads = int(input("Wie viele Threads sollen erzeugt werden? "))
	piCalc = PiCalculation()
	piCalc.calculateSum(n, numberOfThreads)
	print(piCalc.sum * 4)


if __name__ == "__main__":
	main()