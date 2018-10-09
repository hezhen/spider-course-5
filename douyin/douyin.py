import requests
import re
import asyncio
import os

headers = {
    'host': "v3-dy.ixigua.com",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'range': "bytes=524288-524288",
    'if-range': "\"9056E63E897E90A3BFB2619B86481603\""
}

dirname = './video/'
# cur_url = 'http://v3-dy.ixigua.com/41774b984e4022ca52a4795be488dec9/5bb667a3/video/m/2200fd0bcf7114241858464e7ee8e62a2ef115bf46e00004b570145264e/'

async def download_coroutine(url):
    file_name = url[url.rindex('/', 0, -1) + 1: -1] + '.mp4'
    print('Start downloading ', file_name)
    r = requests.get(url, stream = True)
    # download started 
    with open( dirname + file_name, 'wb') as f: 
        for chunk in r.iter_content(chunk_size = 1024*1024): 
            if chunk: 
                f.write(chunk)
    msg = 'Finished downloading %s'%(file_name)
    return msg

async def main(urls):
    """
    Creates a group of coroutines and waits for them to finish
    """
    coroutines = [download_coroutine(url) for url in urls]
    completed, pending = await asyncio.wait(coroutines)
    for item in completed:
        print(item.result())	

def check_dir():
    # 检查用于存储网页文件夹是否存在，不存在则创建
    if not os.path.exists(dirname):
        os.makedirs(dirname)

if __name__ == '__main__': 
    check_dir()

    f = open('videos.json', 'r')
    json_str = f.read()
    f.close()
    urls = re.findall('http://v3-dy.ixigua.com[^\"]+', json_str)

    print('Totally ', len(urls), " videos found")

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(urls))
    finally:
        event_loop.close()


# User home
# url = 'https://aweme.snssdk.com/aweme/v1/aweme/post/?iid=45571322477&device_id=48465812670&os_api=18&app_name=aweme&channel=App%20Store&idfa=C1679749-B1B3-40A3-9AF8-5135FC87538C&device_platform=iphone&build_number=28007&vid=7A4E3942-3612-45F9-93CC-BCBA6FF1563D&openudid=0f51fe7cd85057cc1cc9eac88ce3e6e36fa2f8e3&device_type=iPhone10,3&app_version=2.8.0&version_code=2.8.0&os_version=12.0&screen_width=1125&aid=1128&ac=WIFI&count=21&max_cursor=0&min_cursor=0&user_id=96295860466&mas=010eed4d95322a941ab1ae07308c34f33c9f00fd6cbbe2ad434f38&as=a195753b23c8aba9167181&ts=1538677123'