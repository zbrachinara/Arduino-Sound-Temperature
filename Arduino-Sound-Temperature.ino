#include "src/ArduinoRTClibrary/virtuabotixRTC.h"
#define CLK 6
#define DAT 7
#define RST 8

#define SIGSEND 4

virtuabotixRTC mh_rtc(CLK, DAT, RST);

void setup() {

  pinMode(SIGSEND, INPUT);
  Serial.begin(9600);
  mh_rtc.setDS1302Time(0, 0, 0, 0, 0, 0, 0);
  
}

void loop() {
  
  mh_rtc.updateTime();

  if (digitalRead(SIGSEND)==HIGH) {
    Serial.println(mh_rtc.seconds);
    while(digitalRead(SIGSEND)==HIGH) {
      
    }
  }
  
}
