from Order import Order

order_identification = {1: {"currencyPair": "BTC_XRP", "amount_buy": 10, "amount_sell": 8, "rate_buy": 0.0023,
                             "rate_sell": 0.0025}}

MY_order = Order(order_identification)

new_orders = [{"identification": 1, "order": {"orderNumber": 10002, "resultingTrades" : [{"amount": 10,
                                                                                           "date": "2018-07-19 21:08",
                                                                                           "rate": 0.0023,
                                                                                           "total": 0.023,
                                                                                           "tradeID": 21029,
                                                                                           "type": "buy"}]}}]
MY_order.Add_New_orders(new_orders)

#MY_order.Order_done([{"orderNumber": 10002}])
#MY_order.Order_done([{"orderNumber": 10003}])

for numero in range(0, 10):
    orders = [{"identification": 1, "order": {"orderNumber": numero, "resultingTrades": [{"amount": 10,
                                                                                "date": "2018-07-19 21:08",
                                                                                "rate": 0.0023,
                                                                                "total": 0.023,
                                                                                "tradeID": 21029,
                                                                                "type": "buy"}]}}]
    MY_order.Add_New_orders(orders)
    MY_order.Order_done([])


order_new = [{"identification": 1, "order": {"orderNumber": 20, "resultingTrades": [{"amount": 10,
                                                                                "date": "2018-07-19 21:08",
                                                                                "rate": 0.0023,
                                                                                "total": 0.023,
                                                                                "tradeID": 21029,
                                                                                "type": "sell"}]}}]
MY_order.Reset()
MY_order.Add_New_orders(order_new)
MY_order.Order_done([])
next_order = MY_order.New_order_after_done()
print(next_order)

