
class Order:

    def __init__(self, orders_identification):
        self.my_orders = []
        self.my_order_done = []
        self.orders_identification = orders_identification

    def Reset(self):
        """Reset the orders inside our system"""
        self.my_orders = []
        self.my_order_done = []

    def Order_done(self, Open_orders):
        """Compare between the order that you get from the server and the order that is our system. If our order is not\
        in the open order from the server it means that the order is done"""
        for order_identif in self.my_orders:
            order = order_identif["order"]
            order_number = order["orderNumber"]
            find = False
            for open_order in Open_orders:
                if order_number == open_order["orderNumber"]:
                    find = True
            if not find:
                self.my_order_done.append(order_identif)
                text = "\n" + "ORDER N°" + str(order["orderNumber"]) + " Type : " + str(
                    order["resultingTrades"][0]["type"]) + " Total : " + str(order["resultingTrades"][0]["total"])
                fichier = open("Order_DONE.txt", "a")
                fichier.write(text)
                fichier.close()
        for order in self.my_order_done:
            if order in self.my_orders:
                self.my_orders.remove(order)
        return None

    def New_order_after_done(self):
        """Calculate the new order that they have to sent to the server following our strategy"""
        new_orders = []
        if len(self.my_order_done) > 0:
            for order_done in self.my_order_done:
                if order_done["identification"] in self.orders_identification:
                    if order_done["order"]["resultingTrades"][0]["type"] == "buy":
                        new_orders.append({"identification": order_done["identification"], "type": "sell",
                                          "currencyPair": str(
                                              self.orders_identification[order_done["identification"]]["currencyPair"]),
                                          "amount": float(
                                              self.orders_identification[order_done["identification"]]["amount_sell"]),
                                          "rate": float(
                                              self.orders_identification[order_done["identification"]]["rate_sell"])})
                    elif order_done["order"]["resultingTrades"][0]["type"] == "sell":
                        new_orders.append({"identification": order_done["identification"], "type": "buy",
                                          "currencyPair": str(
                                              self.orders_identification[order_done["identification"]]["currencyPair"]),
                                          "amount": float(
                                              self.orders_identification[order_done["identification"]]["amount_buy"]),
                                          "rate": float(
                                              self.orders_identification[order_done["identification"]]["rate_buy"])})
        return new_orders

    def Add_New_order(self, new_order):
        self.my_orders.append(new_order)
        order = new_order["order"]
        text = "\n" + "ORDER N°" + str(order["orderNumber"]) + " Type : " + str(
            order["resultingTrades"][0]["type"]) + " Total : " + str(order["resultingTrades"][0]["total"])
        fichier = open("Order_NEW.txt", "a")
        fichier.write(text)
        fichier.close()

    def Add_New_orders(self, new_orders):
        for new_order in new_orders:
            self.Add_New_order(new_order)











