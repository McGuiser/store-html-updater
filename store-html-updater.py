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

        item_count = 0
        table_string = '<table><tr>'
        for a in soup.find_all('a'):
            try:
                if 'Are you sure you wish to buy' in a['onclick']:
                    img_url = a.find_all('img')[0]['src']
                    obj_info_id = re.findall(r'obj_info_id=(\d+)&', a['href'])[0]
                    item_name_price = re.findall(r'Are you sure you wish to buy (.*?) at (.*?)\?', a['onclick'])
                    item_name = item_name_price[0][0]
                    item_price = item_name_price[0][1]
                    item_price_int = item_price.split()[0].replace(',', '')

                    if item_count == 4:
                        table_string += '</tr>'
                        item_count = 0

                    table_string += '<td class=\"item_cell\">'
                    table_string += '<a href=\"http://www.neopets.com/browseshop.phtml?owner=' + username + '&buy_obj_info_id=' + obj_info_id + '&buy_cost_neopoints=' + item_price_int + '\">'
                    table_string += '<img alt=\"' + item_name + '" src=\"' + img_url + '\">'
                    table_string += '<br> ' + item_name
                    table_string += '<br> ' + item_price
                    table_string += '</a></td>'
                    
                    item_count += 1

                    print(obj_info_id)
                    print(img_url)
                    print(item_name)
                    print(item_price)
            except:pass
        if item_count <= 4:
            table_string += '<td class=\"item_cell\"></td>'*(4-item_count)
        table_string += '</tr></table>'
        print(table_string)

        print()
        with open('X:\\User\\Documents\\store-html-updater\\first-half.txt', 'r') as myfile:
            first_half=myfile.read()
        with open('X:\\User\Documents\\store-html-updater\\second-half.txt', 'r') as myfile:
            second_half=myfile.read()
        with open('X:\\User\\Documents\\store-html-updater\\final.html', 'w') as myfile:
            myfile.write(first_half + table_string + second_half)

    else:
        print('Failed to log in.', flush=True)
