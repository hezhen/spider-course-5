# -*- coding: utf-8 -*-

import requests
import sys
import pickle
import os.path, time
import re
import json
import argparse
from media_loader import MediaLoader

cookie_fn = 'cookie'

class WeiboFeedCrawler:
    login_url = "https://passport.weibo.cn/sso/login"

    reply_url_0 = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'
    reply_url_1 = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0'
    
    headers = {
        'accept': "*/*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'connection': "keep-alive",
        'origin': "https://passport.weibo.cn",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'cache-control': "no-cache"
    }

    login_headers = {
        'origin': "https://passport.weibo.cn",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded",
        'accept': "*/*",
        'referer': "https://passport.weibo.cn/signin/login",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'cache-control': "no-cache"
    }

    payload = "username={}&password={}&savestate=1&ec=0&entry=mweibo&mainpageflag=1"

    def __init__(self, url, reply_limit = 0):
        self.username = '18600663368'
        self.password = 'Xi@oxiang66'
        self.payload = self.payload.format(self.username, self.password)
        self.post_url = url
        self.reply_limit = reply_limit
        self.pattern = re.compile('<.*>')
        self.max_id = None
        self.replies = []

    def login(self):
        if self.check_cookie_file() and (time.time() - os.path.getmtime(cookie_fn)) < 86400:
            self.load_cookie()
            return
        # TODO: Use selenium to login
        response = requests.request("POST", self.login_url, data=self.payload, headers=self.login_headers)
        cookie = ''
        for k,v in response.cookies.iteritems():
            cookie += k + '=' + v + ';'
        cookie = cookie[:-1]
        with open(cookie_fn, 'w') as f:
            f.write(cookie)
        self.headers['cookie'] = cookie

    def check_cookie_file(self):
        return os.path.isfile(cookie_fn)

    def load_cookie(self):
        with open(cookie_fn, 'r') as f:
            cookie = f.read()
        self.headers['cookie'] = cookie

    def get_post(self):
        self.post_response = requests.get(self.post_url, headers = self.headers)
        c = self.post_response.text

        match_objs = re.findall(r'var\s*\$render_data\s*=\s*([\s\S]*)\[0\]\s\|\|\s\{\};', c)
        if len(match_objs) > 0:
            render_data = json.loads(match_objs[0])[0]
            # In case of re-post
            if 'retweeted_status' in render_data['status']:
                render_data = render_data['status']['retweeted_status']
            else:
                render_data = render_data['status']

            self.id = render_data['id']
            self.mid = render_data['mid']
            self.reply_count = render_data['comments_count']
            self.post_title = render_data['page_info']['title']
            self.post_content1 = render_data['page_info']['content1']
            self.post_content2 = render_data['page_info']['content2']

            # resize the limit according to size of replies
            self.reply_limit = min(self.reply_limit, self.reply_count)

            self.post_data = render_data

            # start downloader to get pics and videos
            self.media_type, self.media_files = MediaLoader(self.post_data).get_media_files()

            print(self.post_title)
            print(self.post_content1)
            print(self.post_content2)
            print("============================================================")

    def get_replies(self):
        if self.max_id is None:
            reply_url = self.reply_url_0.format(self.id, self.mid)
        elif self.max_id == 0:
            return
        else:
            reply_url = self.reply_url_1.format(self.id, self.mid, self.max_id)
        print(reply_url)
        response = requests.get(reply_url, headers = self.headers)
        
        replies = json.loads(response.text)
        self.max_id = replies['data']['max_id']

        for reply in replies['data']['data']:
            r_text = reply['text']
            r_text = self.pattern.sub('', r_text)
            self.replies.append(r_text)
            print('Reply:-------------\r\n', r_text)
        
        if len(self.replies) < self.reply_limit:
            self.get_replies()

    def start(self):
        self.login()
        self.get_post()
        self.get_replies()

        ret = {}
        ret['title'] = self.post_title
        ret['content'] = self.post_content2
        ret['comments'] = self.replies
        ret['type'] = self.media_type
        ret['media_files'] = self.media_files

        return ret

class arguments:
    pass

def parse_app_arguments():
    parser = argparse.ArgumentParser(prog='Weibo Feed Spider', description='Get a post and its replies from weibo')
    parser.add_argument('-u', '--user', type=str, nargs=1, help='username of weibo')
    parser.add_argument('-p', '--password', type=str, nargs=1, help='password of the weibo account')
    parser.add_argument('-l', '--limit', type=int, nargs=1, help='limit of replies to download')
    parser.add_argument('-a', '--url', type=str, nargs=1, help='url of the post')
    
    args = arguments()

    parser.parse_args(namespace=args)

    if args.user is None:
        args.user = '18600663368'

    if args.url is None:
        args.url = 'https://m.weibo.cn/status/HbBPGhHHg'

    if args.password is None:
        args.password = 'Xi@oxiang66'

    if args.limit is None:
        args.limit = 200

    return args

if __name__ == "__main__":
    args = parse_app_arguments()
    weibo_crawler = WeiboFeedCrawler(args.url, args.limit)
    weibo_crawler.start()