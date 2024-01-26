import exceptions as exc
import requests


def initialize_app(config):
    return BlazeBase(config)


default_scopes = [
    'https://www.googleapis.com/auth/firebase',
    'https://www.googleapis.com/auth/cloud-platform'
]

class BlazeBase:
    
    def __init__(self, config):
        
        self.api_key = config.get("apiKey", None)
        self.auth_domain = config.get("authDomain", None) # projectId.firebaseapp.com
        self.database_url = config.get("databaseURL", None) # https://databaseName.firebaseio.com
        self.storage_bucket = config.get("storageBucket", None) # projectId.appspot.com
        self.scopes = config.get("scopes", default_scopes) # Allows user to customize the scopes

        self.service_account_path = config.get("service_account_path", None)
        self.service_account_info = config.get("service_account_info", None)

        self.requests = requests.Session()
        
        try:   
            if self.service_account_info is None and self.service_account_path is None:
                raise exc.BlazeAuthenticationException("Must provide the service account path or the service account information as a dictionary.")
            if self.service_account_info and self.service_account_path:
                raise exc.BlazeAuthenticationException("You can only provide a service account path or the account information.")
            
        except Exception as e:
            raise exc.BlazeAuthenticationException(f"Error with the authentication process: {e}")
    
    def auth(self):
        pass
    
    def database(self):
        pass
    
    def storage(self):
        pass
        
class BlazeAuth:
    pass
        
        
        
        
blazeTest = BlazeBase(config = {"service_account_path": "something"})