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
	return (begin, end, count)

def Squarezoid(begin, end, count):
	x = numpy.linspace(begin, end, count+1)
	step = x[1] - x[0]
	sum = 0
	for i in range(count):
		sum += Function((x[i] + x[i + 1]) / 2)

	return step * sum

def Trapezoid(begin, end, count):
	x = numpy.linspace(begin, end, count+1)
	step = x[1] - x[0]
	sum = 0
	for i in range(count):
		sum += (Function(x[i + 1]) + Function(x[i])) / 2

	return step * sum

def Simpson(begin, end, count):
	if (count % 2 != 0):
		count += 1
		print("\tЗначение интеграла по правилу Симпсона будет рассчитано для n={0}, так как количество промежутков должно быть чётным.".format(count))

	x = numpy.linspace(begin, end, count + 1)
	step = x[1] - x[0]
	sum = Function(begin) + Function(end)
	for i in range(1, count):
		sum += Function(x[i]) * (i % 2 + 1) * 2

	return (step / 3) * sum

def Main():
	inputData = GetInputData()
	begin = inputData[0]
	end = inputData[1]
	intervalCount = inputData[2]

	if (intervalCount == 0):
		for i in [2 ** x for x in range(9)]:
			PrintResults(begin, end, i)
	else:
		PrintResults(begin, end, int(intervalCount))
	pass

def PrintResults(begin, end, n):
	print("\nn = ", n, ":", sep='')

	resSquarezoid = Squarezoid(begin, end, n)
	resTrapezoid = Trapezoid(begin, end, n)
	resSimpson = Simpson(begin, end, n)
	
	if (begin == 1.2 and end == 2):
		realValue = 0.281613
		PrintMethodResult("Mid-Point", resSquarezoid, realValue)
		PrintMethodResult("Trapezoid", resTrapezoid, realValue)
		PrintMethodResult("Simpson's", resSimpson, realValue)
	else:
		PrintMethodResult("Mid-Point", resSquarezoid)
		PrintMethodResult("Trapezoid", resTrapezoid)
		PrintMethodResult("Simpson's", resSimpson)
	pass

def PrintMethodResult(methodName, *args):
	precision = 6
	approx = round(args[0], precision)
	if (len(args) > 0):
		print("\t{0} method: {1}".format(methodName, approx), end='')
	if (len(args) == 2):
		real = round(args[1], precision)
		print("\tError= {0}".format(round(approx - real, precision)), end='')
	print()
	pass

Main()