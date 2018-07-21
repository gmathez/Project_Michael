from Constant_Upload import API_key_extract, Secret_extract
import urllib.request
import urllib.parse
import json
import time
import hmac, hashlib

class Poloniex:

    def __init__(self):
        self.API_KEY = API_key_extract()
        self.SECRET = Secret_extract()

    def Poloiex_ASK(self, type, order={}):

        if (type == "returnTicker") or (type == "return24Volume"):
            with urllib.request.urlopen("https://poloniex.com/public?command=" + type) as response:
                json_data = response.read()
                try:
                    return json.loads(json_data)
                except json.JSONDecodeError as error:
                    print("\nERROR : The commande returnTicket or return24Volume have come with a " +
                          "error during the load of " +
                          "the jsonfile with this message : " + str(error.msg))
                    return {"error": "\n"}

        elif type == "returnOrderBook":
            if "currencyPair" not in order:
                order["currencyPair"] = "all"
            with urllib.request.urlopen("https://poloniex.com/public?command=returnOrderBook&currencyPair=" + order["currencyPair"] + "&depth=10") as response:
                json_data = response.read()
                try:
                    return json.loads(json_data)
                except json.JSONDecodeError as error:
                    print("\nERROR : The commande returnOrderBook have come with a " +
                          "error during the load of " +
                          "the jsonfile with this message : " + str(error.msg))
                    return {"error": "\n"}
        else:
            req = {}
            req['command'] = type
            req['nonce'] = int(time.time() * 10000)
            post_data = urllib.parse.urlencode(req)

            sign = hmac.new(self.SECRET, post_data, hashlib.sha512).hexdigest()
            headers = {'Sign': sign, 'Key': self.API_KEY}
            with urllib.request.urlopen(urllib.request.Request("https://poloniex.com/tradingApi", post_data, headers)) as response:
                json_data = response.read()
                try:
                    return json.loads(json_data)
                except json.JSONDecodeError as error:
                    print("\nERROR : The commande returnTicket or return24Volume have come with a " +
                          "error during the load of " +
                          "the jsonfile with this message : " + str(error.msg))
                    return {"error": "\n"}



