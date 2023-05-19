import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def EMA(data,day,N):
        alfa = 2/(N+1)
        numerator = 0
        denumerator = 0
        for i in range(N):
            numerator += ((1-alfa)**(day - i))*data[day - i]
            denumerator += (1-alfa)**(day - i)
        resultEMA = numerator/denumerator
        return resultEMA

def MACD(priceArray, day):
    EMA12 = EMA(priceArray, day, 12)
    EMA26 = EMA(priceArray, day, 26)
    MACD = EMA12 - EMA26
    return MACD


df = pd.read_csv("C:/Users/filip/Desktop/2357AsusHisData.csv")
priceArray = df["Price"]
priceArray = reversed(priceArray)
priceArray = list(priceArray)


listMACD = []
listSignal = []
listRSI = []

dateList = df["Date"]
dateList = reversed(dateList)
dateList = list(dateList)
interval = 182 #wyswietlanie daty na osi co pol roku
xTicks = np.arange(0, len(dateList), interval)
xLabels = [dateList[i] for i in xTicks]


for i in range(1000):

    if i >= 26:
        listMACD.append(MACD(priceArray, i))
    if i >= 34:
        listSignal.append(EMA(listMACD, i - 26, 9))

#SIMULATION
money = 1000
stock = 0
transakcje = 0
print("Kapitał początkowy: ")
print(money)



for i in range(len(listSignal) - 1):

    x = np.arange(len(priceArray))
    coefficients = np.polyfit(x, priceArray, 1)  # metoda najmniejszych kwadratów
    polynomial = np.poly1d(coefficients)
    ys = polynomial(x)
    if (listMACD[i] > listSignal[i] and stock == 0) or (listMACD[i] < ys[i] and stock == 0): #kupowanie akcji
        stock = int(money/priceArray[i])
        money -= stock*priceArray[i]
        transakcje += 1
    elif (listMACD[i] > listSignal[i] and stock > 0) or (listMACD[i] > ys[i] and stock > 0): #sprzedaż akcji
        money += stock*priceArray[i]
        transakcje += 1
        stock = 0



print("Kapitał końcowy: ")
print(money)
print("Transakcje: ")
print(transakcje)
plt.title("Wykres MACD i Signal (ASUS)")
plt.plot(ys, label="Trend", color='y')
plt.plot(priceArray, label="Cena", color='g')
plt.plot(listMACD, label="MACD", color='b')
plt.plot(listSignal, label="SIGNAL", color='r')
plt.legend()
plt.xticks(ticks=xTicks, labels=xLabels, rotation=45)
plt.xlabel("Data [mm/dd/yyyy]")
plt.ylabel("Wartość")
plt.show()









