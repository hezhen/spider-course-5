# -*- coding: utf-8 -*-
import hashlib
from collections import deque
from bloom_filter import BloomFilter
from selenium import webdriver
import re
from lxml import etree
import time

download_bf = BloomFilter(1024*1024*16, 0.01)
cur_queue = deque()

def create_driver():
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
    return driver

def login(driver, username, password):
    login_url = 'https://login.taobao.com/member/login.jhtml'
    driver.get(login_url)
    driver.execute_script("document.getElementById('J_Quick2Static').click()")
    driver.execute_script("document.getElementById('TPL_username_1').value = '{}'".format(username))
    driver.execute_script("document.getElementById('TPL_password_1').value = '{}'".format(password))
    driver.execute_script("document.getElementById('J_SubmitStatic').click()")

def enqueueUrl(url):
    try:
        md5v = hashlib.md5(url.encode('utf8')).hexdigest()
        if md5v not in download_bf:
            cur_queue.append(url)
            download_bf.add(md5v)
            print(url, ' added to queue')
        # else:
            # print 'Skip %s' % (url)
    except ValueError:
        pass

def dequeuUrl():
    return cur_queue.popleft()

def get_product_info(driver, product_url):
    print('On product: ', product_url)
    # ignore ssl error, optionally can set phantomjs path
    driver.get(product_url)
    time.sleep(2)
    content = driver.page_source
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

    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('Product: ', title, 'Price: ', real_price)

def crawl_shop(driver, url):
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
    cat_links = re.findall('(https://.*\.(taobao|tmall).com/category-[\d\-]+?.htm)', content)

    all_products = []

    for cat_link in cat_links:
        driver.get(cat_link)
        content = driver.page_source
        all_products += re.findall('href=[\"\']{1}(//detail.(taobao|tmall).com/item.htm[^>\"\'\s]+?)"', content)
        for product in all_products:
            enqueueUrl(product)
        time.sleep(3)

if __name__ == '__main__':
    driver = create_driver()
    username = 'user'
    password = 'password'
    # login(driver, username, password)
    shop_url = "https://sony.tmall.com"
    crawl_shop(driver, shop_url)
    driver.close()