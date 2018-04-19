import numpy as np
import matplotlib.pyplot as plt

def Function(x):
	return np.cos(x) - 6 * x + 1
	#return 2 * np.log(x + 1) - 1/x
	#return (x - 1)**3 + 0.5 * np.e**x
	#return np.sqrt(x) - 1/(x + 1)**2
	#return 3**x + x
	#return x**2 + 4 * np.sin(x)
	#return x * np.log(x**2 - 1) - 1

def Derivative(x):
	return -np.sin(x) - 6

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

def DrawMainGraph(begin, end, function, precision=100):
	plt.figure(1)
	
	xList = np.linspace(begin, end, 100)
	yList = [function(x) for x in xList]
	plt.plot(xList, yList, 'b-')
	plt.plot((xList[0], xList[-1]), (0,0), 'k--')

	plt.xlabel("x", fontsize=14)
	plt.ylabel("f(x)", fontsize=14)
	plt.title("f(x) = cos(x) - 6*x + 1", fontsize=14)
	plt.grid(True)

	yMin = min(function(xList[0]), function(xList[-1]))
	yMax = max(function(xList[0]), function(xList[-1]))
	plt.axis((xList[0], xList[-1], yMin, yMax))
	
	plt.show()

def Main():
	precision = 100
	bounds = GetInputData()
	print("Поиск корней на промежутке [{a}; {b}] ...".format(a=bounds[0], b=bounds[1]))
	
	DrawMainGraph(bounds[0], bounds[1], Function)

Main()
