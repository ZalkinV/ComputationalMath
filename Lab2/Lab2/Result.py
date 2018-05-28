import numpy

def Function(x):
	return numpy.log10(x + 2) / x

def GetInputData():
	print("Не вводите ничего и нажимайте Enter для использования значений по умолчанию.\n")
	while True:
		inputString = "Введите через пробел начало и конец промежутка интегрирования: "
		boundList = input(inputString).split(" ")

		if (len(boundList) >= 2):
			try:
				begin = float(boundList[0])
				end = float(boundList[1])

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
			print("Будет использован промежуток по умолчанию [1.2; 2]")
			begin = 1.2
			end = 2
		
		try:
			count = input("Введите количество внутренних промежутков: ")
			if (count == ""):
				count = 0
			elif (int(count) < 1):
				raise ValueError
		except (ValueError, TypeError):
				print("Нужно вводить целые числа большие 0. Попробуйте ещё раз!\n")
		break
	return (begin, end, int(count))

class DefiniteIntegral:
	def __init__(self, function, begin, end, interCount):
		self.Func = function
		self.__n = interCount
		self.__a = begin
		self.__b = end
		self.__prec = 700
		self.__x = numpy.linspace(begin, end, interCount + 1)
		self.__step = self.__x[1] - self.__x[0]
		self.__realRes = None
		self.__midpointRes = None
		self.__trapezoidRes = None
		self.__simpsonRes = None
		pass

	def CalcRealValue(self):
		self.realRes = numpy.log1p(1) * numpy.log1p(self.__b / self.__a - 1)

		for i in range(1, self.__prec):
			self.realRes += (((-1) ** (i + 1)) * (self.__b ** i - self.__a ** i)) / (2 ** i * i ** 2)

		self.realRes = self.realRes / numpy.log1p(9)
		return self.realRes

	def MidpointRule(self):
		if (self.__midpointRes == None):
			sum = 0
			for i in range(self.__n):
				sum += self.Func((self.__x[i] + self.__x[i + 1]) / 2)

			self.__midpointRes = self.__step * sum

		return self.__midpointRes

	def TrapezoidRule(self):
		if (self.__trapezoidRes == None):
			sum = 0
			for i in range(self.__n):
				sum += (self.Func(self.__x[i]) + self.Func(self.__x[i+1]))/2

			self.__trapezoidRes = self.__step * sum

		return self.__trapezoidRes

	def SimpsonRule(self):
		if (self.__simpsonRes == None):
			count = self.__n
			if (count % 2 != 0):
				count += 1
				print("Значение интеграла по правилу Симпсона будет рассчитано для n={0}, так как количество промежутков должно быть чётным.".format(count))

			sum = self.Func(self.__a) + self.Func(self.__b)
			for i in range(1, self.__n):
				sum += self.Func(self.__x[i]) * (i % 2 + 1) * 2
		
			self.simpsonRes = (self.__step / 3) * sum

		return self.simpsonRes

	def PrintResults(self):
		print("\nn = ", self.__n, ":", sep='')

		if (self.__a == 1.2 and self.__b == 2):
			realValue = self.CalcRealValue()
			self.PrintMethodResult("Mid-Point", self.MidpointRule(), realValue)
			self.PrintMethodResult("Trapezoid", self.TrapezoidRule(), realValue)
			self.PrintMethodResult("Simpson's", self.SimpsonRule(), realValue)
		else:
			self.PrintMethodResult("Mid-Point", self.MidpointRule())
			self.PrintMethodResult("Trapezoid", self.TrapezoidRule())
			self.PrintMethodResult("Simpson's", self.SimpsonRule())
		pass

	def PrintMethodResult(self, methodName, *args):
		precision = 6
		approx = round(args[0], precision)
		if (len(args) > 0):
			print("\t{0} method: {1}".format(methodName, approx), end='')
		if (len(args) == 2):
			real = round(args[1], precision)
			print("\tError= {0}".format(round(approx - real, precision)), end='')
		print()
		pass

def Main():
	inputData = GetInputData()
	begin = inputData[0]
	end = inputData[1]
	intervalCount = inputData[2]

	if (intervalCount == 0):
		for i in [2 ** x for x in range(9)]:
			integral = DefiniteIntegral(Function, begin, end, i)
			integral.PrintResults()
			del integral
	else:
		integral = DefiniteIntegral(Function, begin, end, intervalCount)
		integral.PrintResults()
	pass

Main()