# -*- coding: utf-8 -*-
import hashlib
from collections import deque
from bloom_filter import BloomFilter
from selenium import webdriver
import re
from lxml import etree
import time

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
    login_url = 'https://www.douban.com/login'
    driver.get(login_url)
    driver.execute_script("document.getElementById('email').value = '{}'".format(username))
    driver.execute_script("document.getElementById('password').value = '{}'".format(password))
    driver.execute_script("document.getElementsByName('login')[0].click()")

if __name__ == '__main__':
    driver = create_driver()
    username = 'username'
    password = 'pass'
    login(driver, username, password)
    driver.close()
