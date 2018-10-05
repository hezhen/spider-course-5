# -*- coding: utf-8 -*-
import hashlib
from collections import deque
from bloom_filter import BloomFilter

# -*- coding: utf-8 -*-
from selenium import webdriver
import re
from lxml import etree
import time

user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
)

# 进入浏览器设置
options = webdriver.ChromeOptions()
# 设置中文
options.add_argument('lang=zh_CN.UTF-8')
# specify the desired user agent
options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-plugins-discovery")

# ---------- Important ----------------
# 设置为 headless 模式，调试的时候可以去掉
# -------------------------------------
# options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=options)
driver.delete_all_cookies()

start_url = "https://detail.tmall.com/item.htm?id=540212526343"

driver.get(start_url)

download_bf = BloomFilter(1024*1024*16, 0.01)
cur_queue = deque()

def enqueueUrl(url):
    try:
        md5v = hashlib.md5(url).hexdigest()
        if md5v not in download_bf:
            cur_queue.append(url)
            download_bf.add(md5v)
        # else:
            # print 'Skip %s' % (url)
    except ValueError:
        pass

def dequeuUrl():
    return cur_queue.popleft()

def crawl(url):
    print('crawling ', url)
    # ignore ssl error, optionally can set phantomjs path
    driver.get(url)

    time.sleep(2)

    content = driver.page_source

    with open('tmall_cat.html', 'w+') as f:
        f.write(content)

    # 使用 (pattern) 进行获取匹配
    # +? 使用非贪婪模式
    # [^>\"\'\s] 匹配任意不为 > " ' 空格 制表符 的字符
    tmall_links = re.findall('href=[\"\']{1}(//detail.tmall.com/item.htm[^>\"\'\s]+?)"', content)
    taobao_links = re.findall('href=[\"\']{1}(//detail.taobao.com/item.htm[^>\"\'\s]+?)"', content)

    etr = etree.HTML(content)
    item_price_list = etr.xpath('//span[@class="tm-price"]')
    if len(item_price_list) == 0:
        real_price = 0
    elif len(item_price_list) == 1:
        real_price = item_price_list[0].text
    else:
        real_price = etr.xpath('//dl[contains(@class, "tm-promo-cur")]//span[@class="tm-price"]')[0].text

    title = etr.xpath('//*[@class="tb-detail-hd"]/h1')[0].text
    # 正则表达式，贪婪模式匹配所有非空格字符
    # title = re.findall('([^\s]*)', title)

    # 直接去除首尾空格
    title = title.strip()

    print('+++++++++++++++++++++++++++++++++++++++++++++')
    print('Product: ', title, 'Price: ', real_price)
    print('---------------------------------------------')

    # for link in tmall_links:
    #     print(link)
    # for link in taobao_links:
    #     print(link)

    for href in tmall_links + taobao_links:
        href = "https:" + href
        enqueueUrl(href)

    crawl(dequeuUrl())

if __name__ == '__main__':
    crawl(start_url)
    driver.close()
