import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('/Users/zhuobiaocai/Desktop/biology-review/firebase_key.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()