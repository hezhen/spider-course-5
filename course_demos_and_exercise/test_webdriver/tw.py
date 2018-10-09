# -*- coding: utf-8 -*-
from selenium import webdriver
import re
from lxml import etree
import time

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)

# 进入浏览器设置
options = webdriver.ChromeOptions()
# 设置中文
options.add_argument('lang=zh_CN.UTF-8')
# specify the desired user agent
options.add_argument(f'user-agent={user_agent}')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-plugins-discovery")

# ---------- Important ----------------
# 设置为 headless 模式，调试的时候可以去掉
# -------------------------------------
# options.add_argument("--headless")

# 更换头部
# options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
driver = webdriver.Chrome(chrome_options=options)

driver.set_window_size(1920, 1200)  # optional
driver.delete_all_cookies()

driver.execute_script("var s=window.document.createElement('script'); s.src='javascriptChrome.js';window.document.head.appendChild(s);")

login_url = 'https://login.taobao.com/member/login.jhtml'

driver.get(login_url)

username = 'abc'
password = 'test'

driver.execute_script("document.getElementById('J_Quick2Static').click()")
driver.execute_script("document.getElementById('TPL_username_1').value = '{}'".format(username))
driver.execute_script("document.getElementById('TPL_password_1').value = '{}'".format(password))
# driver.execute_script("document.getElementById('J_SubmitStatic').click()")

# driver.execute_script("var s=window.document.createElement('script'); s.src='javascriptChrome.js';window.document.head.appendChild(s);")
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false,});")