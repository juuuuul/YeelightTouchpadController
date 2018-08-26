#!/usr/bin/env python3


from src.light_controller import LightController
from src.message_handler import MessageHandler
from src.config import loadConfig
from src.subscriber import start_mqtt, set_on_message_callback


if __name__ == "__main__":
    loadConfig("config.json")
    
    # Create a light controller and initialize a bulb
    lightController = LightController()
    lightController.initializeBulb()

    # Create a message handler and pass the light controller
    messageHandler = MessageHandler(lightController)

    # Start the mqtt service and set the 
    start_mqtt()
    set_on_message_callback(messageHandler.receiveData)