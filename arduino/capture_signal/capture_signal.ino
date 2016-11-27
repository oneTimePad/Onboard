const unsigned TRIGGER_PIN = 2;
bool trigger_state = 0;


void setup() {
	Serial.begin(9600);
	while(!Serial); // for arduino micro

    //attachInterrupt(digitalPinToInterrupt(TRIGGER_PIN),fct,FALLING);
      pinMode(TRIGGER_PIN,INPUT_PULLUP);

}


void loop() {



 
    
  bool current_state = digitalRead(TRIGGER_PIN);
  if(current_state != trigger_state) {
    if ((trigger_state = current_state)==LOW) {
        Serial.println("telemetry");
    }
    }

  
  
}
