
# CALCULATING THE SLIPPAGE
def slippage(buyPrice,sellPrice,qty):
    slippagePercent = 0.4/100
    slippageValue = sellPrice*slippagePercent + buyPrice*slippagePercent
    return  slippageValue

# BROKERAGE CALCULATED USING THE METHOD OF INDIA'S TOP BROKING FIRM

def brokerageCalculator(buyPrice,sellPrice,qty):
    brokerage_buy = 20 if ((buyPrice * qty * 0.0003) > 20) else round(buyPrice * qty * 0.0003, 2)
    brokerage_sell = 20 if ((sellPrice * qty * 0.0003) > 20) else round(sellPrice * qty * 0.0003, 2)
    brokerage = round(brokerage_buy + brokerage_sell, 2)
    turnover = round((buyPrice + sellPrice) * qty, 2)
    stt_total = round((sellPrice * qty) * 0.00025, 2)
    exc_trans_charge = round(0.0000345 * turnover, 2)
    stax = round(0.18 * (brokerage + exc_trans_charge), 2)
    sebi_charges = round(turnover * 0.000001, 2)
    stamp_charges = round((buyPrice * qty) * 0.00003, 2)
    cc = 0
    total_tax = round(brokerage + stt_total + exc_trans_charge + cc + stax + sebi_charges + stamp_charges, 2)
    return total_tax