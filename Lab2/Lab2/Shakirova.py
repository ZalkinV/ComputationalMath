from math import log10, log1p

class DefiniteIntegral:
	def __init__ (self, n, a, b):
		self.__n = n
		self.__a = a
		self.__b = b
		self.__prec = 300
		self.__h = (self.__b - self.__a) / (self.__n - 1)
		self.__realRes = None
		self.__midpointRes = None
		self.__trapezoidalRes = None
		self.__simpsonRes = None


	def Function(self, x):
		return log10(x + 2) / x


	def RealValue(self):
		self.__realRes = log1p(1) * log1p(self.__b / self.__a - 1)

		for i in range(1, self.__prec):
			self.__realRes += (((-1)**(i + 1)) * (self.__b**i - self.__a**i)) / (2**i * i**2)

		self.__realRes = self.__realRes / log1p(9)
		pass
	
	
	def MidpointRule(self):
		self.__midpointRes = 0.0
		for i in range(0, self.__n):
			self.__midpointRes += self.Function(self.__a + self.__h * (i + 0.5))

		self.__midpointRes *= self.__h
		pass

	
	def TrapezoidalRule(self):
		sum = 0.0
		for i in range(1, self.__n - 1):
			sum += self.Function(self.__a + i * self.__h)

		self.__trapezoidalRes = self.__h * ((self.Function(self.__a) 
											 + self.Function(self.__b)) / 2 + sum)
		pass

	
	def SimpsonsRule(self):
		if (self.__n % 2 == 0):
			count = self.__n + 1
		else:
			count = self.__n


		odd = 0.0
		even = 0.0

		for i in range(2, count - 2, 2):
			odd += self.Function(self.__a + self.__h * i)
			even += self.Function(self.__a + self.__h * (i - 1))

		even += self.Function(self.__a + self.__h * (count - 2)) # так как мы не захватываем предпоследний элемент в цикле

		self.__simpsonRes = self.__h / 3.0 * (self.Function(self.__a) 
								   + self.Function(self.__b) + 2 * odd + 4 * even)
		pass

	def FormattedPrint(self):
		self.MidpointRule()
		self.TrapezoidalRule()
		self.SimpsonsRule() 
		if (self.__b <= 2):
			self.RealValue()
			print("\tMidpoint Rule    = {0}   Error = {1}"
				  .format(self.__midpointRes, abs(self.__realRes - self.__midpointRes)))
			print("\tTrapezoidal Rule = {0}   Error = {1}"
				  .format(self.__trapezoidalRes, abs(self.__realRes - self.__trapezoidalRes)))
			print("\tSimpson's Rule   = {0}   Error = {1}"
				  .format(self.__simpsonRes, abs(self.__realRes - self.__simpsonRes)))
		else:
			print("\tMidpoint Rule    = {0}".format(self.__midpointRes))
			print("\tTrapezoidal Rule = {0}".format(self.__trapezoidalRes))
			print("\tSimpson's Rule   = {0}".format(self.__simpsonRes))
		pass
		

def GetInputData():
	print("Не вводите ничего и нажимайте Enter для использования значений по умолчанию.\n")
	while True:
		inputString = "Введите через пробел начало и конец промежутка интегрирования: "
		pointList = input(inputString).split(" ")

		if (len(pointList) >= 2):
			try:
				begin = float(pointList[0])
				end = float(pointList[1])

				if (begin > end or begin <= -2):
					print("Начало промежутка должно быть меньше его конца и больше -2.")
					continue
				elif (begin <= 0 and end >= 0):
					print("Промежуток интегрирования не должен включать значение 0.")
					continue
			except (ValueError, TypeError):
				print("Нужно вводить числа. Попробуйте ещё раз!\n")
				continue
		else:
			begin = 1.2
			end = 2

		try:
			count = int(input("Введите количество интерполяционных узлов: "))
			if (count == ""):
				count = 0
			elif (int(count) < 1):
				raise ValueError
		except (ValueError, TypeError):
				print("Нужно вводить целые числа большие 0. Попробуйте ещё раз!\n")
		break
	return (begin, end, count)

def Main():
	inputData = GetInputData()
	begin = inputData[0]
	end = inputData[1]
	intervalCount = inputData[2]
	integ = DefiniteIntegral(intervalCount, begin, end)
	integ.FormattedPrint()
	pass

Main()