import pandas as pd
import numpy as np
import time
import os, csv
from nsepython import *
from datetime import date
from dateutil.relativedelta import relativedelta
from bfxhfindicators import Stochastic


entryTargets = []
params = {
    'access_key': 'fce4047d20b3b06c7393ed8093e0574d'
}



def isDoji(out):
    wicks = abs(out[1] - out[2])
    body = abs(out[0] - out[3])
    percentage = 100 / (wicks/body)
    if (percentage <= 33):
        return out


def stochastic(candles):
    stochValues = []
    iStoch = Stochastic(5, 3, 3)
    for candle in candles:
        iStoch.add(candle)
        stochValues.append(iStoch.v())
    return (stochValues)


def HEIKIN(O, H, L, C, oldO, oldC):
    HA_Open = (oldO + oldC)/2
    HA_Close = (O + H + L + C)/4
    elements = np.array([H, L, HA_Open, HA_Close])
    HA_High = elements.max(0)
    HA_Low = elements.min(0)
    out = [HA_Open, HA_High, HA_Low, HA_Close]
    return out


def maxMin(fiboRange):
    rangeMax = max(max(x) if isinstance(x, list) else x for x in fiboRange)
    rangeMin = min(min(x) if isinstance(x, list) else x for x in fiboRange)
    return (rangeMax, rangeMin)


def fibonacciDown(price_max, price_min):
    tempList = []

    diff = price_max - price_min
    level0 = price_max
    level1 = price_max - 0.236 * diff
    level2 = price_max - 0.382 * diff
    level3 = price_max - 0.50 * diff
    level4 = price_max - 0.618 * diff
    level5 = price_max - 0.786 * diff

    tempList = [level1, level2, level3, level4, level5, level0]
    entryTargets.append(tempList)

    return entryTargets


def fibonacciUp(price_max, price_min):
    tempList = []

    diff = price_max - price_min
    level0 = price_max - 1.0 * diff
    level1 = price_max - 0.786 * diff
    level2 = price_max - 0.618 * diff
    level3 = price_max - 0.50 * diff
    level4 = price_max - 0.366 * diff
    level5 = price_max - 0.236 * diff

    tempList = [level1, level2, level3, level4, level5, level0]
    entryTargets.append(tempList)

    return entryTargets


def main():
    # start = time.time()
    while(True):
        os.system(['clear', 'cls'][os.name == 'nt'])
        j = 0
        openPrice = []
        highPrice = []
        lowPrice = []
        closePrice = []
        hikenCandle = []
        doji = []
        swing = []
        dateTime = []
        allCall = []
        dates = []

        print("---------------------------------")
        print("|\tSTOCK MARKET ANALYSIS\t|")
        print("---------------------------------")
        print()
        try:
            df = pd.read_csv('tcs.csv')  # YAHA PE DOWNLOADED CSV FILE (DATA FILE) KA NAAM

            for data in df.index[::-1]:
                openPrice.append(df['Open Price'][data])
                highPrice.append(df['High Price'][data])
                lowPrice.append(df['Low Price'][data])
                closePrice.append(df['Close Price'][data])
                dates.append(df['Date'][data])
            
            n = len(openPrice) - 2

            candle = HEIKIN(openPrice[n], highPrice[n],
                            lowPrice[n], closePrice[n], openPrice[n+1],
                            closePrice[n+1])

            hikenCandle.append(candle)

            for i in range(n-1, -1, -1):
                candle = HEIKIN(openPrice[i], highPrice[i], lowPrice[i],
                                closePrice[i], hikenCandle[j][0], hikenCandle[j][3])

                hikenCandle.append(candle)
                dateTime.append(dates[i])
                j += 1

            stochasticHiken = stochastic(hikenCandle)
            del stochasticHiken[:4]


            for i in hikenCandle:
                doji.append(isDoji(i))

            del doji[:4]
            del dateTime[:3]

            for i in range(1, len(stochasticHiken)):
                if ((stochasticHiken[i]['k'] < stochasticHiken[i]['d']) and stochasticHiken[i-1]['k'] > stochasticHiken[i-1]['d']) or ((stochasticHiken[i]['k'] > stochasticHiken[i]['d']) and stochasticHiken[i-1]['k'] < stochasticHiken[i-1]['d']):
                    swing.append(i)
            for i in range(len(stochasticHiken)):
                if (stochasticHiken[i]['k'] < stochasticHiken[i]['d'] and stochasticHiken[i-1]['k'] > stochasticHiken[i-1]['d']):
                    try:
                        if doji[i]:
                            if i != 0:
                                swingIndex = swing.index(i)
                                if swingIndex != 0:
                                    temp = maxMin(
                                        hikenCandle[swing[swingIndex-1] + 4: swing[swingIndex] + 4])
                                    testList = fibonacciDown(
                                        temp[0], temp[1])
                                    lastCandle = i
                                    allCall.append(dateTime[i])
                        elif doji[i-1] or doji[i+1] or doji[i+2]:
                            if i != 0:
                                swingIndex = swing.index(i)
                                if swingIndex != 0:
                                    temp = maxMin(
                                        hikenCandle[swing[swingIndex-1] + 4: swing[swingIndex] + 4])
                                    testList = fibonacciDown(
                                        temp[0], temp[1])
                                    lastCandle = i
                                    allCall.append(dateTime[i])
                    except (IndexError):
                        pass
                elif (stochasticHiken[i]['k'] > stochasticHiken[i]['d'] and stochasticHiken[i-1]['k'] < stochasticHiken[i-1]['d']):
                    try:
                        if doji[i]:
                            if i != 0:
                                swingIndex = swing.index(i)
                                if swingIndex > 0:
                                    temp = maxMin(
                                        hikenCandle[swing[swingIndex-1] + 4: swing[swingIndex] + 4])
                                    testList = fibonacciUp(
                                        temp[0], temp[1])
                                    lastCandle = i
                                    allCall.append(dateTime[i])
                        elif doji[i-1] or doji[i+1] or doji[i+2]:
                            if i != 0:
                                swingIndex = swing.index(i)
                                if swingIndex > 0:
                                    temp = maxMin(
                                        hikenCandle[swing[swingIndex-1] + 4: swing[swingIndex] + 4])
                                    testList = fibonacciUp(
                                        temp[0], temp[1])
                                    lastCandle = i
                                    allCall.append(dateTime[i])
                    except (IndexError):
                        pass

            os.system(['clear', 'cls'][os.name == 'nt'])
            with open(df['Symbol'][0]+"_REPORT.csv", 'w', newline='') as f:
                fieldnames = ['Symbol', 'Date', 'Call','Stop_Loss', 'Target_1', 'Target_2', 'Target_3', 'Target_4', 'Trend']

                thewriter = csv.DictWriter(f, fieldnames=fieldnames)
                thewriter.writeheader()
            for i in range(len(testList)):
                with open(df['Symbol'][0]+"_REPORT.csv", 'a+', newline='') as f:
                    fieldnames = ['Symbol', 'Date', 'Call',
                                'Stop_Loss', 'Target_1', 'Target_2', 'Target_3', 'Target_4', 'Trend']

                    thewriter = csv.DictWriter(f, fieldnames=fieldnames)
                    if testList[i][0] > testList[i][5]:
                        trend = "BUY"
                    else:
                        trend = "SELL"

                    thewriter.writerow(
                        {'Symbol': df['Symbol'][0], 'Date': allCall[i],
                            'Call': round(testList[i][0],2), 'Stop_Loss': round(testList[i][5],2), 'Target_1': round(testList[i][1],2),
                            'Target_2': round(testList[i][2],2), 'Target_3': round(testList[i][3],2), 'Target_4': round(testList[i][4],2),
                            'Trend': trend,
                        })
                print("-----------------------------------------")
                print("|\t", df['Symbol'][0], "- DATE:", allCall[i], "\t|")
                print("-----------------------------------------")

                if (testList[i][0] > testList[-1][5]):
                    print("| Buy Above\t|\t", round(testList[i][0], 2), "\t|")
                else:
                    print("| Sell Below\t|\t", round(
                        testList[i][0], 2), "\t|")

                print("| Stop Loss\t|\t", round(testList[i][5], 2), "\t|")
                print("| Target-1 \t|\t", round(testList[i][1], 2), "\t|")
                print("| Target-2 \t|\t", round(testList[i][2], 2), "\t|")
                print("| Target-3 \t|\t", round(testList[i][3], 2), "\t|")
                print("| Target-4 \t|\t", round(testList[i][4], 2), "\t|")
            print("-----------------------------------------")

            print()
            input("Press enter to exit... ")
            exit()

        except (KeyError):
            keyerror = True

        # end = time.time()
        # print(f"Runtime of the program is {end - start}")


main()
