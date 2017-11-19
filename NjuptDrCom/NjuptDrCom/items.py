# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NjuptDrComItem(scrapy.Item):
    """items for username and password"""
    username = scrapy.Field()
    password = scrapy.Field()
