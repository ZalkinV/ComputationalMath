import numpy as np
import matplotlib.pyplot as plt

helpLineWidth = 0.9

def Function(x):
	#return np.cos(x) - 6 * x + 1
	#return 2 * np.log(x + 1) - 1/x
	return (x - 1)**3 + 0.5 * np.e**x
	#return np.sqrt(x) - 1/(x + 1)**2
	#return 3**x + x
	#return x**2 + 4 * np.sin(x)
	#return x * np.log(x**2 - 1) - 1

def Derivative(x):
	#return -np.sin(x) - 6
	#
	return 3 * (x - 1)**2 + 0.5 * np.e**x 

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
				print("Нужно вводить действительные числа! Попробуйте ещё раз.")
				continue
		elif (bounds[0] == ''):
			begin = -2
			end = 2
		else:
			print("Промежуток должен быть задан двумя действительными числами")
			
		break
	return (begin, end)

def DrawMainGraph(begin, end, figure, precision=100):
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

def DrawTangentLine(figure, x0):
	plt.figure(figure)

	x1 = x0 - Function(x0)/Derivative(x0)
	plt.plot([x0, x0], [Function(x0), 0], 'r--', linewidth=helpLineWidth)
	plt.plot([x0, x1], [Function(x0), 0], 'r-', linewidth=helpLineWidth)

	return x1

def DrawSecantLine(figure, x0, x1):
	plt.figure(figure)

	x2 = x1 - Function(x1)/ApproxDerivative(x0, x1)
	plt.plot([x0, x0], [Function(x0), 0], 'r--', linewidth=helpLineWidth)
	plt.plot([x1, x1], [Function(x1), 0], 'r--', linewidth=helpLineWidth)
	plt.plot([x0, x1, x2], [Function(x0), Function(x1), 0], 'r-', linewidth=helpLineWidth)

	return x2

def Main():
	precision = 100
	bounds = GetInputData()
	print("Поиск корней на промежутке [{a}; {b}] ...".format(a=bounds[0], b=bounds[1]))
	
	DrawMainGraph(bounds[0], bounds[1], 1, precision)
	DrawTangentLine(1, bounds[0]+0.01)
	DrawSecantLine(1, bounds[0] + 0.01, bounds[0] + 1.5)
	plt.show()

Main()
