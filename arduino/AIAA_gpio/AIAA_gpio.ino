#include <Mavlink.h>
 // #include <SoftwareSerial.h>

//#define rxPin 2
//#define txPin 4
//#define ledPin 13
//const unsigned TRIGGER_PIN = 2;
//bool trigger_state = 0;
Mavlink mav;


void setup() {

  MAVLINK_SERIAL.begin(57600);
  COMPUTER_SERIAL.begin(9600);  
  //Serial.begin(57600);
  while(!MAVLINK_SERIAL);
  //Serial1.begin(9600);
   while(!COMPUTER_SERIAL);
  pinMode(5,OUTPUT);
}


void loop() {
 

  if(MAVLINK_SERIAL.available()>0){
    //COMPUTER_SERIAL.println(MAVLINK_SERIAL.read());
    //COMPUTER_SERIAL.println("HELLO");
    MAVLINK_SERIAL.read();
    digitalWrite(5,HIGH);
    delay(2000);
  
  }
  digitalWrite(5,LOW);

  
  /*bool current_state = digitalRead(TRIGGER_PIN);
  if(current_state != trigger_state) {
    if ((trigger_state = current_state)) {
      Serial.println("Trigger OFF");
    }
    else {
      Serial.println("Trigger ON");
    }
  
  }*/

/*
  COMPUTER_SERIAL.println(mav.read());
  Mavlink::attributes flashAttribs = mav.getAttribs();
 
  COMPUTER_SERIAL.print("LAT = ");
  COMPUTER_SERIAL.println(flashAttribs.lat);
  COMPUTER_SERIAL.print("LON = ");
  COMPUTER_SERIAL.println(flashAttribs.lon);
  COMPUTER_SERIAL.print("ALT = ");
  COMPUTER_SERIAL.println(flashAttribs.alt);
  COMPUTER_SERIAL.print("ROLL = ");
  COMPUTER_SERIAL.println(flashAttribs.roll);
  COMPUTER_SERIAL.print("PITCH = ");
 COMPUTER_SERIAL.println(flashAttribs.pitch);
  COMPUTER_SERIAL.print("YAW = ");
  COMPUTER_SERIAL.println(flashAttribs.yaw);*/
  delay(2000);
}
