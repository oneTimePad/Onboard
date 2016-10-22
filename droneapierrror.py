import requests


'''
exception for http errors from when droneapi makes http requests
'''
class DroneAPIHTTPError(requests.HTTPError):


	def __init__(self,response):    
        """
        Args:
            response: requests.Response object that indicated the error.
        """
        message = '{method} {url} -> {code} Error ({reason}): {message}'
        message = message.format(method=response.request.method,
                                 url=response.request.url,
                                 code=response.status_code,
                                 reason=response.reason,
                                 message=response.text)
	    self.code = response.status_code
	    self.reason= response.reason
	    self.text = response.text
        super(InteropError, self).__init__(message, response=response)

    def errorData(self):
        return (self.code,self.reason,self.text)


'''
exception from api call
'''
class DroneAPICallError(Exception):
        
        def __init__(self,endpoint,message):
            message = '{method} -> Error ({reason})'
            message = message.format(method = endpoint,
                                     reason = message)
            self.call = endpoint
            self.reason = message
            super(DroneAPICallError, self).__init__(message)
        def errorData(self):
            return (self.call,self.reason)


