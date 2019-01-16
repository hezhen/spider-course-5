#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import re
import textwrap
import threading
import time
from subprocess import call
from weibo import WeiboCrawler

from aiohttp.web import Application, Response, StreamResponse, run_app
import json

async def crawl(request):
    resp = StreamResponse()
    data = await request.json()
    url = data['url']
    if 'limit' in data:
        limit = data['limit']
    else:
        limit = 200
    crawler = WeiboCrawler(url, limit)
    ret =  crawler.start()

    await resp.prepare(request)
    await resp.write(json.dumps(ret).encode('utf8'))
    await resp.write_eof()
    return resp

async def intro(request):
    txt = textwrap.dedent("""\
        @param url url of weibo
        @param limit maximum number of replies to grab
        {
            "url": "https://m.weibo.cn/detail/4329233171749375",
            'limit": 100
        }
    """).format(url='127.0.0.1:8080')
    binary = txt.encode('utf8')
    resp = StreamResponse()
    resp.content_length = len(binary)
    resp.content_type = 'text/plain'
    await resp.prepare(request)
    await resp.write(binary)
    return resp

async def simple(request):
    return Response(text="Simple answer")

async def change_body(request):
    resp = Response()
    resp.body = b"Body changed"
    resp.content_type = 'text/plain'
    return resp

async def init(loop):
    app = Application()
    app.router.add_get('/', intro)
    app.router.add_post('/crawl', crawl)
    return app

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))
    run_app(app, host='127.0.0.1', port=9999)