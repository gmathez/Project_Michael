import os #os.system('cls' if os.name == 'nt' else 'clear')
import sys #sys.exit("   ")
import signal
from Order import Order
from Constant_Upload import Order_identification_extract
from Timer import Time_Controler
from Poloniex import Poloniex
import time
from time import strftime
from random import uniform


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
    time_server.Sleep_Time(5)
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
        time.sleep(60)
        sys.exit(entier)


def CLOSE_PROJECT(signal, frame):
    Close_System(0)


signal.signal(signal.SIGINT, CLOSE_PROJECT)


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
    time_server.Sleep_Time(10)
    returnBalances = {}
    continue_ = True #quand j'aurai les infos on pourras tester!
    #continue_ = False
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
    returnOpenOrders = {}
    time_server.Sleep_Time(10)
    if time_server.Spike_Sender():
        clear_terminal()
        print("Our Open orders will be write on a text file (Order_OPEN_BEFORE). \nUnfortunately all your open orders between the limit for your strategy will be cancel. \nBut when we will inform you about it, you can put again these orders without affecting the system")
        returnOpenOrders = poloniex_server.returnOpenOrders()
        if "error" in returnOpenOrders:
            clear_terminal()
            print("An error occur during the return Order with this reason : " + str(returnOpenOrders["error"]))
            Close_System(1)

        time_server.Sleep_Time(30)

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
            if len(values) > 0:
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
                    Order_Limit[key_order]["limit_MAX"] = order["rate_sell"]
                if order["rate_buy"] < Order_Limit[key_order]["limit_MIN"]:
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
        fichier.write("\n ORDER THAT HAVE TO BE CANCELED : ")
        for order_canceled in Orders_to_cancel:
            fichier.write("\n ORDER NUMBER : " + str(order_canceled["orderNumber"]))
        print("The order that will be cancel as been written in Order_OPEN_BEFORE.txt")
    else:
        fichier.write("\n NO ORDER TO CANCEL")
        print("No Order will be cancel.")
    fichier.close()

    """ORDER CANCEL"""
    Orders_canceled = []
    if len(Orders_to_cancel) > 0:
        for order_dic in Orders_to_cancel:
            if time_server.Spike_Sender():
                success = poloniex_server.cancel(order_dic["currency"], order_dic["orderNumber"])
                #success = {"success": 1}
                if "error" in success:
                    clear_terminal()
                    print("Sorry An error occurs during the cancellation of the orderNumber : " +
                          str(order_dic["orderNumber"]) + "Error : " + str(success["error"]))
                    time_server.Sleep_Time(3)
                elif success["success"] == 1:
                    print(str(success["message"]) + "\n")
                    Orders_canceled.append(order_dic)
                    time_server.Sleep_Time(2.5)
    Orders_to_cancel.clear()

    fichier = open("Order_OPEN_BEFORE.txt", "a")
    if len(Orders_canceled) > 0:
        fichier.write("\n ORDER CANCELED : ")
        for order_canceled in Orders_canceled:
            fichier.write("\n ORDER NUMBER : " + str(order_canceled["orderNumber"]))
    else:
        fichier.write("\n NO ORDER CANCELED")
        print("No Order will be cancel.")
    fichier.close()

    print("If a order was not cancel it's not a udge problem. Just try to cancel this/these order(s).\n"
          "The system will place the new orders according to the strategy.\n")



    returnBalances = {}
    time_server.Sleep_Time(10)
    if time_server.Spike_Sender():
        returnBalances = poloniex_server.returnBalances()
        #returnBalances = {"ETH" : "100000000", "ZRX" : "100000000"}
        if "error" in returnBalances:
            print("An error occur during the demand of returnBalances with this message : " + str(returnBalances["error"]))
            time_server.Sleep_Time(10)
            Close_System(1)

    returnTicker = {}
    time_server.Sleep_Time(10)
    if time_server.Spike_Sender():
        returnTicker = poloniex_server.returnTicker()
        if "error" in returnTicker:
            clear_terminal()
            print("An error occur during the return Ticker with this reason : " + str(returnTicker["error"]))
            Close_System(1)

    # returnCurrencies = {}
    # time_server.Sleep_Time(5)
    # if time_server.Spike_Sender():
        # returnCurrencies = poloniex_server.returnCurrencies()
        # if "error" in returnCurrencies:
            # clear_terminal()
            # print("An error occur during the return Currencies with this reason : " + str(returnCurrencies["error"]))
            # Close_System(1)

    New_orders_to_do = []
    Total_money = {}
    for order in order_identification:
        new_order = {}
        new_order["identification"] = order
        order_param = order_identification[new_order["identification"]]
        rate_current = float(returnTicker[order_param["currencyPair"]]["last"])
        Money_BUY = str(str(order_param["currencyPair"]).split("_")[0])
        Money_SELL = str(str(order_param["currencyPair"]).split("_")[1])
        if Money_BUY not in Total_money:
            Total_money[Money_BUY] = float(returnBalances[Money_BUY])
        if Money_SELL not in Total_money:
            Total_money[Money_SELL] = float(returnBalances[Money_SELL])
        if rate_current > order_param["rate_sell"]:
            new_order["type"] = "buy"
            new_order["currencyPair"] = str(order_param["currencyPair"])
            new_order["amount"] = float(order_param["amount_buy"])
            new_order["rate"] = float(order_param["rate_buy"])
            # Total_money[Money_BUY] -= (new_order["amount"] * new_order["rate"]) / 100 * (100 + float(returnCurrencies[Money_BUY]["txFee"]))
            Total_money[Money_BUY] -= new_order["amount"] * new_order["rate"]
        else:
            new_order["type"] = "sell"
            new_order["currencyPair"] = str(order_param["currencyPair"])
            new_order["amount"] = float(order_param["amount_sell"])
            new_order["rate"] = float(order_param["rate_sell"])
            Total_money[Money_SELL] -= new_order["amount"]
        New_orders_to_do.append(new_order)

    Money_left = list(Total_money.values())
    Money_left.sort()
    if Money_left[0] < 0:
        print("You don't have enough money ! See where you don't have enough and start again the program \n")
        for element in Total_money.items():
            print("CURRENCY : {} AFTER THE ORDER IT WILL REST : {}".format(element[0], element[1]))
        print("The system will place what it can place and try again later. Please do the necessary if needed.\n")

    New_orders_to_do.sort(key=lambda order: abs(order["rate"] - float(returnTicker[order_identification[order["identification"]]["currencyPair"]]["last"])))

    Orders_done = []
    Orders_to_do_again = []

    for order in New_orders_to_do:
        time_server.Sleep_Time(1.5)
        order_done = {}
        order_done["identification"] = order["identification"]
        if time_server.Spike_Sender():
            if order["type"] == "buy":
                ORDER = poloniex_server.buy(order["currencyPair"], order["rate"], order["amount"])
            elif order["type"] == "sell":
                ORDER = poloniex_server.sell(order["currencyPair"], order["rate"], order["amount"])
            else:
                ORDER = {"error" : "TYPE UNKOWN"}
            if "error" in ORDER:
                print("An error occur during the transmission of the new order : ")
                print("ORDER TYPE : " + str(order["type"]) + " RATE : " + str(order["rate"]) + " AMOUNT : " + str(order["amount"]) + "\n")
                print("ERROR MESSAGE : " + str(ORDER["error"]) + "\n")
                print("The system will try to do again this order later on.\n")
                Orders_to_do_again.append(order)
            else:
                order_done["order"] = ORDER
                total = float(order["rate"]) * float(order["amount"])
                total = float("{0:.10f}".format(total))
                order_done["order"]["resultingTrades"] = {}
                order_done["order"]["resultingTrades"]["type"] = order["type"]
                order_done["order"]["resultingTrades"]["amount"] = order["amount"]
                order_done["order"]["resultingTrades"]["rate"] = order["rate"]
                order_done["order"]["resultingTrades"]["total"] = total
                Orders_done.append(order_done)

    order_server.Add_New_orders(Orders_done)

    clear_terminal()
    print("From Now, the system don't need you anymore. It will run alone. Before to leave, we'll give you some comments :\n"+
          "Please make sure that the computer will have always internet connexion\n"+
          "Please make sure that the computer have enough power for all the time that you need\n"+
          "An overheat may produce\n"+
          "If an error occurs, it will maybe stop\n"+
          "TO STOP THE PROGRAMME PLEASE PRESS CTRL + C\n\tHave a good day ;-) ")

    time_server.Sleep_Time(5)

    erreur = 0
    Retry = True
    tentatives = 1

    while Retry:
        print("Boucle : " + str(tentatives) + " TIME : " + strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) + "\n")
        Error = False
        returnOpenOrders_loop = {}
        if time_server.Spike_Sender():
            returnOpenOrders_loop = poloniex_server.returnOpenOrders()
            if "error" in returnOpenOrders_loop:
                print("An error occur during a return Open orders ask")
                time_server.Sleep_Time(10)
                Error = True

        if not Error:
            order_server.Order_done(returnOpenOrders_loop)
            Order_TO_DO = order_server.New_order_after_done()
            returnTicker_loop = {}
            if time_server.Spike_Sender():
                returnTicker_loop = poloniex_server.returnTicker()
                if "error" in returnTicker_loop:
                    print("An error occur during a return Ticker ask")
                    time_server.Sleep_Time(10)
                    Error = True

            if not Error:
                Order_TO_DO.extend(Orders_to_do_again)
                Orders_to_do_again.clear()
                Order_TO_DO.sort(key=lambda order: abs(
                    order["rate"] - float(returnTicker_loop[order_identification[order["identification"]]["currencyPair"]]["last"])))

                Orders_done = []
                for order in Order_TO_DO:
                    time_server.Sleep_Time(1.5)
                    order_done = {}
                    order_done["identification"] = order["identification"]
                    if time_server.Spike_Sender():
                        if order["type"] == "buy":
                            ORDER = poloniex_server.buy(order["currencyPair"], order["rate"], order["amount"])
                        elif order["type"] == "sell":
                            ORDER = poloniex_server.sell(order["currencyPair"], order["rate"], order["amount"])
                        else:
                            ORDER = {"error": "TYPE UNKOWN"}
                        if "error" in ORDER:
                            print("An error occur during the transmission of the new order : ")
                            print("ORDER TYPE : " + str(order["type"]) + " RATE : " + str(order["rate"]) + " AMOUNT : " + str(
                                order["amount"]) + "\n")
                            print("ERROR MESSAGE : " + str(ORDER["error"]) + "\n")
                            print("The system will try to do again this order later on.\n")
                            Orders_to_do_again.append(order)
                        else:
                            order_done["order"] = ORDER
                            total = float(order["rate"]) * float(order["amount"])
                            total = float("{0:.10f}".format(total))
                            order_done["order"]["resultingTrades"] = {}
                            order_done["order"]["resultingTrades"]["type"] = order["type"]
                            order_done["order"]["resultingTrades"]["total"] = total
                            order_done["order"]["resultingTrades"]["amount"] = order["amount"]
                            order_done["order"]["resultingTrades"]["rate"] = order["rate"]
                            Orders_done.append(order_done)

                order_server.Add_New_orders(Orders_done)
            else:
                Orders_to_do_again.extend(Order_TO_DO)
                Order_TO_DO.clear()
        if Error:
            erreur += 1
        else:
            erreur = 0

        if erreur == 0:
            Retry = True
        elif (erreur > 0) and (erreur <= 5):
            time_server.Sleep_Time(5)
            Retry = True
        elif (erreur > 5) and (erreur <= 10):
            time_server.Sleep_Time(60)
            Retry = True
        elif (erreur > 10) and (erreur <= 20):
            time_server.Sleep_Time(60)
            Retry = True
        elif (erreur > 20) and (erreur <= 25):
            time_server.Sleep_Time(5 * 60)
            Retry = True
        elif (erreur > 25) and (erreur <= 30):
            time_server.Sleep_Time(15 * 60)
            Retry = True
        elif (erreur > 30) and (erreur <= 40):
            time_server.Sleep_Time(30 * 60)
            Retry = True
        elif (erreur > 40) and (erreur <= 100):
            time_server.Sleep_Time(60 * 60)
            Retry = True
        else:
            Retry = False

        time_server.Sleep_Time(uniform(1, 10)*uniform(0, 10)*6+10)
        tentatives += 1

    Close_System(1)
























