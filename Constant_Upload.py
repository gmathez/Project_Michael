import json

def Extraction_constant():
    with open("CONSTANT.json") as json_data:
        return json.load(json_data)

def API_key_extract():
    return str(Extraction_constant()["LOGIN"]["API_KEY"])

def Secret_extract():
    return str(Extraction_constant()["LOGIN"]["SECRET"])

def Order_identification_extract():
    data = Extraction_constant()
    orders_bloc = data["TRADES"]
    orders_identification = {}
    for order_bloc in orders_bloc:
        orders_identification[order_bloc["IDENTIFICATION"]] = order_bloc["TRADE"]
    return orders_identification
