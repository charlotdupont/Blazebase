import firebase_admin as fba
import requests

from google.oauth2 import service_account


import exceptions as exc

def initialize_app(config):
    return BlazeBase(config)


class BlazeBase:
    
    def __init__(self, config, scopes=None):
        
        self.api_key = config["apiKey"]
        self.auth_domain = config["authDomain"] # projectId.firebaseapp.com
        self.database_url = config["databaseURL"] # https://databaseName.firebaseio.com
        self.storage_bucket = config["storageBucket"] # projectId.appspot.com
        
        self.requests = requests.Session()
        
        if config.get("project_id"):
            self.project_id = config["project_id"]
        
        
        if scopes:
            pass
        
        if not scopes:
            pass
        