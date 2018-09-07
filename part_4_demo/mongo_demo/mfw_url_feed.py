# -*- coding: utf-8 -*-

import urllib3

import re
from bloom_filter import BloomFilter
import os
from mongo_demo import MongoManager

request_headers = {
    'host': "www.mafengwo.cn",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6"
}

city_home_pages = []
city_ids = []
dirname = 'mafengwo_notes/'

# 创建 Bloom Filter
download_bf = BloomFilter(1024 * 1024 * 16, 0.01)

mongo_manager = MongoManager()

def download_city_notes(id):
    for i in range(1, 999):
        url = 'http://www.mafengwo.cn/yj/%s/1-0-%d.html' % (id, i)
        if url in download_bf:
            continue
        print('open url %s' % (url))
        download_bf.add(url)
        http = urllib3.PoolManager()
        r = http.request('GET', url, headers = request_headers)
        htmlcontent = r.data
        city_notes = re.findall('href="/i/\d{7}.html', htmlcontent.decode('utf8'))

        # 如果导航页错误，该页的游记数为0，则意味着 1-0-xxx.html 已经遍历完，结束这个城市
        if len(city_notes) == 0:
            return
        for city_note in city_notes:
            try:
                city_url = 'http://www.mafengwo.cn%s' % (city_note[6:])
                if city_url in download_bf:
                    continue
                print('download %s' % (city_url))
                http = urllib3.PoolManager()
                r = http.request('GET', city_url, headers = request_headers)
                html = r.data
                mongo_manager.insert_page(city_url, html)
                download_bf.add(city_url)
            except Exception as err:
                print( err )
                raise err

def start_crawl():
    # 检查用于存储网页文件夹是否存在，不存在则创建
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    try:
        # 下载目的地的首页
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://www.mafengwo.cn/mdd/', headers=request_headers)
        htmlcontent = r.data
        
        # 利用正则表达式，找出所有的城市主页
        city_home_pages = re.findall('/travel-scenic-spot/mafengwo/\d{5}.html', htmlcontent.decode('utf8'))

        # 通过循环，依次下载每个城市下的所有游记
        for city in city_home_pages:
            city_ids.append(city[29:34])
            download_city_notes(city[29:34])
    except Exception as err:
            print( err )
            raise err

if __name__ == '__main__':
    start_crawl()