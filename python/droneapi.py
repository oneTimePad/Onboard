
import requests
import json
from droneapierror import DroneAPICallError,DroneAPIHTTPError
import base64

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

    def __init__(self):
        self.server_url = None
        self.username   = None
        self.password   = None
        self.access_token =None

    '''
    set django server url
    @server_url: http://url:port : string
    '''
    def setServer(self,server_url):
        self.server_url = server_url
    
    '''
    obtain access from imaging server [get token]
    @username: string
    @password : string
    '''
    def postAccess(self,username,password):
        self.username = username
        self.password = password
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
    post image information to imaging ground server
    @image: image to post
    @telemetry_data: data for geotagging image
    @time: time image was taken
    '''
    #should rename this at some point
    def postServerContact(image, telemetry_data,time):
        pass 
   