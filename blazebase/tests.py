import firebase_admin as fb

test = "/home/charlesdupont/Desktop/Blazebase/firebase_account.json"


cred = fb.credentials.Certificate(test)


app = fb.initialize_app(credential=cred)

print(app)