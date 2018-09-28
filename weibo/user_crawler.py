import json
import threading

import requests
import time

from mysql_db_manager import CrawlDatabaseManager

CRAWL_DELAY = 2

class UsersCrawler:
    url_format = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_%s&page=%d'

    querystring = {"version":"v4"}

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"version\"\r\n\r\nv4\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'host': "m.weibo.cn",
        'connection': "keep-alive",
        'cache-control': "no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, sdch, br",
        'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6",
        'cookie': "SCF=AlTf48qNezF12LbNvCHGGee_Nymdun-Sp9kGATl9gjhJAPPkj2QBT2-Y2MECfIjqy1QjvcBbdVr9HWi6hgbgnTQ.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhEEfKT6-E_qQ8I2HTu2.Vu5JpX5o2p5NHD95Qp1hq4She41K-pWs4DqcjGC2Hkg.y8Kntt; SUB=_2A250CvjnDeRhGeBP7FoW9SvEwjiIHXVX9JivrDV6PUJbkdANLUvGkW1966OJJxi88Ah66us23Spcr23Dpw..; SUHB=0cSXjt5Dqq_ieZ; _T_WM=e0f6480701da87741a5b948440f9d665; SSOLoginState=1495508844; ALF=1498100844; H5_INDEX=0_all; H5_INDEX_TITLE=%E4%BD%A0%E5%B7%B2%E7%BB%8F%E8%A2%AB%E7%A7%BB%E9%99%A4%E7%BE%A4%E8%81%8A; M_WEIBOCN_PARAMS=featurecode%3D20000320%26oid%3D4110491498745329%26luicode%3D10000011%26lfid%3D231051_-_followers_-_5979396421",
        'postman-token': "0b85ea3b-073b-a799-4593-61095e4ed01a"
    }

    # response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    db_manager = None

    threads = []

    run = False

    def __init__(self, uid):
        self.db_manager = CrawlDatabaseManager(10)
        self.root_uid = uid

    # 根据 uid 来抓取一个用户的关注列表
    def fetch_users(self, uid, page):
        url = (self.url_format)%(uid, page)
        response = requests.request("GET", url, data=self.payload, headers=self.headers, params=self.querystring)
        return response.text

    # 从数据库里获取一个新的uid
    def next_uid(self):
        uid = self.db_manager.dequeue_user()
        if uid is None:
            return None
        return uid['user_id']

    # 启动一个新的线程开始抓取
    def start(self):
        self.run = True
        t = threading.Thread(target=self.crawl_feeds, name=None)
        self.threads.append(t)
        # set daemon so main thread can exit when receives ctrl-c
        t.setDaemon(True)
        t.start()

    # 开始抓取用户信息
    def crawl_users(self):
        kickstart = True
        self.run = True

        while self.run:
            uid = self.next_uid()
            if uid is None:
                if kickstart:
                    kickstart = False
                    uid = self.root_uid
                else:
                    print("No more user available")
                    break

            user_str = self.fetch_users(uid, 1)

            print("downloading user of ", uid)

            users = json.loads(user_str)

            f = open('users.txt', 'w+')
            f.write(user_str)
            f.close()

            # 数据解析，如果出错，可能是数据为空，继续下一个user
            try:
                for user in users['data']['cards'][1]['card_group'][1]['users']:
                    print("paring user: ", user['screen_name'])
                    name = user['screen_name']
                    user_id = user['id']
                    followers_count = user['followers_count']
                    follow_count = user['follow_count']
                    description = user['description']
                    self.db_manager.enqueue_user(user_id,
                                                 name=name,
                                                 follow_count=follow_count,
                                                 followers_count=followers_count,
                                                 description=description)
            except Exception as err:
                continue

            time.sleep(CRAWL_DELAY)

if __name__ == '__main__':
    # 种子用户，爬虫的第一个节点，需要手动设置
    root_uid = '1496814565'

    user_crawler = UsersCrawler(root_uid)

    user_crawler.crawl_users()