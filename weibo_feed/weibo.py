
import requests
import sys
import pickle
import os.path, time

url = "https://passport.weibo.cn/sso/login"
cookie_fn = 'weibo.cookie'

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

def login(username='18600663368', password=''):
    if (time.time() - os.path.getmtime(cookie_fn)) < 86400:
        return load_session()

    payload = ( "username={}&password={}&savestate=1&r=https%3A%2F%2Fm.weibo.cn%2Fstatus%2F"
            "HbclHn7NG%3F&ec=0&pagerefer=https%3A%2F%2Fpassport.weibo.cn%2Fsignin%2F"
            "welcome%3Fentry%3Dmweibo%26r%3Dhttps%253A%252F%252Fm.weibo.cn%252Fstatus%252FHbclHn7NG%253F&entry=mweibo")
    payload = payload.format(username, password)
    requests.request("POST", url, data=payload, headers=headers)
    session = requests.session()
    with open(cookie_fn, 'wb') as f:
        pickle.dump(session.cookies, f)
    return session

def load_session():
    session = requests.session()  # or an existing session
    with open(cookie_fn, 'rb') as f:
        session.cookies.update(pickle.load(f))
    return session

if __name__ == "__main__":
     if len(sys.argv) == 3:
         session = login(sys.argv[1], sys.argv[2])