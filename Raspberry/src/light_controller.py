#!/usr/bin/env python3

from yeelight import Bulb
from src.utils import clamp
from src.config import CONFIG
import threading


MODE = ["TEMP", "HUE"]


class LightController:
    MIN_BRIGHTNESS = 1
    MAX_BRIGHTNESS = 100

    MIN_TEMPERATURE = 1700
    MAX_TEMPERATURE = 6500

    MIN_HUE = 0
    MAX_HUE = 359
    
    brightness = MIN_BRIGHTNESS
    temperature = MIN_TEMPERATURE
    hue = MIN_HUE

    mode = 0  # TEMP


    def __init__(self):
        self.ip = CONFIG["bulbIP"]
        self.brightnessFactor = CONFIG["brightnessFactor"]
        self.temperatureFactor = CONFIG["temperatureFactor"]
        self.hueFactor = CONFIG["hueFactor"]
        self.reconnectInterval = CONFIG["reconnectInterval"]


    def initializeBulb(self):   
        try:
            self.bulb = Bulb(self.ip, effect="smooth", duration=1000)
            print("Initialized bulb successfully")
        except:
            print("Bulb initializatio failed")

        try:
            self.bulb.start_music()
            print("Started music mode successfully")
        except:
            print("Music mode failed")

        threading.Timer(self.reconnectInterval, self.initializeBulb).start()


    def changeBrightness(self, value):
        new_value = round(clamp(self.brightness + value * self.brightnessFactor, self.MIN_BRIGHTNESS, self.MAX_BRIGHTNESS))
        if not new_value ==  self.brightness:
            self.brightness = new_value
            self.setBrightness()


    def setBrightness(self):
        try:
            self.bulb.set_brightness(self.brightness)
        except:
            print("Setting brightness failed")


    def changeColor(self, value):
        if self.mode == 0:
            value = clamp(value, -50, 50)
            new_value = round(clamp(self.temperature + value * self.temperatureFactor, self.MIN_TEMPERATURE, self.MAX_TEMPERATURE))
            if not new_value == self.temperature:
                self.temperature = new_value
                self.setTemperature()
                

        if self.mode == 1:
            new_value = round((self.hue + value * self.hueFactor) % self.MAX_HUE)
            if not new_value == self.hue:
                self.hue = new_value
                self.setHue()


    def setTemperature(self):
        try:
            self.bulb.set_color_temp(self.temperature)
        except:
            print("Setting temperature failed")


    def setHue(self):
        try:
            self.bulb.set_hsv(self.hue, 100)
        except:
            print("Setting hue failed")


    def toggleLight(self, value):

        if value:
            try:
                self.bulb.toggle()
                print("Toggle!")
            except:
                print("Toggling failed")


    def toggleMode(self, value):

        if value:
            self.mode = (self.mode + 1) % len(MODE)

            if self.mode == 0:
                self.setTemperature()
            if (self.mode == 1):
                self.setHue()



