
import time
import os




class _Client(object):

    def __init__(self, url, username,password,timeout=5):
        self.url = url
        self.username = username
        self.password = password
        self.login()

    def pasrse_token(self,resp):
        token_resp = resp.json()
        token = token_resp['token']
        exp64 = token+="="*(4-len(token)%4)
        decoded = exp64.decode("base64")
        self.exp = json.loads(decoded.partition('}')[2].partition('}')[0]+'}')['exp']

        self.token = token_resp

    def login(self):
        resp = requests.post(self.url+'/drone/login',headers={'Content-Type': 'application/json; charset=UTF-8'},data=json.dumps({'password':self.password,'username':self.username}))
        if resp.status_code == 200:
            self.parse_token(resp)
        else:
            raise Exception(resp.status_code)

    def refresh(self):
        if long(self.exp)-long(time()) <= 3000:
            resp = requests.post(self.url+'/drone/refresh',headers={'Content-Type':'application/json; charset=UTF-8'},data=json.dumps({'token':self.token}))
            if resp.status_code == 400:
                self.login()
            else:
                self.parse_token(resp)
        
                
class _ImagePoller(object):
    def __init__(self, current_image_number, image_poll_directory):
        self.current_image_number = current_image_number
        self.image_poll_directory = image_poll_directory
        self.current_image_filepath = ""
        update_current_image_filepath()
    def update_current_image_filepath(self):
        current_image_filepath = image_poll_directory + "/capt" + str(current_image_number) + ".jpeg"
    def next_image_available(self):
        return os.path.isfile(current_image_filepath):
    def increment(self):
        current_image_number += 1
        update_current_image_filepath
    



class Client(object):
    def __init__(self,url,username,password, current_image_number=1, image_poll_directory, image_poll_delay):

        self.client = _Client(url,username,password)
        self.imagePoller = _ImagePoller(current_image_number, image_poll_directory)
        self.image_poll_delay = image_poll_delay
        self.executor = ThreadPoolExecutor(max_workers=workers)

    def post(self, image_filepath):
        #TODO implement
        
        #return True if post was successful, otherwise return False
        return False
    
    def run(self):
        while(True):
            if imagePoller.next_image_available() == True:
                image_filepath = imagePoller.current_image_filepath
                post_success = post(image_filepath)
                if post_success == True:
                    imagePoller.increment()
            else:
                time.sleep(image_poll_delay)
