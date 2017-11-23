#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""crawl Dr-Com"""
import json

# using CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
try:
    from spiders.sasc import SascSpider
except ImportError:
    pass

@defer.inlineCallbacks
def crawl(runner, usernames, passwords):
    """Pass arguments to spiders"""
    for username in usernames:
        kwargs = {
            "username": username,
            'passwords': passwords
        }
        yield runner.crawl(SascSpider, **kwargs)
    try:
        # stop all the spiders
        reactor.stop()
    except AttributeError:
        raise AttributeError('reactor has no attribute stop(), maybe your "twisted" module ' +
                             'version is not right')


def main():
    """Open filename.txt and password.txt to load info"""
    try:
        with open('usernames.json') as fp:
            usernames = iter(json.load(fp))
        with open('passwords.json') as fp:
            passwords = iter(json.load(fp))
    except FileNotFoundError as err:
        print(err)

    # You must instance an CrawlerRunner with the Settings object:
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)

    # 1. To crawl default password `123456` using this:
    # crawl(runner, usernames, ['123456'])
    crawl(runner, ['110020160286000'], [str(i) for i in range(233000, 233450)])

    # 2. To crawl 000000 to 999999 except 123456 using this:
    # crawl(runner, usernames, passwords)

    try:
        reactor.run()  # run the spiders
    except AttributeError:
        raise AttributeError('reactor has no attribute stop(), maybe your "twisted" module ' +
                             'version is not right')


if __name__ == '__main__':
    main()
