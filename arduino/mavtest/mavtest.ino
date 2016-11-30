#include <Mavlink.h>


Mavlink mav(Serial1);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  Serial1.begin(57600);
}

void loop() {
  // put your main code here, to run repeatedly:
mav.read();
Mavlink::attributes attribs = mav.getAttribs();
  Serial.print("   Lat: "); Serial.print(attribs.lat);
  Serial.print("   Lon: "); Serial.print(attribs.lon);
  Serial.print("   Rel Alt: "); Serial.print(attribs.alt);
  Serial.print("   Roll: "); Serial.print(attribs.roll);
  Serial.print("   Pitch: "); Serial.print(attribs.pitch);
  Serial.print("   Yaw: "); Serial.println(attribs.yaw);
 // Serial.println("------------------");
 // Serial.println(Serial1.read());
//delay(2000);
}
