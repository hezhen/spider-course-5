
import requests
import sys
import pickle
import os.path, time
import re
import json
import argparse


cookie_fn = 'weibo.cookie'

class WeiboFeedCrawler:
    login_url = "https://passport.weibo.cn/sso/login"

    reply_url_0 = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'
    reply_url_1 = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0'
    
    headers = {
        'accept': "*/*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'connection': "keep-alive",
        'content-type': "application/x-www-form-urlencoded",
        'origin': "https://passport.weibo.cn",
        'referer': "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2Fstatus%2FHbclHn7NG%3F",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'cache-control': "no-cache"
    }

    def __init__(self, username, password, url, reply_limit = 0):
        self.username = username
        self.password = password
        self.post_url = url
        self.reply_limit = reply_limit
        self.pattern = re.compile('<.*>')
        self.max_id = None
        self.replies = []

    def login(self):
        if self.check_cookie_file() and (time.time() - os.path.getmtime(cookie_fn)) < 86400:
            return self.load_session()

        payload = ( "username={}&password={}&savestate=1&r=https%3A%2F%2Fm.weibo.cn%2Fstatus%2F"
                "HbclHn7NG%3F&ec=0&pagerefer=https%3A%2F%2Fpassport.weibo.cn%2Fsignin%2F"
                "welcome%3Fentry%3Dmweibo%26r%3Dhttps%253A%252F%252Fm.weibo.cn%252Fstatus%252FHbclHn7NG%253F&entry=mweibo")
        payload = payload.format(self.username, self.password)
        requests.request("POST", self.login_url, data=payload, headers=self.headers)
        self.session = requests.session()
        with open(cookie_fn, 'wb') as f:
            pickle.dump(self.session.cookies, f)
    
    def check_cookie_file(self):
        return os. path. isfile(cookie_fn)

    def load_session(self):
        self.session = requests.session()  # or an existing session
        with open(cookie_fn, 'rb') as f:
            self.session.cookies.update(pickle.load(f))

    def get_post(self):
        self.post_response = self.session.get(self.post_url)
        c = self.post_response.text

        match_objs = re.findall(r'var\s*\$render_data\s*=\s*([\s\S]*)\[0\]\s\|\|\s\{\};', c)
        if len(match_objs) > 0:
            render_data = json.loads(match_objs[0])[0]
            self.id = render_data['status']['id']
            self.mid = render_data['status']['mid']
            self.reply_count = render_data['status']['comments_count']
            self.post_title = render_data['status']['page_info']['title']
            self.post_content1 = render_data['status']['page_info']['content1']
            self.post_content2 = render_data['status']['page_info']['content2']

            # resize the limit according to size of replies
            self.reply_limit = min(self.reply_limit, self.reply_count)

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
        response = self.session.get(reply_url)
        replies = json.loads(response.text)
        self.max_id = replies['data']['max_id']

        for reply in replies['data']['data']:
            r_text = reply['text']
            r_text = self.pattern.sub('', r_text)
            self.replies.append(r_text)
        
        if len(self.replies) < self.reply_limit:
            self.get_replies()

    def start(self):
        self.login()
        self.get_post()
        self.get_replies()

class arguments:
    pass

def parse_app_arguments():
    parser = argparse.ArgumentParser(prog='Weibo Feed Spider', description='Get a post and its replies from weibo')
    parser.add_argument('-u', '--user', type=str, nargs=1, help='username of weibo')
    parser.add_argument('-p', '--psssword', type=str, nargs=1, help='password of the weibo account')
    parser.add_argument('-l', '--limit', type=int, nargs=1, help='limit of replies to download')
    parser.add_argument('-a', '--url', type=str, nargs=1, help='url of the post')
    
    args = arguments()

    parser.parse_args(namespace=args)

    if args.user is None:
        args.user = '18600663368'

    if args.url is None:
        args.url = 'https://m.weibo.cn/status/HbvLv54Lc'

    if args.password is None:
        args.password = ''

    if args.limit is None:
        args.limit = 200

    return args

if __name__ == "__main__":
    args = parse_app_arguments()
    weibo_crawler = WeiboFeedCrawler(args.user, args.password, args.url, args.limit)
    weibo_crawler.start()