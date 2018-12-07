# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 15:42:53 2018

@author: Arman
"""

import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os


url = r"http://libgen.io/search.php?req=game&open=0&res=25&view=simple&phrase=1&column=def"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
a_tag = soup.findAll("a")

#href = a_tag['href']

link = []
for a in a_tag:
    b = (a['href'])
    if 'php?id' in b:
        link += [b]


div_tag = []
n = []
for i in link:
    new_page = requests.get(i)
    new_soup = BeautifulSoup(new_page.text, 'lxml')
    div_tag = new_soup.find('div', {'class': 'book-info__download'})
    n += [div_tag.find('a')]

m = []
for k in n:
    c = k['href']
    m += ['https://libgen.pw' + c]


final_div = []
n2 = []
for q in m:
    new_page = requests.get(q)
    new_soup = BeautifulSoup(new_page.text, 'lxml')
    final_div = new_soup.find('div', {'class': 'book-info__get'})
    n2 += [final_div.find('a')]


m2 = []
for k2 in n2:
    c = k2['href']
    m2 += [c]

w = 0
for p in m2:
    f = open('Book' + str(w) + '.pdf', 'wb')
    f.write(requests.get("https://libgen.pw" + p).content)
    f.close()
    w += 1
