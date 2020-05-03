#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Haoyang <peter@peterchen.xyz>
#
# Distributed under terms of the MIT license.

"""
test authentication
"""
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
from PeoplesDaily.items import PeoplesdailyItem
import json


class ParagraphSiper(CrawlSpider):
    name = "test"
    http_buffer = "http://data.people.com.cn"
    page_cnt = 1
    ## use cookie instead of explict login info, TODO
    cookie = {
        "JSESSIONID": "F5C3D980C491F127D7EFBF63C6D4A7AA",
        "validateCode": "7kJrZT5qcJ6J7p0QqEL2Tg%3D%3D",
        "pageSize": 20,
        "pageNo": 2
    }
    query = {"cId": "38", "cds": [{"fld": "dataTime.start", "cdr": "AND", "hlt": "false", "vlr": "AND", "qtp": "DEF", "val": "2001-01-01"}, {
        "fld": "dataTime.end", "cdr": "AND", "hlt": "false", "vlr": "AND", "qtp": "DEF", "val": "2020-05-02"}], "obs": [{"fld": "dataTime", "drt": "DESC"}]}

    url = http_buffer + "/pd/wjbyl/s?qs=" + json.dumps(query)

    def start_requests(self):
        yield Request(url=self.url, cookies=self.cookie, method='GET',
                      callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        raw = set(soup.find_all("a", target="_blank", href=True))
        urls = []
        for url in raw:
            if 'detail' in url['href'] and url.contents[0] not in ("详情"):
                item = PeoplesdailyItem()
                item['title'] = url.contents[0]
                item['url'] = self.http_buffer + url['href']
                with open("file{}.txt".format(self.page_cnt), 'a') as w:
                    w.write(item['title'] + " " + item['url'] + "\n")
                yield Request(self.http_buffer+url['href'], method='GET',
                              # headers=self.headers,
                              meta={'item': item},
                              callback=self.parse_content, cookies=self.cookie)
        self.page_cnt += 1
        if self.page_cnt < 10:
            yield FormRequest(url=self.url,
                              method='POST',
                              cookies=self.cookie,
                              formdata={'pageNo': "{}".format(self.page_cnt),
                                        'pageSize': '20', 'top': '0'},
                              callback=self.parse)

    def parse_content(self, response):
        print("success")
        print(response.meta['item'])

        soup = BeautifulSoup(response.body, 'html.parser')

        # with open('test.html'r
