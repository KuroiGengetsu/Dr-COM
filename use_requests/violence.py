import requests
from scrapy import Selector


def get_requests(params=None):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.8',
        'user-agent': 'Chrome/61.0.3163.100 Mozilla/5.0 (Windows NT 6.3) \
        AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 '
    }
    r = requests.post(url="http://192.168.168.168/0.htm", data=params, headers=headers)
    r.encoding = 'GB2312'
    return r.text


if __name__ == '__main__':
    username = '110020160286000'
    password = '233415'
    param = {
        'DDDDD': username,
        'upass': password
        }
    text = get_requests(params=param)
    sel = Selector(text=text, type='html')
    status = sel.xpath('//input/@value').extract()
    result = ''.join(map(str, status))
    if '\u8fd4' in result:
        print(text)
        print('返回')
    elif result == "":
        item = {}
        item['username'] = username
        item['password'] = password
        print(item)
    else:
        print({'what is this?': 'Ohhhhhhhhhh'})
