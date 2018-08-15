# -*- coding: utf-8 -*-
from time import sleep

from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException


class BooksSpider(Spider):
    name = 'img_flip'
    # llowed_domains = ['books.toscrape.com']

    def fun(self, link):
        yield{
            'img': link
        }

    def start_requests(self):
        self.driver = webdriver.Chrome('D:\\ArmanK\\chromedriver.exe')
        self.driver.get('https://www.flipkart.com/search?q=phones&marketplace=FLIPKART&otracker=start&as-show=on&as=off&page=3')

        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//*[@class="_31qSD5"]/@href').extract()

        links = []
        for book in books:
            absolute_url = "https://www.flipkart.com" + book
            # yield Request(absolute_url, callback=self.parse_book)
            self.driver.get(absolute_url)
            sel2 = Selector(text=self.driver.page_source)
            img_link = sel2.xpath('//*[@class="_1Nyybr Yun65Y _30XEf0"]/@src').extract_first()
            links += [img_link]
            print(links)

            fun(img_link)

        # while True:
        #     try:
        #         next_page = self.driver.find_element_by_xpath('//*[@class="_3fVaIS"]/@href')
        #         sleep(3)
        #         self.logger.info('Sleeping for 3 seconds.')
        #         next_page.click()

        #         sel = Selector(text=self.driver.page_source)
        #         books = sel.xpath('//*[@class="_31qSD5"]/@href').extract()
        #         for book in books:
        #             absolute_url = "https://www.flipkart.com" + book
        #             yield Request(absolute_url, callback=self.parse_book)

        #     except NoSuchElementException:
        #         self.logger.info('No more pages to load.')
        #         self.driver.quit()
        #         break

    # def parse_book(self, absolute_url):
    #     print("response\n\n\n\n\n", absolute_url)
    #     self.driver.get(absolute_url)
    #     sel2 = Selector(text=self.driver.page_source)
    #     img_link = sel2.xpath('//*[@class="_1Nyybr Yun65Y  _30XEf0"]/@src()').extract_first()
    #     yield{
    #         'img': img_link
    #     }
