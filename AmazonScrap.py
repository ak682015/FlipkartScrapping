from bs4 import BeautifulSoup
import requests
import csv
import time
import gc



# div class : a-section a-spacing-none a-inline-block s-position-relative
    # a class : a-link-normal a-text-normal ........href
    # img source  




def get_link_of_phone(url):
    
    page = requests.get(url)

    soup = BeautifulSoup(page.text,'lxml')

    next_page_link = soup.find('a',{'class':'pagnNext'})
    next_page_link = "https://www.amazon.in" + next_page_link['href']
    print("next_page_link:",next_page_link)

    div = soup.find_all('div',{'class':'a-section a-spacing-none a-inline-block s-position-relative'})
    phone_link = soup.find_all('a',{'class':'a-link-normal a-text-normal'})

    each_phone_links = []
    for i,each in enumerate(phone_link):
        if(i%2==0):
            each_phone_links+=[each['href']]
            
    return each_phone_links, next_page_link



def read_csv_link_file():
    with open('Amazonlinks.csv', "r") as input:
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
    link_to_page_list = []
    count = 1

    for link in all_links[0:2000]:

        result = False
        while(result==False):
            try:
                individual_page = requests.get(link)
                soup = BeautifulSoup(individual_page.text, 'lxml')
                name_link = soup.find('span',{'id':'productTitle'})
                name = name_link.text.replace('\n','').replace('  ','')
                name_list+=[name]
                print(count,":",name)
                result = True
            except:
                result = False
                #gc.collect()
                #name_list+=["None"]
                #print("None")

        try:       
            price_link = soup.find('span',{'id':'priceblock_ourprice'})
            price = price_link.text
            price_list+=[price]
            print(price)
        except:
            price_list+=["Currently Unavailable"]
            print("PRICE NOT")

        """
        try:
            specs_link = soup.findAll('ul',{'class':'a-unordered-list a-vertical a-spacing-none'})[2]
            specs = specs_link.findAll('span',{'class':'a-list-item'})
            specifications=''
            for i in specs:
                specifications+=i.text+' | '    
            specs_list += [specifications.replace('\t', '').replace('\n', "").replace(',','  ')]
        except:
            specs_list+=["None"]
        
        """

        """  
        try:
            div = soup.find('img',{'class':'a-dynamic-image a-stretch-vertical'})
            img_link= div['data-a-dynamic-image']    
            image_links_list += [img_link]
            #image_links_list+=["None"]
        except:
            image_links_list+=['None']
        """ 
        link_to_page_list += [link]
        count+=1
    
    return name_list, price_list, link_to_page_list  


def write_specs():
    names, prices, link_to_page = get_specs()
    # print(names)
    # print(specificationss)
    # print(prices)
    # print(images)
    print(len(names))
    print(len(prices))
    print(len(link_to_page))


    csv = open('AGAINAMAZONMobileData.csv', "w", encoding="utf-8") 
    columnTitleRow = "SrNo, name, price, linkToPage\n"
    csv.write(columnTitleRow)

    for i in range(len(names)):
        name = names[i].replace(',','_')
        price = prices[i].replace(',','_')
        link_to_pages = link_to_page[i].replace(',','_')

        row = str(i+1) + "," + name + "," + price + "," + link_to_pages + "\n"
        csv.write(row)
    csv.close()

write_specs()


### GOT ALL LINKS ######
# final_link_list = []
# new_page_link = "https://www.amazon.in/Smartphones-Basic-Mobiles-Accessories/s?ie=UTF8&page=1&rh=n%3A1389432031"
# for i in range(2,150):
#     link, new_page_link = get_link_of_phone(new_page_link)
#     final_link_list+=[link]


# print(new_page_link)
# print("new_page_link",len(new_page_link))

# print(final_link_list)
# print("each_product_link",len(final_link_list))


# with open('Amazonlinks.csv', "w") as output:
#     writer = csv.writer(output, lineterminator='\n')
#     writer.writerows(final_link_list)