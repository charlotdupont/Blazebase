
import exceptions as exc
import firebase_admin as fb
import google.auth


def initialize_app(config):
    return BlazeBase(config)


default_scopes = [
    'https://www.googleapis.com/auth/firebase',
    'https://www.googleapis.com/auth/cloud-platform'
]

class BlazeBase:
    
    def __init__(self, config):
        self.database_url = config.get("databaseURL", None) # https://databaseName.firebaseio.com
        self.storage_bucket = config.get("storageBucket", None) # projectId.appspot.com
        self.scopes = config.get("scopes", default_scopes) # Allows user to customize the scopes
        self.quota_project_id = config.get("quota_project_id", None)
        self.credentials = None
        
        if config.get("serviceAccount"):
            try:
                service_account_type = type(config["serviceAccount"])
                if service_account_type is str:
                    self.crentials = google.auth.load_credentials_from_file(config["serviceAccount"], scopes=self.scopes, quota_project_id=self.quota_project_id)
                    self.app = fb.initialize_app(credential=self.credentials, databaseURL=self.database_url, storageBucket=self.storage_bucket)
                if service_account_type is dict:
                    self.credentials = google.auth.load_credentials_from_dict(config["serviceAccount"], scopes=self.scopes)
                    self.app = fb.initialize_app(self.credentials, databaseURL=self.database_url, storageBucket=self.storage_bucket)
            except Exception as e:
                raise exc.BlazeAuthenticationException(f'Could not create the credentials for: "{config["serviceAccount"]}" because {e}| HINT: Ensure it is a dict or a path and that it is valid.') 
        else:
            self.app = fb.initialize_app(credential=None, databaseURL=self.database_url, storageBucket=self.storage_bucket)    
    
    def auth(self):
        return BlazeAuth(app=self.app)
    
    def database(self):
        return BlazeDatabase()
    
    def storage(self):
        return BlazeStorage()
        
class BlazeAuth:
    
    def __init__(self, app):
        self.app = app
    
    def verify_user_token(self, user_token):
        try:
            decoded_token = self.app.verify_id_token(user_token, check_revoked=True)
            uid = decoded_token["uid"]
            return uid
        except Exception as e:
            raise exc.BlazeAuthenticationException(f"Could not verify {user_token} because {e}.")
        

class BlazeDatabase():
    pass


class BlazeStorage():
    pass

        
        
blazeTest = BlazeBase(config = {"serviceAccount": "/home/charlesdupont/Desktop/homeseeker.json"})

testAuth = blazeTest.auth()
testAuth.verify_user_token("This")
