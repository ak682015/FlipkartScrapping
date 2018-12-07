# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 15:42:53 2018

@author: Arman
"""

import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os

#name_of_topic = input("Enter the Topic: ")
main_url = r"http://libgen.io/search.php?req=Machine-Learning&open=0&res=25&view=simple&phrase=1&column=def"
main_page = requests.get(main_url)
soup = BeautifulSoup(main_page.text, 'lxml')
a_tag = soup.findAll("a")

#href = a_tag['href']

first_link = []
for a in a_tag:
    b = (a['href'])
    if 'php?id' in b:
        first_link+=[b]
        

div_tag=[]
second_link = []
for i in first_link:
    second_page = requests.get(i)
    second_soup = BeautifulSoup(second_page.text,'lxml')
    div_tag = second_soup.find('div',{'class':'book-info__download'})
    second_link += [div_tag.find('a')]

final_second_link = []
for k in second_link:
    c = k['href']
    final_second_link += ['https://libgen.pw'+ c]
    

final_div = []
third_link = []
for q in final_second_link:
    third_page = requests.get(q)
    third_soup = BeautifulSoup(third_page.text,'lxml')
    final_div = third_soup.find('div',{'class':'book-info__get'})
    third_link += [final_div.find('a')]
    

final_third_link = []
for k2 in third_link:
    c = k2['href']
    final_third_link += [c]
    
name=0
for p in final_third_link:
    f = open('Book'+str(name)+'.pdf','wb')
    f.write(requests.get("https://libgen.pw"+p).content)
    f.close()
    name+=1
    
