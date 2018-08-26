#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_INA219.h>
#include "communication.h"
#include "config.h"
 
WiFiClient espClient;
PubSubClient client(espClient);


void reconnect() {
    // Loop until we're reconnected
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (client.connect("ESP8266 Client")) {
            Serial.println("connected");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}

void setup_wifi() {
    
    delay(10);
    
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void publish(char* topic, char* data) {
    //Serial.print("Sending data: ");
    //Serial.println(data);

    if (client.publish(topic, data)){
       // Serial.println("Publish ok.");
    }
    else {
        Serial.println("Publish failed.");
    }
}

void setup_mqtt() {
    Serial.begin(9600);

    client.setServer(mqtt_server, 1883);
}

void ensure_connection() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();    
}