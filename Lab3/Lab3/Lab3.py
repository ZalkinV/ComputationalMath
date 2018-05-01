import numpy as np
import matplotlib.pyplot as plt

helpLineWidth = 0.9
maxMethodIterations = 15

def Function(x):
	return np.cos(x) - 6 * x + 1
	#return (x - 1) ** 3 + 0.5 * np.e ** x
	#return 3**x + x
	#return x**2 + 4 * np.sin(x)
	#return np.exp(-x ** 2) * np.cos(4 * x)

def Derivative(x):
	return -np.sin(x) - 6
	#return 3 * (x - 1) ** 2 + 0.5 * np.e ** x
	#return 3**x * np.log(3) + 1
	#return 2 * x + 4 * np.cos(x)
	#return (np.exp(-x ** 2) * -2 * x * np.cos(4 * x)) + (np.exp(-x ** 2) * -np.sin(4 * x) * 4)

def ApproxDerivative(x0, x1):
	return (Function(x1) - Function(x0)) / (x1 - x0)

def GetInputData():
	while True:
		bounds = input("Введите через пробел начало и конец промежутка: ").split(' ')
		if (len(bounds) == 2):
			try:
				begin = float(bounds[0])
				end = float(bounds[1])
			except (ValueError):
				print("Нужно вводить действительные числа! Попробуйте ещё раз.\n")
				continue
		elif (bounds[0] == ''):
			begin = -2
			end = 2
		else:
			print("Промежуток должен быть задан двумя действительными числами!\n")
			continue
		break

	while True:
		errorString = input("Введите желаемую точность вычислений в виде десятичной дроби: ")
		if (len(errorString) != 0):
			try:
				error = float(errorString)
			except (ValueError):
				print("Нужно вводить десятичные дроби! Попробуйте ещё раз.\n")
				continue
		else:
			error = 0.01
		break

	return (begin, end, error)

def DrawMainGraph(begin, end, figure, precision = 100):
	plt.figure(figure)
	
	xList = np.linspace(begin, end, precision)
	yList = [Function(x) for x in xList]
	plt.plot(xList, yList, 'b-')
	plt.plot((xList[0], xList[-1]), (0,0), 'k--')

	plt.xlabel("x", fontsize=14)
	plt.ylabel("f(x)", fontsize=14)
	plt.title("f(x) = cos(x) - 6*x + 1", fontsize=14)
	plt.grid(True)

	plt.axis([min(xList), max(xList), min(yList), max(yList)])
	pass

def DrawSecantLine(x0, x1, figure = -1):
	try:
		x2 = x1 - Function(x1) / ApproxDerivative(x0, x1)
	
		if (figure != -1):
			plt.figure(figure)
			plt.plot([x0, x0], [Function(x0), 0], 'g--', linewidth=helpLineWidth)
			plt.plot([x1, x1], [Function(x1), 0], 'g--', linewidth=helpLineWidth)
			plt.plot([x0, x1, x2], [Function(x0), Function(x1), 0], 'g-', linewidth=helpLineWidth)
	except ZeroDivisionError:
		print("Производная в точке {x} равна 0. Досрочно прекращаю вычисления.".format(x=x0))
		raise ZeroDivisionError

	return x2

def MethodSecant(x0, x1, error, figure = -1):
	xPrevious = x0
	xCurrent = x1
	yNext = Function(x1)
	i = 0
	
	try:
		while (abs(yNext) >= error and i < maxMethodIterations):
			xNext = DrawSecantLine(xPrevious, xCurrent, figure)
			yNext = Function(xNext)
			xPrevious = xCurrent
			xCurrent = xNext
			i += 1
	except ZeroDivisionError:
		pass

	return xCurrent

def DrawTangentLine(x0, figure = -1):
	try:
		x1 = x0 - Function(x0) / Derivative(x0)
		
		if (figure != -1):
			plt.figure(figure)
			plt.plot([x0, x0], [Function(x0), 0], 'r--', linewidth=helpLineWidth)
			plt.plot([x0, x1], [Function(x0), 0], 'r-', linewidth=helpLineWidth)
	except ZeroDivisionError:
		print("Производная в точке {x} равна 0. Досрочно прекращаю вычисления.".format(x=x0))
		raise ZeroDivisionError

	return x1

def MethodTangent(x0, error, figure = -1):
	xCurrent = x0
	yCurrent = Function(x0)
	i = 0
	
	try:
		while (abs(yCurrent) >= error and i < maxMethodIterations):
			xCurrent = DrawTangentLine(xCurrent, figure)
			yCurrent = Function(xCurrent)
			i += 1
	except ZeroDivisionError:
		pass

	return xCurrent

def MethodBisection(a, b, error):
	if (Function(a) * Function(b) > 0):
		raise RuntimeError

	i = 0
	while (abs(Function((a + b) / 2)) > error and i < maxMethodIterations):
		x = (a + b) / 2
		a, b = (a, x) if Function(a) * Function(x) < 0 else (x, b)
		i += 1
	return (a + b) / 2

def MethodBruteForce(a, b, error):
	n = int((b - a) / error) * 10 #Надо придумать, как вычислять n, зная погрешность для y - error
	xList = np.linspace(a, b, n + 1)
	roots = []

	for i in range(n - 1):
		if (Function(xList[i]) * Function(xList[i + 1]) < 0):
			roots.append(xList[i] - ApproxDerivative(xList[i], xList[i + 1]) * Function(xList[i]))

	return roots

def PrintResult(x, error):
	if (isinstance(x, list)):
		for currentRoot in x:
			print("\tx = {root} +- {approx}".format(root=round(currentRoot, GetCalcPrecision(error)), approx=error))
	else:
		print("\tx = {root} +- {approx}".format(root=round(x, GetCalcPrecision(error)), approx=error))
	pass

def GetCalcPrecision(error):
	precisionCalc = 1
	digitalNumber = 0

	while (error % precisionCalc >= error and digitalNumber < 15):
		digitalNumber += 1
		precisionCalc /= 10

	return digitalNumber

def Main():
	precision = 100

	data = GetInputData()
	bounds = data[0:2]
	error = data[2]
	print("Поиск корней на промежутке [{a}; {b}] с точностью {e} ...".format(a=bounds[0], b=bounds[1], e=error))
	
	DrawMainGraph(bounds[0], bounds[1], 1, precision)
	
	print("\nРезультаты вычислений:")
	#BAD: Ниже две очень плохие строки, которые нужно будет заменить
	offsetA = abs(bounds[0] / 10) 
	offsetB = offsetA * 2 + 0.1

	print("\nМетод Касательных (Ньютона)")
	rootTan = MethodTangent(bounds[0] + offsetA, error, 1)
	plt.plot(rootTan, Function(rootTan), 'or', label = "Метод касательных")
	if (bounds[0] <= rootTan and rootTan <= bounds[1]):
		PrintResult(rootTan, error)
	else:
		print("Не получилось найти корни на введённом интервале.")
	
	print("\nМетод Секущих:")
	rootSec = MethodSecant(bounds[0] + offsetA, bounds[0] + offsetB, error, 1)
	plt.plot(rootSec, Function(rootSec), 'og', label = "Метод секущих")
	if (bounds[0] <= rootSec and rootSec <= bounds[1]):
		PrintResult(rootSec, error)
	else:
		print("Не получилось найти корни на введённом интервале.")
	
	try:
		print("\nМетод Бисекции:")
		rootBis = MethodBisection(bounds[0], bounds[1], error)
		plt.plot(rootBis, Function(rootBis), 'vm', label = "Метод бисекции")
		PrintResult(rootBis, error)
	except RuntimeError:
		print("Значения функции на концах отрезка одного знака. Бисекция невозможна.")

	#BAD: Есть проблема в том, что нам даётся погрешность для значений y, а в
	#методе грубой силы, погрешность для y используется для количества
	#промежутков, то есть для погрешности x.  Надо везде использовать одинаковую
	#погрешность
	print("\nМетод Грубой силы:")
	rootsBF = MethodBruteForce(bounds[0], bounds[1], error)
	plt.plot(rootsBF, [Function(x) for x in rootsBF], '^c', label = "Метод грубой силы")
	PrintResult(rootsBF, error)
	
	plt.legend(loc='best')
	plt.show()

	pass

Main()