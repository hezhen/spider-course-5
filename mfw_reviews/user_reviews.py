# -*- coding: utf-8 -*-

import requests

review_loading_url = 'http://www.mafengwo.cn/home/ajax_review.php?act=loadList&filter=0&offset=%d&limit=20&uid=%d&sort=1'

user_id = 129914
offset = 0

url = (review_loading_url%(offset, user_id))

print(url)

headers = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'x-requested-with': "XMLHttpRequest",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    'referer': "http://www.mafengwo.cn/i/10167942.html",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'cache-control': "no-cache"
}

r = requests.get(url, headers = headers )

content = r.text

content = content[content.find('<'):content.rfind('>')+1]

content = content.replace('\\/', '/').replace('\\n', '').replace('\\t', '').replace('\\\"', '\"')

content = content.encode('utf8').decode("unicode-escape")

with open('mfw_user_reivews_%d_%d.html' % (user_id, offset), 'wb+') as f:
	f.write(content.encode('utf8', 'replace'))