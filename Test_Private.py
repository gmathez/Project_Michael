from Poloniex import Poloniex


if __name__ == '__main__':
    poloniex = Poloniex()
    returnOrder = poloniex.returnOpenOrders("all")
    #print(str(returnOrder["ETH_ZRH"]))
    print(returnOrder)
