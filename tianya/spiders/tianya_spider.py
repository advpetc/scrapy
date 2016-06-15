# from scrapy.spiders import Spider
# from tianya.items import TianyaItem
# from scrapy.http import Request
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy import Selector
# 
# 
# class TianyanSpider(CrawlSpider):
# 	name="tianya"
# 	allowed_domains=["http://bbs.tianya.cn"]
# 	start_urls=["http://bbs.tianya.cn/list-416-1.shtml"]
# 	download_delay=2
# 	#start_urls=["http://bbs.tianya.cn/post-416-105171-1.shtml"]
# 	rules=[Rule(LinkExtractor(allow=('/list.jsp?item=416'),restrict_xpaths=('//div[@class="links"]')),callback='parse',follow=True)]		
# 
# 	def parse(self,response):
# 		#sel=Selector(response)		
# 		text_handle=response.xpath('//td[@class="td-title faceblue"]')
# 		http_buffer="http://bbs.tianya.cn"		
# 		items=[]
# 		file_handle=open('text.txt','w')
# 			
# 		for text in text_handle:
# 			item=TianyaItem()
# 			link=http_buffer+text.xpath('a/@href').extract()[0]#get the title-url to redirect
# 			item['title']=text.xpath('a/text()').extract()	
# 									
# 			file_handle.write(item['title'][0].encode('utf-8'))
# 			file_handle.write("\n")			
# 			file_handle.write(link)
# 			file_handle.write("\n")			
# 					
# 			#print link, item['title'][0]
# 
# 			#yield item
# 			yield Request(link,callback=self.parse_content)
# 			#print link, item['title'][0]
# 			items.append(item)
# 		#file_handle.close()		
# 		
# 
# 		
# 		
# 		#file_handle=open('test.txt','w')
# 		#for text in text_handle:
# 		#	print text			
# 		#	file_handle.write(text.encode('utf-8'))
# 		#file_handle.close()		
# 		
# 
# 	def parse_content(self,response):
# 		text_handle2=response.xpath('//div[@class="bbs-content clearfix"]/text()').extract()
# 		#print text_handle2		
# 		#file_handle=open('text.txt','w')	
# 	
# 		for text in text_handle:
# 			item=TianyaItem()
# 			item['answer']=text_handle2
# 			file_handle.write('something should be here!')			
# 			file_handle.write(text_handle2[0].encode('utf-8'))
# 			print text_handle2
# 		yield item




from scrapy.spiders import Spider
from tianya.items import TianyaItem
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
# import datetime
# import re
# import time
import scrapy
import sys
# from urlparse import urljoin
# from hashlib import md5
#from pybloomfilter import BloomFilter
# from urlparse import parse_qs, urlparse

sys.stdout=open('output.txt','w')

class TianyanSpider(CrawlSpider):
	name="tianya"
	allowed_domains=["http://bbs.tianya.cn"]
	start_urls=["http://bbs.tianya.cn/list-416-1.shtml"]
	#download_delay=2
	#start_urls=["http://bbs.tianya.cn/post-416-105171-1.shtml"]
	
	rules=[Rule(LinkExtractor(allow=('/list.jsp'),deny=('javascript:'),restrict_xpaths=('//div[@class="links"]')),callback='parse',follow=True)]		
	

	def parse(self,response):
		#sel=Selector(response)		
		text_handle=response.xpath('//td[@class="td-title faceblue"]')
		http_buffer="http://bbs.tianya.cn"		
		items=[]
		for text in text_handle:
			item=TianyaItem()
			link=http_buffer+text.xpath('a/@href').extract()[0]#get the title-url to redirect
			item['title']=text.xpath('a/text()').extract()	
									
			# sys.stdout.write(item['title'][0].encode('utf-8'))
# 			sys.stdout.write('\n')		
# 			sys.stdout.write(link)
# 			sys.stdout.write('\n')			

			#yield item
			yield Request(link,callback=self.parse_content,meta={'item':item},dont_filter=True)
# 			yield Request(link, callback=self.parse_content,dont_filter=True)
			items.append(item)
			yield items
		#file_handle.close()		
		sys.stdout.write('next page')

		
		
		#file_handle=open('test.txt','w')
		#for text in text_handle:
		#	print text			
		#	file_handle.write(text.encode('utf-8'))
		#file_handle.close()		
		

	def parse_content(self,response):
		item=response.meta['item']
        
		text_handle2=response.xpath('//div[@class="bbs-content clearfix"]/text()').extract()
		#print text_handle2		
		#file_handle=open('text.txt','w')	
# 		items=[]
		
# 		item=TianyaItem()
		item['answer']=text_handle2
		
		# sys.stdout.write('\n')
# 		sys.stdout.write(text_handle2[0].encode('utf-8'))
		yield item









