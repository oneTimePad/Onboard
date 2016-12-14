from droneapi import DroneAPI


SERVER_URL = "http://127.0.0.1:8000"
USERNAME = "drone"
PASSWORD = "ruautonomous"

api  = DroneAPI(SERVER_URL, USERNAME, PASSWORD)


api.postAccess()
api.postHeartbeat()


