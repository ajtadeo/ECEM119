#include "secrets.h"
#include <SPI.h>
#include <WiFiNINA.h>

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;

int status = WL_IDLE_STATUS;              // the Wi-Fi radio's status
unsigned long previousMillisInfo = 0;     //will store last time Wi-Fi information was updated
const int intervalInfo = 5000;            // interval at which to update the board information

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial);

  while (status != WL_CONNECTED){
    Serial.print("Attempting to connect to network: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }
  Serial.println("Connected");
  Serial.println("---------------------------------------");
}

void loop() {
  // print RSSI info
  unsigned long currentMillisInfo = millis();
  if (currentMillisInfo - previousMillisInfo >= intervalInfo) {
    previousMillisInfo = currentMillisInfo;
    long rssi = WiFi.RSSI();
    Serial.print("signal strength (RSSI):");
    Serial.println(rssi);
  }
}
