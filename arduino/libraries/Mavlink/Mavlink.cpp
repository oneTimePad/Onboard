#include "Mavlink.h"

Mavlink::Mavlink(HardwareSerial& serialPort){
	serial = &serialPort;
}

Mavlink::~Mavlink(){

}

int Mavlink::read(){
	if(serial->available()){
		uint8_t c = serial->read();
		if(mavlink_parse_char(MAVLINK_COMM_0, c, &msg, &stat)){
			switch(msg.msgid){
				case MAVLINK_MSG_ID_GLOBAL_POSITION_INT:{
					attribs.lat = mavlink_msg_global_position_int_get_lat(&msg);
					attribs.lon = mavlink_msg_global_position_int_get_lon(&msg);
					attribs.alt = mavlink_msg_global_position_int_get_alt(&msg);
				}break;
				case MAVLINK_MSG_ID_ATTITUDE:{
					attribs.roll = mavlink_msg_attitude_get_roll(&msg);
					attribs.pitch = mavlink_msg_attitude_get_pitch(&msg);
					attribs.yaw = mavlink_msg_attitude_get_yaw(&msg);
				}break;
				case MAVLINK_MSG_ID_ALTITUDE:{
					attribs.rel_alt = mavlink_msg_altitude_get_altitude_relative(&msg);
				}

							     
			}
		}
	}
	return 1;
}

Mavlink::attributes Mavlink::getAttribs(){
	return attribs; 
}
