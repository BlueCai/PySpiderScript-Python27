#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-11-03 06:16:30
# Project: IpcMe

import re
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.ipc.me/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.top-entry > .entry-title > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        for each in response.doc('.entry-body > .entry-title > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        for each in response.doc('.pagenavi > a').items():
            if U'下一页 »' == each.html():
                print each.html()
                self.crawl(each.attr.href, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
