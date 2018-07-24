from Poloniex import Poloniex


if __name__ == '__main__':
    poloniex = Poloniex()
    returnOrder = poloniex.returnBalances()
    #print(str(returnOrder["ETH_ZRX"]))
    print(returnOrder)

