# -*- coding: utf-8 -*-

from threading import Thread
import re
import requests
import os

class pic_downloader():
    res_dir = './res'

    def __init__(self, json_obj):
        self.data = json_obj
        self.media_files = {}
        self.media_files['pics'] = []
    
    def assure_res_dir(self):
        if not os.path.exists(self.res_dir):
            os.makedirs(self.res_dir)

    def get_media_files(self):
        type = None
        if 'pics' in self.data:
            pic_urls = [x['large']['url'] for x in pics]
            type = 'pics'
            t = Thread(target=self.download_pics, args=(pic_urls,))
            t.start()
        elif 'page_info' in self.data:
            if self.data['page_info']['type'] == 'video':
                self.parse_videos()
                type = 'video'
        return type, self.media_files

    def parse_videos(self):
        pic_url = self.data['page_info']['page_pic']['url']
        self.media_files['pics'].append(pic_url)
        t = Thread(target=self.download_pics, args=((pic_url),))
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

    def download_video(self, video_url, video_filename):
        r = requests.get(video_url, stream = True)
        self.assure_res_dir()
        # download started 
        with open( self.res_dir + '/' + video_filename, 'wb') as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk)

    def download_pics(self, pic_urls):
        self.assure_res_dir()

        i = 1
        for url in pic_urls:
            print('Download picture', i, "of ", len(pic_urls))
            r = requests.get(url)
            filename = self.res_dir + url[url.rfind('/'):]
            with open(filename, 'wb') as f:
                f.write(r.content)
            i += 1