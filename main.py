
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import glob
import os
import math
import matplotlib.pyplot as plt
from trade_manager import profitCalculator


# IMPORT LIST OF TRADING DAYS
dateList = pd.read_csv('Trading Dates1.csv')

# THIS PATH IMPORTS ALL THE STOCK DATA OF THAT TIME FRAME INSIDE THE FOLDER
fifteen_min_path = '15_MIN_DATA/'
daily_path = 'DAILY_DATA/'
five_min_path = '5_MIN_DATA/'

# SORT FILES IN ALPHABETICAL ORDER
files15min = sorted(filter(os.path.isfile, glob.glob(fifteen_min_path + '/*.csv')))
filesDaily = sorted(filter(os.path.isfile, glob.glob(daily_path + '/*.csv')))
files5min = sorted(filter(os.path.isfile, glob.glob(five_min_path + '/*.csv')))
fifteen_min_data_list = []
stocklist = []
daily_data_list = []
five_min_data_list = []

# STORING ALL THE FILES AS A LIST OF DATAFRAMES, EACH DATAFRAME HAS A STOCKS DATA
for filename in files15min:
    tempdf = pd.read_csv(filename)
    fifteen_min_data_list.append(tempdf)

for filename in filesDaily:
    tempdf = pd.read_csv(filename)
    stockName = os.path.basename(filename).split(".")
    stocklist.append(stockName[0])
    daily_data_list.append(tempdf)

for filename in files5min:
    tempdf = pd.read_csv(filename)
    five_min_data_list.append(tempdf)

# ADD INDICATOR VALUES AS A COLUMN TO YOUR DATAFRAME
period = 20
multiplier = 2
for dataframes in fifteen_min_data_list:
    sma = dataframes['Close'].rolling(20).mean()
    stdDev = dataframes['Close'].rolling(20).std()
    dataframes['UpperBB'] = sma + multiplier*stdDev
    dataframes['LowerBB'] = sma - multiplier*stdDev

shouldLoop = True
# RUN THE LOOP UNTIL USER INTERRUPTS
while shouldLoop:
    # INITIALIZE ALL THE VARIABLES
    balance = 500000
    maxAccountValue = 0
    rpt = balance*(0.2/100)
    tradeWiseAccuracy = 0
    drawDownStartDate = ""
    drawDownEndtDate = ""
    ddStartTradeNo = 0
    ddEndTradeN0 = 0
    tempStartDate = ""
    tempDDTradeNo = 0
    # print("RPT: ",rpt)
    maxDrawDown = 0
    tradesExceedingfive = 0
    maxNumberOfTrades = 0
    netProfit = balance
    totalTrades = 0
    tradingDays = 0
    marginReq = 0
    candlesOutsideBB = 2
    momentumProfit = 0
    prevDClose = 1.0
    prevDOpen = 1.0
    prevDLow = 1.0
    prevDHigh = 1.0
    changePercentProfit = 0
    numberOfChangePercent = 0
    numberOfProfitableChangePercent = 0
    notChangePercentProfit = 0
    numberOfNotChangePercent = 0
    numberOfProfitableNotChangePercent = 0
    dayWiseAccuracy = 0
    x_axis = []
    y_axis =[]
    totalTradesAboveRange = 0
    totalTradesUnderRange = 0

    # FOR DATE RANGE
    fromDate = input("Enter from date in DD/MM/YY: ")
    toDate = input("Enter to date in DD/MM/YY: ")
    splitDate = fromDate.split("/")
    actualFromDate = "20" + splitDate[2] + "-" + splitDate[1] + "-" + splitDate[0]
    splitDate = toDate.split("/")
    actualToDate = "20" + splitDate[2] + "-" + splitDate[1] + "-" + splitDate[0]
    fromIndex = dateList.loc[dateList['Date'] == actualFromDate].index.values.astype(int)[0]
    toIndex = dateList.loc[dateList['Date'] == actualToDate].index.values.astype(int)[0] + 1

    # EXTRACTING TRADING DATES BETWEEN FROM DATE AND TWO DATE
    tempDatesDf = dateList[fromIndex:toIndex]

    # LOOPING THROUGH ALL DATES IN THIS DATE RANGE
    for actualDate in tempDatesDf['Date']:
        tradingDays+=1
        print(actualDate)
        # DECLARING A DICTIONARY TO STORE ALL THE TRADE INFORMATION FOR THAT DAY

        finalDict = {"Stock Name": [],"Bollinger Level":[],"P/L":[],"Entry":[],"Exit":[],"StopLoss":[],"Qty":[],"Time":[],"Margin":[],"Accuracy":[],"Trend":[]}

        # ITERATING THROUGH EACH RECORD TO CHECK IF THE STOCK IS ELIGIBLE FOR TRADE
        index=0
        for fifteen_min_df,stockNames,daily_data in zip(fifteen_min_data_list,stocklist,daily_data_list):
                # FINDING THE RECORDS IN 15 MIN TIME FRAME THAT HAVE MATCH THE CURRENT DATE
                fifteenMinIndex = fifteen_min_df.loc[fifteen_min_df['Date'] == actualDate].index.values
                if (fifteenMinIndex.size != 0):
                    temp15mindf = fifteen_min_df.loc[fifteen_min_df['Date'] == actualDate]


                # IN THIS PART OF THE CODE WRITE CONDITIONS THAT NEED TO BE True
                # FOR THE STOCK TO BE ELIGIBLE TO TRADE LONG POSITION
                condition_long_1 = True
                condition_long_2 = True

                # ADD MORE CONDITIONS ACCORDING TO STRATEGY

                # CONDITION FOR SHORT TRADES
                condition_short_1 = False
                condition_short_2 = False
                if(condition_long_1 and condition_long_2):
                    # AS SOON AS THE CONDITION IS MET BREAK THE DATAFRAME AND PASS THE REMAINING DATAFRAME TO CALCULATE
                    # TRADE ENTRY/EXIT AND PROFIT/LOSS

                    breakDf = temp15mindf.iloc[index:, :]

                    profit, entry, stoploss, qty, levelBreached, entryTime, margin, exit, range = profitCalculator(breakDf, "Long", rpt)
                    #REMOVING OUTLIERS
                    if(profit > 10*rpt):
                        profit = 0
                    # ADD ALL THE TRADE INFORMATION TO THE DICTIONARY
                    finalDict['Stock Name'].append(stockNames)
                    finalDict['Bollinger Level'].append("Upper")
                    finalDict['P/L'].append(profit)
                    finalDict['Entry'].append(entry)
                    finalDict['StopLoss'].append(stoploss)
                    finalDict['Qty'].append(qty)
                    finalDict['Time'].append(entryTime)
                    finalDict['Margin'].append(margin)
                    finalDict['Exit'].append(exit)
                    finalDict['Trend'].append("Trending")
                    if (profit > 0):
                        finalDict['Accuracy'].append(1)
                    else:
                        finalDict['Accuracy'].append(0)
                    # break
                elif(condition_short_1 and condition_short_2):

                    breakDf = temp15mindf.iloc[index:, :]

                    profit, entry, stoploss, qty, levelBreached, entryTime, margin, exit, range = profitCalculator(
                        breakDf, "Short", rpt)
                    # REMOVING OUTLIERS
                    if (profit > 10 * rpt):
                        profit = 0

                    finalDict['Stock Name'].append(stockNames)
                    finalDict['Bollinger Level'].append("Lower")
                    finalDict['P/L'].append(profit)
                    finalDict['Entry'].append(entry)
                    finalDict['StopLoss'].append(stoploss)
                    finalDict['Qty'].append(qty)
                    finalDict['Time'].append(entryTime)
                    finalDict['Margin'].append(margin)
                    finalDict['Exit'].append(exit)
                    finalDict['Trend'].append("Trending")
                    if (profit > 0):
                        finalDict['Accuracy'].append(1)
                    else:
                        finalDict['Accuracy'].append(0)

                    # print(breakDf)

                    # break

        index+=1
        finalDf = pd.DataFrame.from_dict(finalDict)
        finalResult = finalDf.sort_values('Time')
        finalResult = finalResult.head(5)
        print(finalResult.to_string())
        totalProfit = finalResult['P/L'].sum()
        marginReq = finalResult['Margin'].sum()
        tradeWiseAccuracy += finalResult['Accuracy'].sum()
        if(totalProfit > 0):
            dayWiseAccuracy+=1
        # if(marginReq>400000):
        # print(finalResult.to_string())
        print("Margin Required: ",marginReq)
        print("Total Profit ",totalProfit)
        print("RPT: ",rpt)
        netProfit+=totalProfit
        totalTrades += len(finalResult.index)
        if (len(finalResult.index) > 5):
            tradesExceedingfive += 1

        if(len(finalResult.index) > maxNumberOfTrades):
            maxNumberOfTrades = len(finalResult.index)
        if(netProfit >= maxAccountValue):
            maxAccountValue = netProfit
            # RPT CHANGING CODE
            rpt = maxAccountValue*(0.2/100)
            tempStartDate = actualDate
            tempDDTradeNo = totalTrades
        if(netProfit < maxAccountValue):
            drawDown = ((maxAccountValue - netProfit)/maxAccountValue)*100
            if(drawDown > maxDrawDown):
                maxDrawDown = drawDown
                drawDownStartDate = tempStartDate
                ddStartTradeNo = tempDDTradeNo
                drawDownEndtDate = actualDate
                ddEndTradeN0 = totalTrades

        x_axis.append(totalTrades)
        y_axis.append(netProfit)
    print("Net Profit: ",netProfit)
    print("Total Trades: ",totalTrades)
    print("Trading Days",tradingDays)
    print("Max DrawDown: ", maxDrawDown,"%")
    print("DrawDown Start Date: ",drawDownStartDate)
    print("DrawDown End Date: ", drawDownEndtDate)
    print("DrawDown Start Trade No: ", ddStartTradeNo)
    print("DrawDown End Trade No: ", ddEndTradeN0)
    print("Trades Exceeding 5: ", tradesExceedingfive)
    print("Max Number of trades in a day: ", maxNumberOfTrades)
    print("Daywise Accurace: ", (dayWiseAccuracy/tradingDays)*100,"%")
    print("Tradewise Accuracy: ", (tradeWiseAccuracy / totalTrades) * 100, "%")
    plt.plot(x_axis, y_axis)
    plt.xlabel('Number of Trades')
    plt.ylabel('Total Profit')
    plt.title("Equity Curve")
    plt.show()
    tempInput = input("Continue? Y/N: ")
    if (tempInput == "N"):
        shouldLoop = False