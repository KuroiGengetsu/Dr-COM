# -*- coding: utf-8 -*-
import scrapy


class DrComItem(scrapy.Item):
    """items for username and password"""
    username = scrapy.Field()
    password = scrapy.Field()
