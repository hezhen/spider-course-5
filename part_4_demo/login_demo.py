# -*- coding: utf-8 -*-

import urllib3

request_headers = {
    'host': "www.mafengwo.cn",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6"
}

login_url = 'https://passport.mafengwo.cn/login/'

def login(username, passowrd):
    data = {'passport':username, "password":passowrd, "code":""}
    http = urllib3.PoolManager()
    r = http.request('POST', login_url, fields= data, headers = request_headers, redirect = False)
    request_headers['cookie'] = r.getheader('set-cookie')
    print('cookie:', request_headers['cookie'])
    # print(r.data)

username = 'Your user name'
password = 'Your password'

login(username, password)