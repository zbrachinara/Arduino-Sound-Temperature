#include "src/ArduinoRTClibrary/virtuabotixRTC.h"
#define CLK 6
#define DAT 7
#define RST 8

virtuabotixRTC mh_rtc(CLK, DAT, RST);

void setup() {

  Serial.begin(9600);
  mh_rtc.setDS1302Time(0, 0, 0, 0, 0, 0, 0);
  
}

void loop() {

  delay(5000);
  mh_rtc.updateTime();

  Serial.println(mh_rtc.seconds);
  
}
