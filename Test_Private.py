from Poloniex import Poloniex
import time

if __name__ == '__main__':
    poloniex = Poloniex()
    returnOrder = poloniex.returnOpenOrders()
    # {"XXX_YYY" : [{'orderNumber': '21429192550', 'type': 'buy', 'rate': '0.00200001',
    # 'startingAmount': '100.00000000', 'amount': '100.00000000', 'total': '0.20000100', 'date': '2018-07-25 10:34:28',
    # 'margin': 0}]}
    print(str(returnOrder["ETH_ZRX"]))

    if True :
        time.sleep(1)
        returnBalances =poloniex.returnBalances()
        print("\nETH : " + returnBalances["ETH"] + " ZRX : " + returnBalances["ZRX"] + " \n")

        time.sleep(1)
        returnTicker = poloniex.returnTicker()
        print(str(returnTicker["ETH_ZRX"]))

        """ime.sleep(1)
        cancel = poloniex.cancel("ETH_ZRX", returnOrder["ETH_ZRX"][0]["orderNumber"])
        # {'success': 1, 'amount': '60.00000000', 'message': 'Order #21389963818 canceled.'}
        print("CANCEL : " + str(cancel) + " \n")

        time.sleep(1)
        returnBalances = poloniex.returnBalances()
        print("\nETH : " + returnBalances["ETH"] + " ZRX : " + returnBalances["ZRX"] + " \n")

        time.sleep(1)
        buy = poloniex.buy("ETH_ZRX", 0.00200001, 100)
        # {'orderNumber': '21448329394', 'resultingTrades': []} sell
        print("BUY : " + str(buy) + "\n")

        time.sleep(1)
        returnBalances = poloniex.returnBalances()
        print("\nETH : " + returnBalances["ETH"] + " ZRX : " + returnBalances["ZRX"] + " \n")"""



