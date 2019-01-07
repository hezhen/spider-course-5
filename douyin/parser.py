import json
from mysql_manager import MysqlManager

mysql = MysqlManager(4)

with open('videos.json', 'r') as f:
    i = 1
    while True:
        print("Parse json: ", i)
        i+= 1
        line = f.readline()

        if not line:
            break

        if len(line) < 10:
            continue

        # urls = re.findall('http://v3-dy.ixigua.com[^\"]+', json_str)
        obj = json.loads(line)

        # aweme_list->[n]->video->play_addr->url_list
        i_url = 0
        for v in obj['aweme_list']:
            # print("-----", i_url)
            try:
                url = v['video']['play_addr']['url_list'][0]
            except Exception as err:
                print("parse error ", i, " index: ", i_url)
            i_url += 1
            # print(url)
            mysql.enqueue_url(url)