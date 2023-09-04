[3:08 PM] Luis Damo

 

import requests

import certifi

from google_auth_oauthlib import flow

 

certifi.where()

 

http_proxy = "http://10.185.190.100:8080"

https_proxy = "https://10.185.190.100:8080"

ftp_proxy = "10.185.190.100:8080"

 

proxies = {

"http" : http_proxy,

"https" : https_proxy,

"ftp" : ftp_proxy

}

 

response = requests.get('https://www.google.com/', verify='C:\\Users\\EJLZE\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\certifi\\cacert.pem', proxies=proxies).text

print(response)