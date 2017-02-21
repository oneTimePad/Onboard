#include <Mavlink.h>

const unsigned TRIGGER_PIN = 2; //input pin
volatile bool trigger_state = 0; 
Mavlink mav(Serial1);


void fct() {
  trigger_state = 1; //triggered

}

void setup() { 
  Serial.begin(9600);
  Serial1.begin(57600);
  attachInterrupt(digitalPinToInterrupt(TRIGGER_PIN),fct,FALLING);
  pinMode(TRIGGER_PIN,INPUT);

}

void loop() {
     	mav.read();
	//when triggered output to serial
	if (trigger_state) {
		Mavlink::attributes attribs = mav.getAttribs();
		Serial.print(attribs.lat);
		Serial.print(',');
		Serial.print(attribs.lon);
		Serial.print(',');
		Serial.print(attribs.rel_alt);
		Serial.print(',');
		Serial.print(attribs.alt);
		Serial.print(',');
		Serial.print(attribs.roll);
		Serial.print(',');
		Serial.print(attribs.pitch);
		Serial.print(',');
		Serial.println(attribs.yaw);
	}
}
