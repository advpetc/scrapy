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
from bs4 import NavigableString
from PeoplesDaily.items import PeoplesdailyItem
import json
from scrapy.exceptions import CloseSpider
from scrapy.utils.response import open_in_browser
import urllib.request
import logging


class ParagraphSiper(CrawlSpider):
    name = "test"
    http_buffer = "http://data.people.com.cn"
    page_cnt = 6
    # use cookie instead of explict login info, TODO
    cookie = {
        "JSESSIONID": "04337EE5F6C5D6352103646CB97791BC",
        "validateCode": "uOnVMc3TNci8eOl9hQ3nrg%3D%3D",
        # "pageSize": 20,
        # "pageNo": 2
    }
    query = {"cId": "38", "cds": [{"fld": "dataTime.start", "cdr": "AND", "hlt": "false", "vlr": "AND", "qtp": "DEF", "val": "2001-01-01"}, {
        "fld": "dataTime.end", "cdr": "AND", "hlt": "false", "vlr": "AND", "qtp": "DEF", "val": "2020-05-02"}], "obs": [{"fld": "dataTime", "drt": "DESC"}]}

    url = http_buffer + "/pd/wjbyl/s?qs=" + json.dumps(query)
    verifying = False

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
                item['content'] = ""
                while self.verifying:
                    logging.error("waiting for entering captcha")
                yield Request(self.http_buffer+url['href'], method='GET',
                              meta={'item': item},
                              callback=self.parse_content, cookies=self.cookie)
        if self.page_cnt < 295:
            self.page_cnt += 1
            yield FormRequest(url=self.url,
                              method='POST',
                              cookies=self.cookie,
                              formdata={'pageNo': "{}".format(self.page_cnt),
                                        'pageSize': '20', 'top': '0'},
                              callback=self.parse)

    def parse_content(self, response):
        print("success")
        soup = BeautifulSoup(response.body, 'html.parser')
        raw = soup.find_all("div", {"class": "detail"})
        if len(raw) == 0:
            self.verifying = True
            self.crawler.engine.pause()
            open_in_browser(response)
            # img = urllib.request.urlretrieve(self.http_buffer+"/servlet/validateCodeServlet", "captcha.jpeg")
            # yield Request(self.http_buffer+"/servlet/validateCodeServlet", method='GET',
            #               cookies=self.cookie,
            #               callback=self.parse_captcha)
            # self.crawler.engine.unpause()
            logging.error("Please enter captcha")
            if input("Have you finished?"):
                self.crawler.engine.unpause()
                self.verifying = False
            item = response.meta['item']
            yield Request(self.http_buffer + item['url'], method='GET',
                          meta={'item': item},
                          callback=self.parse_content, cookies=self.cookie)
        else:
            time_index = raw[0].text.find("时间：")
            response.meta['item']['date'] = raw[0].text[time_index+3:time_index+13]
            response.meta['item']['content'] = raw[0].text[time_index+13:].strip()
    # def parse_captcha(self, response):
    #     captcha = response.body
