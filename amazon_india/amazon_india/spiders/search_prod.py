# -*- coding: utf-8 -*-
import scrapy
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
import time

class SearchProdSpider(scrapy.Spider):
    name = 'search_prod'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.amazon.in",
            wait_time=3,
            screenshot=True,
            callback=self.selenium_tasks
        )

    def selenium_tasks(self,response):
        driver=response.meta['driver']
        srch_bar=driver.find_element_by_xpath("//input[@id='twotabsearchtextbox']")
        srch_bar.send_keys("Laptop") #SEARCH LAPTOP
        srch_bar.send_keys(Keys.ENTER) #PRESS ENTER
        time.sleep(5) #wait for site to load

        yield SeleniumRequest(
            url=driver.current_url,
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        all_items=response.xpath("//div[@class='sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20']/div")
        for item in all_items:
    
                prod_link=item.xpath(".//div[@class='a-section a-spacing-none']/h2/a/@href").get()
                prod_name=item.xpath(".//div[@class='a-section a-spacing-none']/h2/a/span/text()").get()
                prod_rating=item.xpath("(.//div[@class='a-section a-spacing-none a-spacing-top-micro']/div/span)[1]/@aria-label").get()
                prod_price=item.xpath(".//div[@class='a-section a-spacing-none a-spacing-top-small']/div[@class='a-row a-size-base a-color-base']/a/span[@class='a-price']/span/text()").get()

                yield{
                    'prod_name':prod_name,
                    'prod_rating':prod_rating,
                    'prod_price':prod_price,
                    'prod_link':f'https://www.amazon.in{prod_link}'
                }
        
        nxt_btn=response.xpath("//li[@class='a-last']/a/@href").get()
        if nxt_btn:
            nxt_link=f'https://www.amazon.in{nxt_btn}'
            yield SeleniumRequest(
            url=nxt_link,
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )
        