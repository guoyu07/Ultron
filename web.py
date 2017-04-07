# !/usr/bin/env python
# -*- coding: utf-8 -*-
import falcon, json, urllib.parse
from app import App


class CrawlerResource(object):
    def on_post(self, req, resp):
        """Handles POST requests"""
        req.auto_parse_form_urlencoded = True
        try:
            body = req.stream.read(req.content_length or 0)
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex)

        try:
            raw_body = urllib.parse.parse_qsl(body.decode('utf8'))
            dict_body = dict(raw_body)
            text = dict_body['text'].split(':', 1)[1]
            crawl = App(text)
            print(crawl.send())
            resp.body = json.dumps({"text": "发布成功"})
        except Exception:
            resp.body = json.dumps({"text": "操作失败"})


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
crawler = CrawlerResource()

app.add_route('/', crawler)
