import paho.mqtt.client as mqtt
from src.config import CONFIG

mqttc = mqtt.Client()

print("Started subscriber.")


def on_connect(mosq, obj, falgs, rc):
    mqttc.subscribe("touchpad/x", 0)
    mqttc.subscribe("touchpad/y", 0)
    # mqttc.subscribe("touchpad/stat", 0)
    mqttc.subscribe("touchpad/tap", 0)
    mqttc.subscribe("touchpad/double_tap", 0)


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mosq, obj, level, string):
    print(string)


def start_mqtt():
    global mqttc
    
    # Connect
    mqttc.connect(CONFIG["brokerIP"], CONFIG["port"])

    # Assign event callbacks
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe


def set_on_message_callback(func):
    global mqttc
    
    mqttc.on_message = func
    
    # Continue the network loop
    mqttc.loop_forever()