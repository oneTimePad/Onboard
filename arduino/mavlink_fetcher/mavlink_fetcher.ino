#include <Mavlink.h>

const unsigned TRIGGER_PIN = 2;
volatile bool trigger_state = 0;
Mavlink mav(Serial1);
volatile  int lol = 0;

void fct() {
  trigger_state = 1;
}

void setup() {
	Serial.begin(9600);
	while(!Serial); // for arduino micro
  Serial1.begin(57600);
    attachInterrupt(digitalPinToInterrupt(TRIGGER_PIN),fct,FALLING);
//      pinMode(TRIGGER_PIN,INPUT);

}

void loop() {
/*
 mav.read();
       Mavlink::attributes attribs = mav.getAttribs();
  Serial.print("   Lat: "); Serial.print(attribs.lat);
  Serial.print("   Lon: "); Serial.print(attribs.lon);
  Serial.print("   Rel Alt: "); Serial.print(attribs.rel_alt);
  Serial.print("   Roll: "); Serial.print(attribs.roll);
  Serial.print("   Pitch: "); Serial.print(attribs.pitch);
  Serial.print("   Yaw: "); Serial.println(attribs.yaw);
*/

//      mav.read();
//  bool current_state = digitalRead(TRIGGER_PIN);
//  //Serial.println(current_state);
//  if(current_state != trigger_state) {
//    if ((trigger_state = current_state)==LOW) {
//      Serial.println(lol++);
//    
////       Mavlink::attributes attribs = mav.getAttribs();
////  Serial.print("   Lat: "); Serial.print(attribs.lat);
////  Serial.print("   Lon: "); Serial.print(attribs.lon);
////  Serial.print("   Rel Alt: "); Serial.print(attribs.rel_alt);
////  Serial.print("   Roll: "); Serial.print(attribs.roll);
////  Serial.print("   Pitch: "); Serial.print(attribs.pitch);
////  Serial.print("   Yaw: "); Serial.println(attribs.yaw);
//    }
//    }

      if (trigger_state) {
        trigger_state = 0;
        Serial.println(++lol);
      }
  
}
