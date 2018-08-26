import src.light_controller


# To avoid broken connection issues, we reconnect to the bulb when every 100th message is received
restart_time = 100
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
            print("Restart connection!")

        # We potentially get to much data and only need the first 4 bytes    
        value = int.from_bytes(msg.payload[:4], byteorder='little', signed=True)
        
        if value == 0:
            return
        
        if (msg.topic == "touchpad/x"):
            self.lightController.setTemperature(value)
        if (msg.topic == "touchpad/y"):
            self.lightController.setBrightness(value) 
        if (msg.topic == "touchpad/stat"):
            self.lightController.toggleLight(value)

