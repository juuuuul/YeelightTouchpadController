import src.light_controller


# To avoid broken connection issues, we reconnect to the bulb when every 100th message is received
restart_time = 1000
timer = 0


class MessageHandler:

    def __init__(self, lightController):
        self.lightController = lightController    


    def receiveData(self, mosq, obj, msg):
        global timer, restart_time

        timer += 1
        if timer == restart_time:     
            self.lightController.initializeBulb()
            timer = 0

        # We potentially get to much data and only need the first 4 bytes    
        value = int.from_bytes(msg.payload[:4], byteorder='little', signed=True)
        
        if value == 0:
            return
        
        if (msg.topic == "touchpad/x"):
            self.lightController.changeColor(value)
        if (msg.topic == "touchpad/y"):
            self.lightController.changeBrightness(value) 
        if (msg.topic == "touchpad/tap"):
            self.lightController.toggleLight(value)
        if (msg.topic == "touchpad/double_tap"):
            self.lightController.toggleMode(value)

