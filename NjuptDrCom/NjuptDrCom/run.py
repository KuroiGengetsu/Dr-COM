#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""crawl NJUPT"""
import os
import sys
# using CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

try:
    from spiders.sasc import SascSpider
except ImportError:
    from NjuptDrCom.spiders.sasc import SascSpider


@defer.inlineCallbacks
def crawl(runner, usernames, passwords):
    for username in usernames:
        kwargs = {
            "username": username,
            'passwords': passwords
        }
        yield runner.crawl(SascSpider, **kwargs)
    try:
        reactor.stop()
    except AttributeError:
        raise AttributeError('reactor has no attribute stop(), maybe your "twisted" module ' +
                             'version is not right')

def main():
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    try:
        username_txt = open(path + '\\username.txt', 'r')
        password_txt = open(path + '\\password.txt', 'r')
        usernames = [s.replace('\n', '') for s in username_txt.readlines()]
        passwords = [s.replace('\n', '') for s in password_txt.readlines()]
    except FileNotFoundError:
        path = path.replace('\\spiders', '')
        username_txt = open(path + '\\username.txt', 'r')
        password_txt = open(path + '\\password.txt', 'r')
        usernames = [s.replace('\n', '') for s in username_txt.readlines()]
        passwords = [s.replace('\n', '') for s in password_txt.readlines()]
    except UnboundLocalError:
        raise UnboundLocalError('can\'t open file, ' +
            'check whether username.txt or password.txtis ' +
            'in your dictionary(NjuptDrCom/NjuptDrCom)')
    finally:
        username_txt.close()
        password_txt.close()

    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    crawl(runner, usernames, passwords)
    try:
        reactor.run()
    except AttributeError:
        raise AttributeError('reactor has no attribute stop(), maybe your "twisted" module ' +
                             'version is not right')

if __name__ == '__main__':
    main()
