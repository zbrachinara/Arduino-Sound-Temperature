#include "src/ArduinoRTClibrary/virtuabotixRTC.h"
#define CLK 6
#define DAT 7
#define RST 8

#define SIGSEND 4

virtuabotixRTC mh_rtc(CLK, DAT, RST);

#include <dht.h>

dht DHT;

#define DHT11_PIN 12
volatile byte state = LOW;

uint16_t to_seconds() {

 int seconds = mh_rtc.seconds;
 int minutes = mh_rtc.minutes;
 int hours = mh_rtc.hours;

 return seconds + minutes * 60 + hours * 3600;
  
}

void setup() {

  pinMode(SIGSEND, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(SIGSEND), printWindSpeed, RISING);
  Serial.begin(9600);
  mh_rtc.setDS1302Time(0, 0, 0, 0, 0, 0, 0);
  
  
}

void loop() {
 int chk = DHT.read11(DHT11_PIN);
 Serial.print("Temperature = ");
 Serial.println(DHT.temperature);
 Serial.print("Humidity = ");
 Serial.println(DHT.humidity);
 delay(5000);
}

void printWindSpeed() {
 mh_rtc.updateTime();
 Serial.println(to_seconds());
}
