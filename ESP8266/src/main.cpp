#include <stdio.h>
#include <Wire.h>
#include <Adafruit_INA219.h>
#include "communication.h"
#include "touchpad.h"


char msg[50];


void setup() {
    Serial.begin(9600);
    while (!Serial) continue;

    // Connection to the raspberry pi
    setup_wifi();
    setup_mqtt();

    // Touchpad
    mouse_init();
}


union coord {
    int pos;
    char pos_chr[4];
};


void loop() {

    ensure_connection();

    mouse_data data = read_mouse_data();

    // Interpret positional data as char array
    publish("touchpad/x", (char*)&data.x);
    publish("touchpad/y", (char*)&data.y);
    publish("touchpad/stat", (char*)&data.stat);
    publish("touchpad/tap", (char*)&data.tap);
    publish("touchpad/double_tap", (char*)&data.double_tap);
}