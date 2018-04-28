import numpy as np
import matplotlib.pyplot as plt

helpLineWidth = 0.9
maxMethodIterations = 15

def Function(x):
	#return np.cos(x) - 6 * x + 1
	#return 2 * np.log(x + 1) - 1/x
	#return (x - 1) ** 3 + 0.5 * np.e ** x
	#return np.sqrt(x) - 1/(x + 1)**2
	#return 3**x + x
	#return x**2 + 4 * np.sin(x)
	#return x * np.log(x**2 - 1) - 1
	return np.exp(-x**2) * np.cos(4*x)

def Derivative(x):
	#return -np.sin(x) - 6
	#
	#return 3 * (x - 1) ** 2 + 0.5 * np.e ** x
	#
	#
	#
	#
	return (np.exp(-x**2) * -2 * x) * (-np.sin(4 * x) * 4)

def ApproxDerivative(x0, x1):
	return (Function(x1) - Function(x0)) / (x1 - x0)

def GetInputData():
	while True:
		bounds = input("Введите начало промежутка и конец промежутка через пробел: ").split(' ')
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
	return (begin, end)

def DrawMainGraph(begin, end, figure, precision = 100):
	plt.figure(figure)
	
	xList = np.linspace(begin, end, 100)
	yList = [Function(x) for x in xList]
	plt.plot(xList, yList, 'b-')
	plt.plot((xList[0], xList[-1]), (0,0), 'k--')

	plt.xlabel("x", fontsize=14)
	plt.ylabel("f(x)", fontsize=14)
	plt.title("f(x) = cos(x) - 6*x + 1", fontsize=14)
	plt.grid(True)

	plt.axis((xList[0], xList[-1], min(yList), max(yList)))
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
	xCurrent = x0 #Чтобы не было ошибки, если цикл ни разу не запуститься
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
	n = int((b - a) / error)
	xList = np.linspace(a, b, n + 1)
	yList = Function(xList)
	roots = []

	for i in range(n - 1):
		if (yList[i] * yList[i + 1] < 0):
			roots.append(xList[i] - ApproxDerivative(xList[i], xList[i + 1]) * yList[i])

	return roots

def PrintResult(x, error):
	if (isinstance(x, list)):
		for currentRoot in x:
			print("\tx = {root} +- {approx}".format(root=round(currentRoot, GetCalcPrecision(error)), approx=error))
	else:
		print("\tx = {root} +- {approx}\n".format(root=round(x, GetCalcPrecision(error)), approx=error))
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
	error = 0.001
	bounds = GetInputData()
	print("Поиск корней на промежутке [{a}; {b}] ...".format(a=bounds[0], b=bounds[1]))
	
	DrawMainGraph(bounds[0], bounds[1], 1, precision)
	
	print("\nРезультаты вычислений:")

	print("Метод Касательных (Ньютона)")
	rootTan = MethodTangent(bounds[0] + 0.01, error, 1)
	plt.plot(rootTan, Function(rootTan), 'or', label = "Метод касательных")
	PrintResult(rootTan, error)
	
	print("Метод Секущих:")
	rootSec = MethodSecant(bounds[0] + 0.01, bounds[0] + 1.5, error, 1)
	plt.plot(rootSec, Function(rootSec), 'og', label = "Метод секущих")
	PrintResult(rootSec, error)
	
	try:
		print("Метод Биссекции:")
		rootBis = MethodBisection(bounds[0], bounds[1], error)
		plt.plot(rootBis, Function(rootBis), 'vm', label = "Метод бисекции")
		PrintResult(rootBis, error)
	except RuntimeError:
		print("Значения функции на концах отрезка одного знака. Биссекция невозможна.")

	print("Метод Грубой силы:")
	rootsBF = MethodBruteForce(bounds[0], bounds[1], error)
	plt.plot(rootsBF, [Function(x) for x in rootsBF], '^c', label = "Метод грубой силы")
	PrintResult(rootsBF, error)
	
	plt.legend(loc='best')
	plt.show()

	pass

Main()