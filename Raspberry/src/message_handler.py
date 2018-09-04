import src.light_controller
from src.config import CONFIG


lastMessage = {'x' : 0, 'y': 0}


class MessageHandler:

    def __init__(self, lightController):
        self.lightController = lightController    


    def receiveData(self, mosq, obj, msg):

        # We potentially get to much data and only need the first 4 bytes    
        value = int.from_bytes(msg.payload[:4], byteorder='little', signed=True)
        
        if value == 0:
            return


        # To avoid small accidental changes on the wrong axis, the value for an axis is only used
        # if the ratio between this axis and the other one is above a threshold given in the config 
        
        if (msg.topic == "touchpad/x" and self.isRatioHighEnough(value, lastMessage['y'])):
            self.lightController.changeColor(value)
            lastMessage['x'] = value

        if (msg.topic == "touchpad/y" and self.isRatioHighEnough(value, lastMessage['x'])):
            self.lightController.changeBrightness(value) 
            lastMessage['y'] = value

        if (msg.topic == "touchpad/tap"):
            self.lightController.toggleLight(value)

        if (msg.topic == "touchpad/double_tap"):
            self.lightController.toggleMode(value)

    
    def isRatioHighEnough(self, a, b):
        return b == 0 or abs(a / b) > CONFIG["axisThreshold"]