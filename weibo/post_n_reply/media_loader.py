# -*- coding: utf-8 -*-

import json
from threading import Thread
import requests
import re
import time

class MediaLoader:
    def __init__(self, json_obj):
        self.data = json_obj
        self.media_files = {}
        self.media_files['pics'] = []

    def get_media_files(self):
        type = None
        if 'pics' in self.data:
            self.parse_pics()
            type = 'pics'
        elif 'page_info' in self.data:
            if self.data['page_info']['type'] == 'video':
                self.parse_videos()
                type = 'video'
        return type, self.media_files
        
    def parse_pics(self):
        for pic in self.data['pics']:
            url = pic['large']['url']
            self.media_files['pics'].append(url)
            t = Thread(target=self.download_pics, args=(url,))
            t.start()

    def parse_videos(self):
        pic_url = self.data['page_info']['page_pic']['url']
        self.media_files['pics'].append(pic_url)
        t = Thread(target=self.download_pics, args=(pic_url,))
        t.start()

        video_url = self.data['page_info']['media_info']['stream_url_hd']
        if video_url is None:
            video_url = self.data['page_info']['media_info']['stream_url']

        re_result = re.findall(r'.*/(.*\.mp4)?', video_url)
        if len(re_result) > 0:
            video_filename = re_result[0]
        else:
            video_filename = time.ctime() + '.mp4'

        self.media_files['video'] = video_filename

        t = Thread(target=self.download_video, args=(video_url, video_filename, ))
        t.start()
    
    def download_pics(self, url):
        r = requests.get(url)
        with open(url[url.rfind('/')+1:], 'wb') as f:
            f.write(r.content)

    def download_video(self, video_url, video_filename):
        r = requests.get(video_url, stream = True)
        # download started 
        with open( video_filename, 'wb') as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk)

if __name__ == "__main__":
    with open('test_data/pics.json', 'rb') as f:
        c = f.read()
    obj = json.loads(c)
    print(MediaLoader(obj[0]['status']).get_media_files())