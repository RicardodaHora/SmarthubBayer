from google_auth_oauthlib import flow

flow = flow.InstalledAppFlow.from_client_secrets_file(

                '/Users/EJLXP/Documents/SmartHub/secret_gcp.json', ['https://www.googleapis.com/auth/bigquery'])

credentials = flow.run_local_server(port=8080)