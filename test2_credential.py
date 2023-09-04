from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Carregue as informações de configuração do JSON
flow = InstalledAppFlow.from_client_secrets_file(
    '/Users/EJLXP/Documents/SmartHub/secret_gcp.json',
    scopes=['https://www.googleapis.com/auth/bigquery']
)

# Crie a URL de autorização manualmente
auth_url, _ = flow.authorization_url(prompt='consent')

# Imprima a URL de autorização e peça ao usuário para acessá-la em uma aba anônima
print('Acesse esta URL para autenticar:', auth_url)

# Após o usuário acessar a URL, eles receberão um código de autorização na barra de endereços
# Peça ao usuário para fornecer o código de autorização
authorization_code = input('Digite o código de autorização: ')

# Troque o código de autorização por credenciais de acesso
flow.fetch_token(authorization_response=authorization_code)

# Obtenha as credenciais de acesso
credentials = flow.credentials