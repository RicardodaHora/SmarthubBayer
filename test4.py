#imports

import certifi_win32
from google_auth_oauthlib import flow
from google.cloud import storage

flow = flow.InstalledAppFlow.from_client_secrets_file(

                '/Users/EJLXP/Documents/SmartHub/secret_gcp.json', ['https://www.googleapis.com/auth/devstorage.read_write'])

credentials = flow.run_local_server(port=8080)

storage_client  = storage.Client(project="pbeat04042280-qa-4e56-smarthub", credentials=credentials)

print (storage_client.list_buckets())
