import scrapy
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from time import sleep
import time


class homePrice(scrapy.Spider):
    name = 'home'
    allowed_domains = ['divar.ir']
    start_urls = ['https://divar.ir/s/tehran/buy-apartment?price=20000000-']

    def parse(self, response):
        driver = webdriver.Firefox()
        driver.get(self.start_urls[0])
        # driver.set_script_timeout("3")

        SCROLL_PAUSE_TIME = 1

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")


        for i in range(1000):
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)


            # Calculate new scroll height and compare with last scroll height
            # new_height = driver.execute_script("return document.body.scrollHeight")
            # if new_height == last_height:
            #     break
            # last_height = new_height
            # sel = driver.page_source
            # selen = Selector(text=sel)
            #
            sele = driver.page_source
            selen = Selector(text=sele)
        # time.sleep(5)
        # driver.close()

        # ccss.css
        # for link in selen.css('.post-card-item.kt-col-6.kt-col-xxl-4 a::attr(href)'):
        #     yield {'html': link}
            for link in selen.css('.post-card-item.kt-col-6.kt-col-xxl-4 a::attr(href)'):
                yield response.follow(link.get(), callback=self.parse_news)

    def parse_news(self, response):
        # yield {
        #     'price': response.css('p.kt-unexpandable-row__value::text').get(),
        #     'price_one_meters': response.css('p.kt-unexpandable-row__value::text')[1].get()
        # }

        yield {
            'Title': response.css('.kt-page-title h1::text').get(),
            'Address': response.css('.kt-page-title__subtitle.kt-page-title__subtitle--responsive-sized::text').get(),
            'Area': response.css('.kt-group-row-item__value::text').get(),
            'Year': response.css('.kt-group-row-item__value::text')[1].get(),
            'Number Of Room': response.css('.kt-group-row-item__value::text')[2].get(),
            'Price': response.css('.kt-unexpandable-row__value::text').get(),
            'Price per meter': response.css('.kt-unexpandable-row__value::text')[1].get(),
            # 'Floor': response.css('.kt-unexpandable-row__value::text')[3].get(),
            'Elevator': response.css('span.kt-group-row-item__value.kt-body.kt-body--stable::text')[0].get(),
            'Parking': response.css('span.kt-group-row-item__value.kt-body.kt-body--stable::text')[1].get(),
            'Warehouse': response.css('span.kt-group-row-item__value.kt-body.kt-body--stable::text')[2].get(),
            'Time': response.css('.time::text').get()
        }
