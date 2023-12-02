#include <Arduino_LSM6DS3.h>

float ax, ay, az, gx, gy, gz;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");

    while (1);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()){
    IMU.readAcceleration(ax, ay, az);
    Serial.print(ax);
    Serial.print('\t');
    Serial.print(ay);
    Serial.print('\t');
    Serial.print(az);
    Serial.print('\t');
    IMU.readGyroscope(gx, gy, gz);
    Serial.print(gx);
    Serial.print('\t');
    Serial.print(gy);
    Serial.print('\t');
    Serial.println(gz);
  }
}
