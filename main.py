import os #os.system('cls' if os.name == 'nt' else 'clear')
import sys #sys.exit("   ")
from Order import Order
from Constant_Upload import Order_identification_extract
from Timer import Time_Controler
from Poloniex import Poloniex

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def agreements():
    Response = input(
        "Welcome to our Trading System. Before to start the program please verify on the file CONSTANT.json " +
        "that all the information are correct\n Please write OK to continue : ")

    if not (Response == 'OK') and not (Response == 'ok'):
        clear_terminal()
        print("\nYour answer was not OK, Please Restart if you want so.")
        return False
    clear_terminal()
    Response = input(
        "\n Be aware that this program can order, cancel order, etc without your permission. Please write AGREE to continue : ")

    if not (Response == 'AGREE') and not (Response == 'agree'):
        clear_terminal()
        print("\nYour answer was not AGREE, Please Restart if you change of mind.")
        return False
    return True

if __name__ == '__main__':

    if not agreements():
        sys.exit(0)

    time_server = Time_Controler()
    poloniex_server = Poloniex()
    order_server = Order(Order_identification_extract())


