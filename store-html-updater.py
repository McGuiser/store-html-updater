from __future__ import print_function
from bs4 import BeautifulSoup
from random import randint
import http.cookiejar
import requests
import urllib
import time
import sys
import re

login_url = 'http://www.neopets.com/login.phtml'
found_count = 0
login_attempt_count = 0

username = input('Username: ')
password = input('Password: ')

with requests.Session() as s:
    r = s.get(login_url)
    Text = r.content.decode()
    soup = BeautifulSoup(Text, 'html.parser')
    payload = {'destination': '', 'username': username, 'password': password}
    print('Logging in to the site.')
    r = s.post(login_url, data=payload)
    r = s.get('http://www.neopets.com/browseshop.phtml?owner=' + username)
    Text = r.content.decode()
    soup = BeautifulSoup(Text, 'html.parser')
    if str(soup.find(id="npanchor")) != 'None':
        neopoints = re.search(
            r'\>(.*?)\<', str(soup.find(id="npanchor"))).group(1)
        time_str = re.search(r'\>(.*?)\<', str(soup.find(id="nst"))).group(1)
        print(neopoints + ' ' + time_str)
        f = open('X:\\User\\Documents\\store-html-updater\\shop.html', 'w')
        f.write(str(r.content))
        f.close()

        for x in soup.find_all('a'):
            try:
                if 'Are you sure you wish to buy' in x['onclick']:
                    print(x['onclick'])
            except:pass
    else:
        print('Failed to log in.', flush=True)
