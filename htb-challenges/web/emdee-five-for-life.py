# Challenge: Emdee Five For Life
# https://app.hackthebox.eu/challenges/emdee-five-for-life

import requests
from bs4 import BeautifulSoup
import hashlib

URL = "http://xxx.xxx.xxx.xxx:xxxx"
cookies = {'PHPSESSID': 'xxx'}

page = requests.get(URL, cookies=cookies)
soup = BeautifulSoup(page.content, "html.parser")
string = soup.find('h3').text

print("String: " + string)

md5string = hashlib.md5(string.encode())

print("MD5 Hash: " + md5string.hexdigest())

myobj = {'hash': md5string.hexdigest()}

x = requests.post(URL, data = myobj, cookies=cookies)
soup = BeautifulSoup(x.content, "html.parser")

print(soup.find('p').text)