# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
# from scrapy.conf import settings
# settings.overrides['DEPTH_LIMIT'] = 20


# def product_info(response, value):
#     return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()


class FlipSpider(Spider):
    name = 'flip'
    #allowed_domains = ['https://www.flipkart.com/']
    start_urls = ['https://www.flipkart.com/search?q=phone&marketplace=FLIPKART&otracker=start&as-show=on&as=off&page=50']

    def parse(self, response):
        products = response.xpath('//*[@class="_31qSD5"]/@href').extract()
        for product in products:
            absolute_url = response.urljoin(product)
            yield Request(absolute_url, callback=self.parse_book)

        # process next page
        next_page_url = response.xpath('//*[@class="_3fVaIS"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)

    def parse_book(self, response):
        title = response.xpath('//*[@class="_35KyD6"]/text()').extract_first()
        price = response.xpath('//*[@class="_1vC4OE _3qQ9m1"]/text()').extract_first()

        #image_url = response.xpath('//img/@src').extract_first()
        #image_url = image_url.replace('../..', 'http://books.toscrape.com/')

        rating = response.xpath('//*[@class="hGSR34 _2beYZw"]/text()').extract_first()

        specs = response.xpath('//*[@class="_2-riNZ"]/text()').extract()
        strspecs = ""
        for spec in specs:
            strspecs += str(spec) + '\n'

        # product information data points
        # upc = product_info(response, 'UPC')
        # product_type = product_info(response, 'Product Type')
        # price_without_tax = product_info(response, 'Price (excl. tax)')
        # price_with_tax = product_info(response, 'Price (incl. tax)')
        # tax = product_info(response, 'Tax')
        # availability = product_info(response, 'Availability')
        # number_of_reviews = product_info(response, 'Number of reviews')

        yield {
            'title': title,
            'price': str(price),
            'specs': strspecs,
            'rating': rating
        }
