from droneapi import  DroneAPI
img_filepath="/home/lie/capt1.jpeg"


drone_api = DroneAPI("http://localhost:8443","drone","ruautonomous")
logged_in = False
while logged_in == False:
	try:
		drone_api.postAccess()
		logged_in = True
	except TypeError:
		pass
	except DroneAPICallError as e:
		print e
print "DEBUG:" + "logged in"



resp = drone_api.postImage(img_filepath,"")
while True:
	pass
print resp
