class BlazeBaseException(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(self.message)
    
        
    def __str__(self):
        return f"\033[91m{self.message}"

     
class BlazeAuthenticationException(BlazeBaseException):
    pass
        
        