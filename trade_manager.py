import math
import technicals
from brokerage import brokerageCalculator
from brokerage import slippage
def profitCalculator(df,positionType,rpt):

    openPosition = False
    orderPlaced = False
    stopLossHit = False
    isLevelBreached = False
    stopLossTrailed = False
    rangeFailed = False
    entry = 0
    stopLoss = 0
    profit = 0
    qty = 0
    margin = 0
    leverage = 5
    exit = 0
    rangeLimit = 0.1
    rangeValue = 0
    timeOfEntry = "18:15:00"
    trailSLValue = 0
    targetPrice = 100
    if(positionType == "Long"):

        # CHECK FOR THE ENTRY CONDITIONS, FOR EXAMPLE A PULLBACK IN CASE OF TREND TRADING
        # OR RSI DIVERGENCE IN CASE OF REVERSAL TRADING

        entry_condition = True
        for high,close,low,time,open in zip(df['High'],df['Close'],df['Low'],df['Time'],df['Open']):

            # STOP THE LOOP IF STOPLOSS IS HIT

            if(stopLossHit == True):
                break

            if(entry_condition and orderPlaced == False):

                # SET THE ENTRY PRICE FOR PROFIT CALCULATION

                entry = close

                # SET THE STOPLOSS PRICE
                stopLoss = low

                orderPlaced = True

                # BELOW CODE CHECKS THE RANGE OF STOPLOSS AND ENTRY PRICE, IF IT IS TOO SMALL THEN THE TRADE
                # IS REJECTED AS THE TRADE BECOMES AN OUTLIER AND MARGIN LIMIT IS BREACHED

                range = entry - stopLoss

                if (range > 0 and technicals.percentCalculator(entry, stopLoss) > rangeLimit):

                    # CALCULATING THE QUANTITY OF THE STOCK TO BUY BASED ON RISK PER TRADE(RPT)
                    # USING FLOOR FUNCTION TO MINIMIZE THE RISK
                    qty = math.floor(rpt / range)

                else:
                    # IN CASE THE RANGE OF THE STOCK IS TOO SMALL WE SKIP TRADING THE STOCK
                    stopLossHit = True
                    qty = 0
                    rangeFailed = True


            # ONCE ORDER IS PLACED WE CHECK IF THE ENTRY PRICE IS TRIGGERED OR NOT

            if(orderPlaced == True and openPosition == False):

                # To check if the order placed is executed or not

                if(high > entry):

                    # BELOW CODE HANDLES THE CASE WHEN THE ENTRY PRICE AND STOPLOSS IS HIT IN THE SAME CANDLE
                    # IN THIS CASE WE TREAT THE TRADE AS A NORMAL STOPLOSS HIT TRADE TO MAKE THE SYSTEM ROBUST

                    if(low < stopLoss):
                        profit = qty * (stopLoss - entry) - brokerageCalculator(entry, stopLoss, qty) - slippage(entry,stopLoss,qty)
                        exit = stopLoss
                        stopLossHit = True
                        timeOfEntry = time
                    else:
                        openPosition = True
                        timeOfEntry = time
                        margin = (entry*qty)/leverage



            elif(openPosition == True):
                #CHECKING IF THE STOPLOSS IS HIT OR TARGET IS HIT ONCE THE POISTION IS OPEN
                if(low < stopLoss):
                    profit = qty*(stopLoss -entry ) - brokerageCalculator(entry,stopLoss,qty) - slippage(entry,stopLoss,qty)
                    exit = stopLoss
                    stopLossHit = True
                elif (close > targetPrice):
                    profit = qty*(close -entry ) - brokerageCalculator(entry,close,qty) - slippage(entry,close,qty)
                    exit = close
                    stopLossHit = True
                # IF TARGET OR STOPLOSS IS NOT HIT THEN CLOSING THE TRADE 5 MINUTES PRIOR TO MARKET CLOSE
                elif(time == "15:10:00"):
                    profit = qty * (close - entry) - brokerageCalculator(entry, close, qty) - slippage(entry, close,qty)
                    exit = close
                    stopLossHit = True


    # SAME CODE FOR SHORT POSITION

    elif(positionType == "Short"):
        entry_condition = True
        for high,close,low,time,open in zip(df['High'],df['Close'],df['Low'],df['Time'],df['Open']):

            if(stopLossHit == True):
                break

            if(entry_condition and orderPlaced == False):
                entry = close

                # STOPLOSS SET AS CANDLE HIGH FOR SHORT TRADES
                stopLoss = high
                orderPlaced = True
                range = stopLoss - entry

                if (range > 0 and technicals.percentCalculator(stopLoss, entry) > rangeLimit):
                    qty = math.floor(rpt/range)

                else:
                    stopLossHit = True
                    qty = 0
                    rangeFailed = True

            if(orderPlaced == True and openPosition == False):
                # To check if the order placed is executed or not
                if(low < entry):
                    if(high > stopLoss):
                        profit = qty * (entry - stopLoss) - brokerageCalculator(stopLoss, entry, qty) - slippage(stopLoss,entry,qty)
                        stopLossHit = True
                        exit = stopLoss
                        timeOfEntry = time
                    else:
                        openPosition = True
                        timeOfEntry = time
                        margin = (entry * qty) / leverage



            elif(openPosition == True):

                if(high > stopLoss):
                    profit = qty*(entry -stopLoss ) - brokerageCalculator(stopLoss,entry,qty) - slippage(stopLoss,entry,qty)
                    stopLossHit = True
                    exit = stopLoss
                elif(close < targetPrice):
                    profit = qty * (entry - close) - brokerageCalculator(close, entry, qty) - slippage(close, entry,qty)
                    exit = close
                    stopLossHit = True
                elif (time == "15:10:00"):
                    profit = qty*(entry -close)- brokerageCalculator(close,entry,qty) - slippage(close,entry,qty)
                    exit = close
                    stopLossHit = True

    # RETURNING ESSENTIAL TRADE INFORMATION

    return profit,entry,stopLoss,qty,isLevelBreached,timeOfEntry,margin,exit,rangeFailed




