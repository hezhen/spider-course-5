# -*- coding: utf-8 -*-

import requests
from lxml import html
from lxml import etree


user_review_home = 'http://www.mafengwo.cn/u/%d/review.html'

user_id = 129914

url = user_review_home % (user_id)

print(url)

headers = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'x-requested-with': "XMLHttpRequest",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'cache-control': "no-cache"
}

r = requests.get(url, headers = headers )

tree = etree.HTML(r.text)

with open('mfw_userinfo_%d.html' % (user_id), 'w+') as f:
	f.write(r.text)

print( '')
print( 'User Name: ', tree.xpath(u"//*[@class='MAvaName']")[0].text)

print( 'Level: ', tree.xpath(u"//*[@class='MAvaLevel']")[0].text)

print( '评论: ', tree.xpath(u"//*[@class='num-reviews _j_filter on']//b")[0].text)
print( '金牌评论: ', tree.xpath(u"//*[@class='num-gold _j_filter']//b")[0].text)
print( '点赞: ', tree.xpath(u"//*[@class='num-ding _j_filter']//b")[0].text)
print( '空白评论: ', tree.xpath(u"//*[@class='num-notReviews _j_filter']//b")[0].text)

print( '')