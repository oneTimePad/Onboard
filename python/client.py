





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



class Client(object):
    def __init__(self,url,username,password):

        self.client = _Client(url,username,password)
        self.executor = ThreadPoolExecutor(max_workers=workers)

    def 
