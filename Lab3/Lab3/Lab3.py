import numpy as np
import matplotlib.pyplot as plt

helpLineWidth = 0.9

def Function(x):
	#return np.cos(x) - 6 * x + 1
	#return 2 * np.log(x + 1) - 1/x
	return (x - 1) ** 3 + 0.5 * np.e ** x
	#return np.sqrt(x) - 1/(x + 1)**2
	#return 3**x + x
	#return x**2 + 4 * np.sin(x)
	#return x * np.log(x**2 - 1) - 1
def Derivative(x):
	#return -np.sin(x) - 6
	#
	return 3 * (x - 1) ** 2 + 0.5 * np.e ** x 

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

	yMin = min(Function(xList[0]), Function(xList[-1]))
	yMax = max(Function(xList[0]), Function(xList[-1]))
	plt.axis((xList[0], xList[-1], yMin, yMax))
	pass

def DrawSecantLine(x0, x1, figure = -1):
	#TODO: Надо добавить проверку деления на ноль. Можно в этом случае просто сдвигать точки и сообщать (или нет) об этом пользователю
	x2 = x1 - Function(x1) / ApproxDerivative(x0, x1)

	if (figure != -1):
		plt.figure(figure)
		plt.plot([x0, x0], [Function(x0), 0], 'g--', linewidth=helpLineWidth)
		plt.plot([x1, x1], [Function(x1), 0], 'g--', linewidth=helpLineWidth)
		plt.plot([x0, x1, x2], [Function(x0), Function(x1), 0], 'g-', linewidth=helpLineWidth)

	return x2

def MethodSecant(x0, x1, error, figure = -1):
	xPrevious = x0
	xCurrent = x1
	yNext = Function(x1)
	i = 0

	while (abs(yNext) > error and i < 100):
		xNext = DrawSecantLine(xPrevious, xCurrent, figure)
		yNext = Function(xNext)
		xPrevious = xCurrent
		xCurrent = xNext
		i += 1
	return xCurrent

def DrawTangentLine(x0, figure = -1):
		#TODO: Надо добавить проверку деления на ноль. Можно в этом случае просто сдвигать точки и сообщать (или нет) об этом пользователю
	x1 = x0 - Function(x0) / Derivative(x0)

	if (figure != -1):
		plt.figure(figure)
		plt.plot([x0, x0], [Function(x0), 0], 'r--', linewidth=helpLineWidth)
		plt.plot([x0, x1], [Function(x0), 0], 'r-', linewidth=helpLineWidth)

	return x1

def MethodTangent(x0, error, figure = -1):
	xCurrent = x0 #Чтобы не было ошибки, если цикл ни разу не запуститься
	yCurrent = Function(x0)
	i = 0
	
	while (abs(yCurrent) > error and i < 100):
		xCurrent = DrawTangentLine(xCurrent, figure)
		yCurrent = Function(xCurrent)
		i += 1
	return xCurrent

def GetCalcPrecision(error):
	precisionCalc = 100
	digitNumber = -2
	while (error % precisionCalc >= error):
		digitNumber += 1
		precisionCalc /= 10
	return digitNumber


def Main():
	precision = 100
	error = 0.05
	bounds = GetInputData()
	print("Поиск корней на промежутке [{a}; {b}] ...".format(a=bounds[0], b=bounds[1]))
	
	DrawMainGraph(bounds[0], bounds[1], 1, precision)
	rootTan = MethodTangent(bounds[0] + 0.01, error, 1)
	rootSec = MethodSecant(bounds[0] + 0.01, bounds[0] + 1.5, error, 1)
	
	plt.plot(rootTan, Function(rootTan), 'or')
	plt.plot(rootSec, Function(rootSec), 'og')
	plt.show()

	print("Метод Ньютона(касательных): ", round(rootTan, GetCalcPrecision(error)))
	print("Метод Секущих: ", round(rootSec, GetCalcPrecision(error)))
	pass

Main()