# NJUPT-Dr-COM

author: KuroiGengetsu

Crawl teachers' accounts from our school network, who had left our school because their account havn't been removed.

I'll use scrapy to finish this.

That's all.

# 爬取校园网的账号密码(暴力方法)

主要是针对已经离校的老师的账号，以营造社团更好的网络环境(老师账号免费，而且已离校老师的账号不用的话很浪费)

## 实现

>python, scrapy 

原理就是通过给定的老师账号的格式，然后利用穷举法不断地向登录网站POST信息，检测跳转页面的内容，因为成功与不成功是有区别的，所以可以判断该密码和账号是否有效，如果有效，就储存起来。我们只针对那些平时不用校园网的老师并且最好是已经离校。
