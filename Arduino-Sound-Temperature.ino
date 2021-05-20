#include "src/ArduinoRTClibrary/virtuabotixRTC.h"
#include <dht.h>

//RTC module pins
#define CLK 6
#define DAT 7
#define RST 8

//Interupt pin, for anemometer
#define SIGSEND 3

//DHT11 pin
#define DHT11_PIN 12

//Sets up DHT, RTC, and Interupt pins
virtuabotixRTC mh_rtc(CLK, DAT, RST);
dht DHT;
volatile byte state = LOW;

/*Updates RTC time and converts time 
 * from hour:minutes:seconds to seconds 
 */
uint16_t to_seconds() {

 mh_rtc.updateTime();
 
 int seconds = mh_rtc.seconds;
 int minutes = mh_rtc.minutes;
 int hours = mh_rtc.hours;

 return seconds + minutes * 60 + hours * 3600;
}

/*Opens serial monitor, initializes the RTC module
 * and interrupt pin
 */
void setup() {
  pinMode(SIGSEND, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(SIGSEND), printWindSpeed, RISING);
  Serial.begin(9600);
  mh_rtc.setDS1302Time(0, 0, 0, 0, 0, 0, 0);
}

//prints temperature and humidity every 1000ms
void loop() { 
 int chk = DHT.read11(DHT11_PIN);
 Serial.write(0b0);
 Serial.print(DHT.temperature);
 Serial.print(':');
 Serial.print(DHT.humidity);
 Serial.print(':');
 Serial.println(to_seconds());
 delay(1000);
}

//prints time when the circuit is closed
void printWindSpeed() { 
 Serial.write(0b1);
 Serial.println(to_seconds());
}
