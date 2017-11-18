# -*- coding: utf-8 -*-
"""crawl NJUPT teachers' accounts"""
import scrapy
from scrapy.http.cookies import CookieJar
from scrapy.utils.response import open_in_browser


class TeacherAccountSpider(scrapy.Spider):
    """crawl NJUPT teachers' accounts"""
    name = 'account'
    start_urls = ['http://192.168.168.168/0.htm']

    def parse(self, response):
        cookie_jar = CookieJar()
        yield scrapy.FormRequest.from_response(response=response,
                                               formdata={
                                                   # xxxx is year, xxx is random
                                                   'DDDDD': '10100xxxx0xxx00',  # username
                                                   'upass': 'password'  # password
                                               },
                                               meta={'cookieJar': cookie_jar._cookies},
                                               callback=self.after_login
                                               )

    @staticmethod
    def after_login(response):
        """check whether login successfully"""
        open_in_browser(response)
        status = response.xpath('//input/@value').extract()
        onload = response.xpath('//input/@value').extract()
        if status is None:
            print("\n\n\n\n\nget nothing\n\n\n\n\n")
        else:
            return {repr(status): repr(onload)}
