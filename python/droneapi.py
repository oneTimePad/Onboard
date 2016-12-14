
import requests
import json
from droneapierror import DroneAPICallError,DroneAPIHTTPError
import base64
import datetime

'''
contains information for access token
'''
class DroneAPIToken:

    def __init__(self,token_response):
        token = token_response['token']
        token_b64 = token + "="* (4-len(token)%4)
        decoded_token = str(base64.b64decode(token_b64))
        self.expiration = json.loads(decoded_token.partition('}')[2].partition('}')[0]+"}")['exp']
        self.token = token
           

    def getToken(self):
        return self.token

    def getExpiration(self):
        return long(self.expiration)

    #appended to headers list when accessing api
    #returned as tuple (authorization_header,token)
    def toAuthorization(self):
        return ('Authorization','JWT ' + self.token)

'''
exports remote ground imagin station api
'''
class  DroneAPI:

    def __init__(self, server_url, username, password):
        self.server_url = server_url
        self.username   = username
        self.password   = password
        self.access_token =None

    '''
    set django server url
    @server_url: http://url:port : string
    '''
        
    def setAccessToken(self, access_token_as_text):
        self.access_token = DroneAPIToken({'token': access_token_as_text})
    
    '''
    obtain access from imaging server [get token]
    @username: string
    @password : string
    '''
    def postAccess(self):
        if self.server_url  is None:
            raise DroneAPICallError('getAccess','server url specified')
        headers = {'Content-Type':'application/json; charset=UTF-8'}
        data    = {'password': self.password, 'username': self.username}
        endpoint = self.server_url +'/drone/login'
        resp = requests.post(endpoint,headers=headers,data=json.dumps(data))

        if resp.status_code == 200:
            self.access_token = DroneAPIToken(resp.json())
        else:
            raise DroneAPIHTTPError(resp)
    '''
    refresh current token before expires
    '''
    def postRefresh(self):
        token = self.access_token
        if  token.getExpiration() - long(time()) <= EXP_TIME:
            headers = {'Content-Type': 'application/json; charset=UTF-8'}
            data    = {'token': token.getToken()}
            resp = requests.post(self.url + '/drone/refresh',headers=headers,data=data)
            if resp.status_code == 400:
                self.postAccess(self.username, self.password)
            elif resp.status_code == 200:
                self.access_token = DroneAPItoken(resp.json())
            else:
                raise DroneAPIHTTPException(resp)
                
                
    '''
    post a heartbeat message to the ground station, return the response
    '''
    def postHeartbeat(self):
        #server_url must be set before attempting to post anything!
        if self.server_url  is None:
            raise DroneAPICallError('getAccess','server url specified')
            
        # put metadata + token into the header, im not sure if i did that correctly
        token_label, token_value = self.access_token.toAuthorization()
        headers = {'Content-Type':'application/json; charset=UTF-8', token_label: token_value}
        # write the binary data from the file to the request
        data = {'post_timestamp': str(datetime.datetime.now())}
        endpoint = self.server_url +'/drone/postHeartbeat'
        
        #send the post request
        resp = requests.post(endpoint, headers=headers, data=json.dumps(data))
        
        return resp
    


    '''
    post image to imaging ground server
    @image: filepath of image to post, image should already be geotagged and timetagged
    returns the response
    '''
    def postImage(self, image_filepath, telemetry_filepath):
        
        #server_url must be set before attempting to post anything!
        if self.server_url  is None:
            raise DroneAPICallError('getAccess','server url specified')
            
        # put metadata + token into the header, im not sure if i did that correctly
        token_label, token_value = self.access_token.toAuthorization()
        headers = {token_label: token_value}
        # write the binary data from the file to the request
        files = {'image': open(image_filepath, "rb"), 'pitch': (None, "5"), 'roll': (None, "5"), 'lat': (None, "5"), 'lon': (None, "5"), 'alt': (None, "5"), 'yaw': (None, "5")}
        endpoint = self.server_url +'/drone/postImage'
        
        #send the post request
        resp = requests.post(endpoint, headers=headers, files=files)
        
        #return the response
        return resp
        
         
        
        
   
