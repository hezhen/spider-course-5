import json
from threading import Thread
import requests
import re
import time

class MediaLoader:
    def __init__(self, json_obj):
        self.data = json_obj

    def get_objects(self):
        if 'pics' in self.data:
            t = Thread(target=self.parse_pics)
            t.start()
        elif 'page_info' in self.data:
            if self.data['page_info']['type'] == 'video':
                t = Thread(target=self.parse_videos)
                t.start()
    
    def parse_pics(self):
        for pic in self.data['pics']:
            url = pic['large']['url']
            self.download_pics(url)

    def parse_videos(self):
        self.download_video()
    
    def download_pics(self, url):
        r = requests.get(url)
        with open(url[url.rfind('/')+1:], 'wb') as f:
            f.write(r.content)

    def download_video(self):
        pic_url = self.data['page_info']['page_pic']['url']
        self.download_pics(pic_url)

        video_url = self.data['page_info']['media_info']['stream_url_hd']
        if video_url is None:
            video_url = self.data['page_info']['media_info']['stream_url']
        re_result = re.findall(r'http://.*/(.*\.mp4)?', video_url)
        if len(re_result) > 0:
            video_filename = re_result[0]
        else:
            video_filename = time.ctime() + '.mp4'
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
    MediaLoader(obj[0]['status']).get_objects()