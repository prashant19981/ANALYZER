# THIS SCRIPT CONTAINS TECHNICAL ANALYSIS TOOLS USED BY THE TRADERS


# TO CHECK IF THE BODY OF THE CANDLE IS MORE THAN 50% OF TOTAL CANDLE SIZE AND IF OPEN < CLOSE
def bullishCheck(open,high,low,close):
    range = high - low
    if (range == 0):
        return False
    bullishBodyPrev = close - open
    bodyPercentageBullish = (bullishBodyPrev / range) * 100

    if(bodyPercentageBullish > 50):
        return True
    return False

# TO CHECK IF THE BODY OF THE CANDLE IS MORE THAN 50% OF TOTAL CANDLE SIZE AND IF OPEN > CLOSE
def bearishCheck(open,high,low,close):
    range = high - low
    if (range == 0):
        return False
    bearishBodyPrev = open - close
    bodyPercentageBearish = (bearishBodyPrev / range) * 100
    if(bodyPercentageBearish > 50):
        return True
    return False

# CHECK IF THE CANDLE IS INVERTED HAMMMER

def isInvertedHammer(open,high,low,close):
    condition1 = False
    condition2 = False
    if(high != low):
        openVal = ((high-open)/(high-low))*100
        closeVal = ((high-close)/(high-low))*100
        if(openVal > 50.0):
            condition1 = True
        if(closeVal > 80.0):
            condition2 = True
        return condition1 and condition2
    else:
        return False

def isHammer(open,high,low,close):
    condition1 = False
    condition2 = False
    if (high != low):
        openVal = ((high - open) / (high - low)) * 100
        closeVal = ((high - close) / (high - low)) * 100
        # print(openVal, closeVal)
        # high-open/high-low should be greater than 50
        # high-close/high-low should be greater than 80 or 90
        if (openVal < 50.0):
            condition1 = True
        if (closeVal < 20.0):
            condition2 = True
        return condition1 and condition2
    else:
        return False
def isInsideCandle(prevHigh,prevLow,currentHigh,currentLow):
    if(prevHigh >= currentHigh and prevLow <= currentLow):
        return True



def intradayPercentCalculator(open,current):
    return  ((current-open)/open)*100


def percentCalculator(high,low):
    diff = high-low
    return (diff/low)*100