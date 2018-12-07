# -*- coding: utf-8 -*-
from time import sleep
from selenium import webdriver
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException
import csv


def img_func(incoming_image_link):

    print("INCOMING LINK:", incoming_image_link)
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome('D:\\ArmanK\\chromedriver.exe', chrome_options=options)
    driver.get(incoming_image_link)

    sel = Selector(text=driver.page_source)

    links = []
    driver.get(incoming_image_link)
    sel2 = Selector(text=driver.page_source)
    img_link = sel2.xpath('//*[@class="_1Nyybr Yun65Y _30XEf0"]/@src').extract_first()
    links += [img_link]
    print("img_link:", img_link)
    return img_link


def get_link_func(incoming_spec_link):


    base_page = requests.get(incoming_spec_link)
    soup = BeautifulSoup(base_page.text, 'lxml')

    next_page_link = soup.find('a',{'class':'_3fVaIS'})
    next_page_link = "https://www.flipkart.com" + next_page_link['href']
    print("next_page_link:",next_page_link)
    

    products_link = soup.find_all("a", {'class':'_31qSD5'})
    #print("products_link",products_link)
    each_product_link = []
    for product in products_link:
        each_product_link += ["https://www.flipkart.com"+product['href']]
        
    #print("each_product_link",each_product_link)
    return each_product_link, next_page_link




def read_csv_link_file():
    with open('links2.csv', "r") as input:
        read = csv.reader(input, lineterminator='\n')
        count=0
        input_link = []
        for row in read:
            for row2 in row:
                #print(row2)
                count+=1
                input_link += [row2] 
    return input_link


def get_specs():
    all_links = read_csv_link_file()
    name_list = []
    price_list = []
    specs_list = []
    image_links_list = []
    link_to_page_list = []


    for link in all_links[501:1150]:
        individual_page = requests.get(link)
        soup = BeautifulSoup(individual_page.text, 'lxml')


        try:
            name_link = soup.find('span',{'class':'_35KyD6'})
            name = name_link.text
            name_list+=[name]
            #print(name)
        except:
            name_list+=["None"]

        try:       
            price_link = soup.find('div',{'class':'_1vC4OE _3qQ9m1'})
            price = price_link.text
            price_list+=[price]
        except:
            price_list+=["None"]

        try:
            specs_link = soup.find('div',{'class':'_3WHvuP'})
            specs = specs_link.findAll('li',{'class':'_2-riNZ'})
            specifications=''
            for i in specs:
                specifications+=i.text+' | '
            specs_list += [specifications]
        except:
            specs_list+=["None"]

              
        image_links_list += [img_func(link)]
        link_to_page_list += [link]
            #image_links_list+=["None"]

    return name_list, price_list, specs_list, image_links_list, link_to_page_list  


def write_specs():
    names, prices, specificationss, images, link_to_page = get_specs()
    print(names)
    print(specificationss)
    print(prices)
    print(images)
    print(link_to_page)
    print(len(names))
    print(len(specificationss))
    print(len(prices))
    print(len(images))
    print(len(link_to_page))


    csv = open('500FlipkartMobileData.csv', "a", encoding="utf-8") 
    columnTitleRow = "SrNo, name, price, specifications, imagesLink, linkToPage\n"
    csv.write(columnTitleRow)

    for i in range(len(names)):
        name = names[i].replace(',','_')
        price = prices[i].replace(',','_')
        specifications = specificationss[i].replace(',','_')
        imagesLink = images[i].replace(',','_')
        link_to_pages = link_to_page[i].replace(',','_')

        row = str(i+501) + "," + name + "," + price + "," + specifications + "," + imagesLink + "," + link_to_pages + "\n"
        csv.write(row)
    csv.close()

write_specs()






####### GOT LINKS AND SAVED IN CSV##########
"""
final_link_list = []
new_page_link = "https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=50"
for i in range(2,50):
    link, new_page_link = get_link_func(new_page_link)
    final_link_list+=[link]


print(new_page_link)
print("new_page_link",len(new_page_link))

print(final_link_list)
print("each_product_link",len(final_link_list))

with open('links.csv','w') as f:
    for sublist in final_link_list:
        for each_link in sublist:
            f.write(each_link + ',')
        f.write('\n')

with open('links2.csv', "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(final_link_list)

"""
