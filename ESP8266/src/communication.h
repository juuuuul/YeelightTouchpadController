#ifndef communication_h
#define communication_h

void setup_wifi();
void setup_mqtt();
void publish(char* topic, char* data);
void ensure_connection();

#endif