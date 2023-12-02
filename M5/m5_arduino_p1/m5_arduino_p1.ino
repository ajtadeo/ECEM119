#include <Arduino_LSM6DS3.h>
#include <ArduinoHttpClient.h>
#include "secrets.h"
#include <SPI.h>
#include <WiFiNINA.h>

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
char host[] = "172.20.10.2";
int port = 9000;

WiFiClient wifiClient;
HttpClient client = HttpClient(wifiClient, host, port);

int status = WL_IDLE_STATUS;              // the Wi-Fi radio's status
unsigned long previousMillisInfo = 0;     //will store last time Wi-Fi information was updated
const int intervalInfo = 50;            // interval at which to update the board information

String move = "";

void setup() {
  Serial.begin(9600);
  while (!Serial);

  pinMode(LED_BUILTIN, OUTPUT);

  // initialize IMU
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // connect to wifi
  while (status != WL_CONNECTED){
    Serial.print("Attempting to connect to network: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println("Connected");
  Serial.println("---------------------------------------");
}

void loop() {
  float gx_start, gx_end, gy_start, gy_end, gz;
  unsigned long currentMillisInfo = millis();

  if (currentMillisInfo - previousMillisInfo >= intervalInfo) {
    previousMillisInfo = currentMillisInfo;
    if (IMU.accelerationAvailable()){
      IMU.readGyroscope(gx_start, gy_start, gz);

      if (gx_start > 700){
        delay(170);
        IMU.readGyroscope(gx_end, gy_end, gz);
        if (gx_end < -600) {
          // Serial.println("UP");
          move = "up";
        }
      } else if (gy_start > 300) {
        delay(170);
        IMU.readGyroscope(gx_end, gy_end, gz);
        if (gy_end < -400) {
          // Serial.println("DOWN");
          move = "down";
        }
      } else {
        move = "";
      }

      // only send HTTP requests if movement is detected
      if (move != "") {
        // construct payload
        String payload = "{\"move\":\"" + move + "\"}";

        // send POST request
        client.beginRequest();
        client.post("/p1");
        client.sendHeader("Content-Type", "application/json");
        client.sendHeader("Content-Length", payload.length());
        client.beginBody();
        client.print(payload);
        client.endRequest();

        // read POST response
        // Serial.println(client.responseStatusCode());
        // Serial.println(client.responseBody());
      }
    }
  }
}
