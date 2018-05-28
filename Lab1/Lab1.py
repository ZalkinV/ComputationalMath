import matplotlib.pyplot as plt
import numpy

def Function(x):
	return numpy.sin(0.227 * (x ** 3) - 0.04 * x)

def Lagranzh(x, xLagrList): #Возможно, для ускорения работы в цикле стоит один раз вызывать эту функция,
                            #чтобы она возращала список значений
	result = 0
	
	for iY in range(pointCount):
		addition = Function(xLagrList[iY])	
		for jX in range(pointCount):
			if (jX != iY):
				addition *= (x - xLagrList[jX]) / (xLagrList[iY] - xLagrList[jX])

		result += addition
	return result

def DrawMainGraph(xList, yFuncList, yLagrList, xLagrNodeList):
	plt.figure(1)
	plt.subplots_adjust(left=0.15)
	plt.xlabel("x", fontsize=14)
	plt.ylabel("f(x)", fontsize=14)
	plt.title("Интерполяция методом Лагранжа", fontsize=14)
	plt.plot(xList, yLagrList, 'b-', label='Полином Лагранжа')
	plt.plot(xList, yFuncList, 'g-', label='Исходная функция')
	plt.legend(loc='best')
	plt.grid(True)

	yLagrNodeList = [Lagranzh(x, xLagrNodeList) for x in xLagrNodeList]
	plt.plot(xLagrNodeList, yLagrNodeList, 'ok', markersize=5)
	#С оркруглениями ниже можно ещё поработать
	print("Координаты узлов интерполяционной сетки:\nx = {0}\ny = {1}".format(numpy.around(xLagrNodeList, 3), numpy.around(yLagrNodeList, 3)))
	pass

def DrawAccuracyGraph(xList, yDifList):
	plt.figure(2)
	plt.subplots_adjust(left=0.15)
	plt.xlabel("x", fontsize=14)
	plt.ylabel("f(x) - g(x)", fontsize=14)
	plt.title("Абсолютная погрешность интерполирования", fontsize=14)
	plt.plot(xList, yDifList, 'r-', label='Абсолютная погрешность')
	plt.grid(True)
	pass

def CalculateAccuracy(absoluteErrorList):
	difSum = 0
	for dif in absoluteErrorList:
		difSum += dif ** 2

	return (difSum / len(absoluteErrorList)) ** (0.5)
	

def Main():
	xList = numpy.linspace(xMin, xMax, precision)
	xLagrNodeList = numpy.linspace(xMin, xMax, pointCount)

	yFuncList = [Function(x) for x in xList]
	yLagrList = [Lagranzh(x, xLagrNodeList) for x in xList]
	DrawMainGraph(xList, yFuncList,  yLagrList, xLagrNodeList)

	yDifList = [yFuncList[i] - yLagrList[i] for i in range(len(xList))]
	DrawAccuracyGraph(xList, yDifList)
	print("Среднеквадратичная погрешность интерполяции (MSE) = {0}".format(round(CalculateAccuracy(yDifList),2)))

	plt.show()
	pass

#Плохой кусок кода ниже.  Может вообще проверку убрать?  А ещё переменные xMin
#и т.д.  видны за пределами цикла while (UPD: Просто она считается глобальной
while True: 
	try:
		xMin = float(input("Начало промежутка: "))
		xMax = float(input("Конец промежутка: "))
		pointCount = int(input("Количество интерполяционных узлов: "))
		break
	except (ValueError, TypeError):
		print("Нужно вводить числа! Попробуйте ещё раз.\n")
precision = 250 #Количество значений x на промежутке [a,b].  Чем больше, тем плавнее график
#
Main()
