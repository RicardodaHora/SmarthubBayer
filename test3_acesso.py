import requests

import certifi

certifi.where()


response = requests.get('https://urllib3.readthedocs.io/', verify='C:\\Users\\EJLZE\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\certifi\\cacert.pem').text

print(response)

 

 