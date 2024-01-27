import google.auth

credentials, projectid = google.auth.load_credentials_from_file("/home/charlesdupont/Desktop/homeseeker.json")

n = credentials.__dict__
f = projectid

print(n)
print(f" Something {f}")
