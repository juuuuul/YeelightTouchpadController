import json

CONFIG = {}


def loadConfig(path):
    global CONFIG 

    with open(path) as json_config:
        data = json.load(json_config)

    CONFIG["brokerIP"] = data["brokerIP"]
    CONFIG["port"] = data["port"]
    CONFIG["bulbIP"] = data["bulbs"][0]["ip"]
    CONFIG["brightnessFactor"] = data["bulbs"][0]["brightnessFactor"]
    CONFIG["temperatureFactor"] = data["bulbs"][0]["temperatureFactor"]  