#ifndef MAVLINK_WRAP_H
#define MAVLINK_WRAP_H

#include <Arduino.h>
#include "ardupilotmega/mavlink.h"

class Mavlink{
public:
	typedef struct attributes{
		long lat; //latitude * 1e7
		long lon; //longitude * e17
		long rel_alt; //relative altitude in millimeters
		float roll; //roll in radians
		float pitch; //pitch in radians
		float yaw; //yaw in radians
	};

	Mavlink(HardwareSerial& serialPort);
	~Mavlink();
	int read();
	attributes getAttribs();

private:
	mavlink_message_t msg;
	mavlink_status_t stat;
	HardwareSerial *serial;
	attributes attribs;
};

#endif