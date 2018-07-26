from Constant_Upload import API_key_extract, Secret_extract
import urllib.request
import urllib.parse
import json
import time
import hmac, hashlib
from urllib.error import URLError, HTTPError
from URL_Error import Return_Code
from socket import timeout


class Poloniex:

    def __init__(self):
        self.API_KEY = API_key_extract()
        self.SECRET = Secret_extract()

    def Poloiex_ASK(self, type, req={}):

        if (type == "returnTicker") or (type == "return24Volume") or (type == "returnCurrencies"):
            try:
                with urllib.request.urlopen("https://poloniex.com/public?command=" + type) as response:
                    json_data = response.read()
                    return json.loads(json_data)
            except HTTPError as error:
                print('The Server couldn\'t fulfill the request\n')
                print("\t Error code : " + error.code +  " " + Return_Code(error.code)[0] + " " + Return_Code(error.code)[1] + "\n")
                return {"error": "\n"}
            except URLError as error:
                print("We failed to reach a server \n")
                print("\t Reason : " + str(error.reason) + "\n")
                return {"error": "\n"}
            except timeout:
                print("We failed to reach a server because it's too long\n")
                return {"error": "\n"}
            except json.JSONDecodeError as error:
                print("\nERROR : The command returnTicket or return24Volume have come with a " +
                        "error during the load of " +
                        "the jsonfile with this message : " + str(error.msg))
                return {"error": "\n"}
        else:
            req['command'] = str(type)
            req['nonce'] = int(time.time() * 10000)
            post_data = urllib.parse.urlencode(req).encode()

            sign = hmac.new(self.SECRET.encode(), post_data, hashlib.sha512).hexdigest()
            headers = {'Sign': str(sign),
                       'Key': str(self.API_KEY),
                       'Content-Type': 'application/x-www-form-urlencoded'}
            try:

                with urllib.request.urlopen(urllib.request.Request("https://poloniex.com/tradingApi", post_data, headers)) as response:
                    json_data = response.read()
                    return json.loads(json_data)
            except HTTPError as error:
                if int(error.code) == 422:
                    print("An error occur with false informations during the ordertype : " + str(type) + " : " + str(req) + "\n")
                print('The Server couldn\'t fulfill the request\n')
                print("\t Error code : " + str(error.code) +  " " + str(Return_Code(error.code)[0]) + " " + str(Return_Code(error.code)[1]) + "\n")
                return {"error": "\n"}
            except URLError as error:
                print("We failed to reach a server \n")
                print("\t Reason : " + str(error.reason) + "\n")
                return {"error": "\n"}
            except timeout:
                print("We failed to reach a server because it's too long\n")
                return {"error": "\n"}
            except json.JSONDecodeError as error:
                print("\nERROR : The command "+ str(type).upper()+" have come with a " +
                        "error during the load of " +
                        "the jsonfile with this message : " + str(error.msg))
                return {"error": "\n"}

    def returnTicker(self): #PUBLIC
        return self.Poloiex_ASK("returnTicker")

    def returnCurrencies(self): #PUBLIC
        return self.Poloiex_ASK("returnCurrencies")

    def return24Volume(self): #PUBLIC
        return self.Poloiex_ASK("return24Volume")

    def returnBalances(self): #PRIVATE
        return self.Poloiex_ASK("returnBalances")

    def returnOpenOrders(self, currencyPair = "all"): #PRIVATE
        return self.Poloiex_ASK("returnOpenOrders", {"currencyPair": currencyPair})

    def buy(self, currencyPair, rate, amount): #PRIVATE
        return self.Poloiex_ASK("buy", {"currencyPair": currencyPair, "rate": rate, "amount": amount})

    def sell(self, currencyPair, rate, amount): #PRIVATE
        return self.Poloiex_ASK("sell", {"currencyPair": currencyPair, "rate": rate, "amount": amount})

    def cancel(self, currencyPair, orderNumber): #PRIVATE
        return self.Poloiex_ASK("cancelOrder", {"currencyPair": currencyPair, "orderNumber": orderNumber})


