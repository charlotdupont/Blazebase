import json
import os

import firebase_admin as fb
import firebase_admin.auth as fba
import requests
from requests_toolbelt.adapters import appengine

try:
    import blazebase.exceptions as exc
except Exception:
    import exceptions as exc


def initialize_app(config):
    return BlazeBase(config)

class BlazeBase:
    
    def __init__(self, config):
        self.api_key = config.get("apiKey")
        self.requests = requests.Session()
                
        try:                                                                                                
            credentials = fb.credentials.Certificate(config.get("serviceAccount", None))
            self.app = fb.initialize_app(credential=credentials, options={
                "databaseURL": config.get("databaseURL", None),
                "storageBucket": config.get("storageBucket", None), 
                "projectId": config.get("projectId", None), 
                "databaseAuthVariableOverride": config.get("databaseAuthVariableOverride", None),
                "serviceAccountId": config.get("serviceAccountId", None),
                "httpTimeout": config.get("httpTimeout", None)
                })
        except Exception as e:
            raise exc.BlazeAuthenticationException(f"Could not authenticate the service account: {e}")
        
        
        if os.getenv("GAE_ENV", "").startswith("standard"):
            # Production in the standard env
            adapter = appengine.AppEngineAdapter(max_retries=3)
        else:
            # Local execution
            adapter = requests.adapters.HTTPAdapter(max_retries=3)
        for scheme in ('http://', 'https://'):
            self.requests.mount(scheme, adapter)

    
    def auth(self):
        return BlazeAuth(app=self.app, api_key=self.api_key, request=self.requests)
    
    def database(self):
        return BlazeDatabase()
    
    def storage(self):
        return BlazeStorage()
        
class BlazeAuth:
    
    def __init__(self, app, api_key, request):
        self.app = app
        self.api_key = api_key
        self.requests = request
    
    def verify_user_token(self, user_token):
        try:
            decoded_token = fba.verify_id_token(id_token=user_token, app=self.app, check_revoked=True)
            uid = decoded_token["uid"]
            return uid
        except Exception as e:
            raise exc.BlazeAuthenticationException(f"Could not verify token: {e}.")
        
    def sign_in_with_email_and_password(self, email, password):
        request_ref = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={0}".format(self.api_key)
        headers = {'Content-Type: application/json'}
        data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
        request_object = self.requests.post(request_ref, headers=headers, data=data)
        
        self.current_user = request_object.json()
        return request_object.json()
        

class BlazeDatabase():
    pass


class BlazeStorage():
    pass
