from google.cloud import storage
import pandas as pd

credentials_path = '/Users/EJLXP/Documents/SmartHub/secret_gcp.json'

client = storage.Client.from_service_account_json(credentials_path)

bucket_name = 'bra-pbeat04042280-qa-4e56-raw/fruit'

bucket = client.bucket(bucket_name)

blobs = bucket.list_blobs()

csv_blob = None
for blob in blobs:
    if blob.name.lower().endswith('.csv'):
        csv_blob = blob
        break

if csv_blob:
    try:
        csv_content = csv_blob.download_as_text()

        df = pd.read_csv(csv_content)

        df_head = df.head(5)
        print(df_head)

    except Exception as e:
        print("Erro:", e)
else:
    print("Nenhum arquivo CSV encontrado")