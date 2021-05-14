# -*- coding: utf-8 -*-
import scrapy


class CryptoSpider(scrapy.Spider):
    name = 'crypto'
    allowed_domains = ['https://goldprice.org/']
    start_urls = ['https://goldprice.org/cryptocurrency-price']

    def clean_names(self,name):
        return name.strip('\xa0')

    def parse(self, response):
        all_rows=response.xpath("//table[@class='views-table cols-8 table table-striped table-hover table-condensed table-0']/tbody/tr")
        for row in all_rows:
            crypto_name=self.clean_names(row.xpath(".//td[@class='views-field views-field-field-crypto-proper-name']/a/text()").get())
            market_cap=row.xpath("normalize-space(.//td[@class='views-field views-field-field-market-cap views-align-right hidden-xs']/text())").get()
            price=row.xpath("normalize-space(//td[@class='views-field views-field-field-crypto-price views-align-right']/text())").get()
            change=row.xpath("normalize-space(.//td[@class='views-field views-field-field-crypto-price-change-pc-24h views-align-right']/text())").get()
            yield{
                'CRYPTO NAME':crypto_name,
                'PRICE':price,
                'CHANGE(24h)':change,
                'MARKET CAP.':market_cap
            }
            

