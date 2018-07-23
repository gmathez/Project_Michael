import os #os.system('cls' if os.name == 'nt' else 'clear')
import sys #sys.exit("   ")
from Order import Order
from Constant_Upload import Order_identification_extract
from Timer import Time_Controler
from Poloniex import Poloniex
import time
from time import strftime

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def agreements():
    Response = input(
        "Welcome to our Trading System. Before to start the program please verify on the file CONSTANT.json " +
        "that all the information are correct\n Please write OK to continue : ")

    if not str(Response).upper() == 'OK':
        clear_terminal()
        print("\nYour answer was not OK, Please Restart if you want so.")
        return False
    clear_terminal()
    Response = input(
        "\n Be aware that this program can order, cancel order, etc without your permission. Please write AGREE to continue : ")

    if not str(Response).upper() == 'AGREE':
        clear_terminal()
        print("\nYour answer was not AGREE, Please Restart if you change of mind.")
        return False
    return True

def Public_Connexion_Control(poloniex_server, time_server):
    clear_terminal()
    print("\n The constants are load. We will try to connect to the public serveur of Poloniex.")
    continue_ = True
    nb = 0
    message = {}
    while continue_ and (nb <= 3):
        if time_server.Spike_Sender():
            message = poloniex_server.returnTicker()
            if "error" in message:
                nb += 1
                clear_terminal()
                print("\n The public connexion doesn't work. We will try a few time.")
            else:
                continue_ = False
                clear_terminal()
                print("\n The public connexion work fine. We will try now the private connection")
    if continue_ and (nb > 3):
        clear_terminal()
        print("\n The public connexion seem to have trouble : " + str(
            message["error"]) + ". Please try again in a few minutes")
        return False
    return True

def Close_System(entier):
    clear_terminal()
    if entier == 0:
        print("The Trading System will now process to its exit.")
        text = "END : " + strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) + "\n"
        fichier = open("Order_DONE.txt", "a")
        fichier.write(text)
        fichier.close()
        fichier = open("Order_NEW.txt", "a")
        fichier.write(text)
        fichier.close()
        time.sleep(10)
        sys.exit(entier)
    else:
        print("It seems that an error occur during the trading system. We apologize for that.")
        text = "ERROR SYSTEM : " + strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) + "\n"
        fichier = open("Order_DONE.txt", "a")
        fichier.write(text)
        fichier.close()
        fichier = open("Order_NEW.txt", "a")
        fichier.write(text)
        fichier.close()
        fichier = open("Order_OPEN_BEFORE.txt", "a")
        fichier.write(text)
        fichier.close()
        time.sleep(10)
        sys.exit(entier)


if __name__ == '__main__':

    """ AGREEMENT DECLEARATION """
    if not agreements():
        Close_System(1)

    """ INITALISATION SERVERS """
    time_server = Time_Controler()
    poloniex_server = Poloniex()
    order_identification = Order_identification_extract()
    order_server = Order(order_identification)

    """ CONTROL PUBLIC CONNEXION """
    time_server.Sleep_Time(10)
    if not Public_Connexion_Control(poloniex_server, time_server):
        Close_System(1)

    """ CONTROL PRIVATE CONNEXION """
    time_server.Sleep_Time(30)
    returnBalances = {}
    #continue_ = True #quand j'aurai les infos on pourras tester!
    continue_ = False
    nb = 0
    while continue_ and (nb <= 3):
        if time_server.Spike_Sender():
            returnBalances = poloniex_server.returnBalances()
            if "error" in returnBalances:
                nb += 1
                clear_terminal()
                print("\n The private connexion doesn't work. We will try a few time.")
            else:
                continue_ = False
                clear_terminal()
                print("\n The private connexion work fine.")
                time_server.Sleep_Time(10)
    if continue_ and (nb > 3):
        clear_terminal()
        print("\n The private connexion seem to have trouble : " + str(
            returnBalances["error"]) + ". Please try again in a few minutes and verify your API key and Secret")
        Close_System(1)

    clear_terminal()
    print("We can now begin to calculate the order and put everything in place for the trading")

    """SEE THE SITUATION OF THE ORDERS"""
    returnTicker = {}
    returnOpenOrders = {}
    time_server.Sleep_Time(30)
    if time_server.Spike_Sender():
        returnTicker = poloniex_server.returnTicker()
        if "error" in returnTicker:
            clear_terminal()
            print("An error occur during the return Ticker with this reason : " + str(returnOpenOrders["error"]))
            Close_System(1)
    time_server.Sleep_Time(30)
    if time_server.Spike_Sender():
        clear_terminal()
        print("Our Open orders will be write on a text file (Order_OPEN_BEFORE). \nUnfortunately all your open orders between the limit for your strategy will be cancel. \nBut when we will inform you about it, you can put again these orders without affecting the system")
        #returnOpenOrders = poloniex_server.returnOpenOrders("all")
        returnOpenOrders = {"XXX_YYY":[{"orderNumber":"120466","type":"sell","rate":"0.025","amount":"100","total":"2.5"},
                                       {"orderNumber": "127492", "type": "buy", "rate": "1.352", "amount": "50",
                                        "total": "2"},
                                       {"orderNumber": "73926", "type": "buy", "rate": "2", "amount": "100",
                                        "total": "2.5"}]}

        if "error" in returnOpenOrders:
            clear_terminal()
            print("An error occur during the return Order with this reason : " + str(returnOpenOrders["error"]))
            Close_System(1)

        time_server.Sleep_Time(20)

    text = "START : " + strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) + "\n"
    fichier = open("Order_DONE.txt", "w")
    fichier.write(text)
    fichier.close()
    fichier = open("Order_NEW.txt", "w")
    fichier.write(text)
    fichier.close()
    fichier = open("Order_OPEN_BEFORE.txt", "w")
    fichier.write(text)
    fichier.close()

    if not (len(returnOpenOrders) == 0):
        fichier = open("Order_OPEN_BEFORE.txt", "a")
        for key, values in returnOpenOrders.items():
            fichier.write("\n OPEN ORDER FOR : " + str(key))
            for element in values:
                fichier.write("\n\t OrderNumber : " + str(element["orderNumber"]) + " TYPE : " + str(element["type"]).upper() +
                              " RATE : " + str(element["rate"]) + " AMOUNT : " + str(element["amount"]) + " TOTAL : " + str(element["total"]))
            fichier.write("\n" * 2)
        fichier.close()
    else:
        fichier = open("Order_OPEN_BEFORE.txt", "a")
        fichier.write("\n NO OPEN ORDER")
        fichier.close()

    """CALCULATION OF THE ORDER OUT OF RANGE"""
    list_identification = list(order_identification.keys())
    if len(list_identification) == 0:
        print("You place no bloc in the CONSTANT.json. Restart when you complete the document")
        sys.exit(1)
    blocs = list(order_identification.values())
    currencyPair_interest = list(set([element["currencyPair"] for element in blocs]))
    Order_Bloc_Sort = {}
    for currency in currencyPair_interest:
        Order_Bloc_Sort[currency] = []
        for bloc in blocs:
            if bloc["currencyPair"] == currency:
                Order_Bloc_Sort[currency].append(bloc)

    Order_Limit = {}
    for key_order, values_order in Order_Bloc_Sort.items():
        if len(values_order) > 0:
            Order_Limit[key_order] = {}
            Order_Limit[key_order]["limit_MAX"] = values_order[0]["rate_sell"]
            Order_Limit[key_order]["limit_MIN"] = values_order[0]["rate_buy"]
            for order in values_order:
                if order["rate_sell"] > Order_Limit[key_order]["limit_MAX"]:
                    Order_Limit[key_order]["rate_MAX"] = order["amount_sell"]
                if order["rate_buy"] > Order_Limit[key_order]["limit_MIN"]:
                    Order_Limit[key_order]["limit_MIN"] = order["rate_buy"]

    Orders_to_cancel = []

    for currency in currencyPair_interest:
        if currency in returnOpenOrders:
            if len(returnOpenOrders[currency]) > 0:
                if currency in Order_Limit:
                    for open_order in returnOpenOrders[currency]:
                        if (float(open_order["rate"]) <= Order_Limit[currency]["limit_MAX"]) and (float(open_order["rate"]) >= Order_Limit[currency]["limit_MIN"]):
                            dic = {}
                            dic["currency"] = currency
                            dic["orderNumber"] = open_order["orderNumber"]
                            Orders_to_cancel.append(dic)

    fichier = open("Order_OPEN_BEFORE.txt", "a")
    if len(Orders_to_cancel) > 0:
        fichier.write("\n ORDER CANCELED : ")
        for order_to_cancel in Orders_to_cancel:
            fichier.write("\n ORDER NUMBER : " + str(order_to_cancel["orderNumber"]))
        print("The order that will be cancel as been written in Order_OPEN_BEFORE.txt")
    else:
        fichier.write("\n NO ORDER CANCEL")
        print("No Order will be cancel.")
    fichier.close()
    clear_terminal()

    """ORDER CANCEL"""
    if len(Orders_to_cancel) > 0:
        for order_dic in Orders_to_cancel:
            if time_server.Spike_Sender():
                #success = poloniex_server.cancel(order_dic["currency"], order_dic["orderNumber"])
                success = {"success": 1}
                if "error" in success:
                    clear_terminal()
                    print("Sorry An error occurs during the cancellation of the orderNumber : " +
                          str(order_dic["orderNumber"]) + "Error : " + str(success["error"]))
                    time_server.Sleep_Time(3)
                elif success["success"] == 1:
                    print("The order number : " + str(order_dic["orderNumber"] + " was canceled"))
                time_server.Sleep_Time(2.5)
    Orders_to_cancel.clear()

    os.system("pause")





















