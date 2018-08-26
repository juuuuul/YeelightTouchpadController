#!/usr/bin/env python3

from yeelight import Bulb
import src.utils
from src.config import CONFIG


class LightController:
    MIN_BRIGHTNESS = 1
    MAX_BRIGHTNESS = 100
    MIN_TEMPERATURE = 1700
    MAX_TEMPERATURE = 6500
    
    brightness = MIN_BRIGHTNESS
    temperature = MIN_TEMPERATURE
    tapping = False


    def __init__(self):
        self.ip = CONFIG["bulbIP"]
        self.brightnessFactor = CONFIG["brightnessFactor"]
        self.temperatureFactor = CONFIG["temperatureFactor"]


    def initializeBulb(self):   
        self.bulb = Bulb(self.ip)
        self.bulb.start_music()


    def setBrightness(self, value):

        self.brightness = clamp(self.brightness + value * self.brightnessFactor, self.MIN_BRIGHTNESS, self.MAX_BRIGHTNESS)

        try:
            self.bulb.set_brightness(self.brightness)
        except:
            print("Setting brightness failed")


    def setTemperature(self, value):

        value = clamp(value, -50, 50)

        self.temperature = clamp(self.temperature + value * self.temperatureFactor, self.MIN_TEMPERATURE, self.MAX_TEMPERATURE)
        
        try:
            self.bulb.set_color_temp(self.temperature)
        except:
            print("Setting temperature failed")


    def toggleLight(self, value):

        # If a tap occurs, the stat value is 9.
        # Sometimes multiple 9 in row are sent. In this case, we only toggle once for every 9-block.
        # Therefore, we are keeping tracking of being in a block or not by a tapping boolean.

        if value == 9 and not self.tapping:
            try:
               self.bulb.toggle()
            except:
                print("Toggling failed")

        # If a 9 is received, set tapping to True
        self.tapping = value == 9
    
