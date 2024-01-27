
import exceptions as exc
import firebase_admin as fb
import firebase_admin.auth as fba


def initialize_app(config):
    return BlazeBase(config)


default_scopes = [
    'https://www.googleapis.com/auth/firebase',
    'https://www.googleapis.com/auth/cloud-platform'
]

class BlazeBase:
    
    def __init__(self, config):
                
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
            decoded_token = fba.verify_id_token(id_token=user_token, app=self.app, check_revoked=True)
            uid = decoded_token["uid"]
            return uid
        except Exception as e:
            raise exc.BlazeAuthenticationException(f"Could not verify token: {e}.")
        

class BlazeDatabase():
    pass


class BlazeStorage():
    pass

        
        
blazeTest = BlazeBase(config = {"serviceAccount": "/home/charlesdupont/Desktop/Blazebase/admin_service_account.json"})

testAuth = blazeTest.auth()

print(testAuth.verify_user_token("eyJhbGciOiJSUzI1NiIsImtpZCI6IjY5NjI5NzU5NmJiNWQ4N2NjOTc2Y2E2YmY0Mzc3NGE3YWE5OTMxMjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vaG9tZXNlZWtlci12LWR1cG9udCIsImF1ZCI6ImhvbWVzZWVrZXItdi1kdXBvbnQiLCJhdXRoX3RpbWUiOjE3MDYzMjEzNzcsInVzZXJfaWQiOiJNWWs2c3JpWktXYnlUWTludGdsSW9pMmN4TkYyIiwic3ViIjoiTVlrNnNyaVpLV2J5VFk5bnRnbElvaTJjeE5GMiIsImlhdCI6MTcwNjMyMTM3NywiZXhwIjoxNzA2MzI0OTc3LCJlbWFpbCI6ImNoYXJsby5kdXBvbnRAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImNoYXJsby5kdXBvbnRAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.dMlB7JZ14cNbChh2Bz3JFESQpWqpqBNDwiOLsZFF6O-g3uvSCRqo-zYN4SMX1FYMglN9-Lx4DZre97aF4w1caRjCJ4jUoMXIQ_BPcIlc5qsf9kUG9Z39kBjp1O7gdmWAIFaxyHRgyqN3tqbBDrpX-zeEFn_LBkpmPj-5M_4v4ChtMI80bfTbm8-lHoyvKznMw9a911pVGBH8DrC_BkUhjhYj9wI_kdHrFS6XNsNHOAQYtbnBqb_XHQ3uL6nttKG8o8irq0iUXsk81_mEnZrFkr3llKfPO851Za6uWPyWnAe8fuzX1xFfDlytxWzcRlE4e7yJbdd1B05dlSk_m5TEzw"))