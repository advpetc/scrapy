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
import scrapy
import sys
import urllib

sys.stdout=open('output.txt','w')
class TianyanSpider(CrawlSpider):
	name="tianya"
	allowed_domains=["http://bbs.tianya.cn"]
	start_urls=["http://bbs.tianya.cn/list-416-1.shtml"]
	#download_delay=2
	
	def parse(self,response):
		#sel=Selector(response)	
		text_handle=response.xpath('//td[@class="td-title faceblue"]')
		http_buffer="http://bbs.tianya.cn"		

		for text in text_handle:
			item=TianyaItem()
			link=http_buffer+text.xpath('a/@href').extract()[0]#get the title-url to redirect
			item['title']=text.xpath('a/text()').extract()										

			yield Request(link,callback=self.parse_content,meta={'item':item},dont_filter=True)

		next_page=http_buffer+response.xpath('//div[@class="links"]/a[@rel="nofollow"]/@href').extract()[0]
		sys.stdout.write(next_page)
		yield Request(next_page,callback=self.parse,dont_filter=True)
		
		
		
		#file_handle=open('test.txt','w')
		#for text in text_handle:
		#	print text			
		#	file_handle.write(text.encode('utf-8'))
		#file_handle.close()		
		

	def parse_content(self,response):
		item=response.meta['item']
        
		text_handle2=response.xpath('//div[@class="bbs-content clearfix"]/text()').extract()
		item['answer']=text_handle2
		yield item
	# 
# 	def parse_next_page(self,response):
# 		item=response.meta['item']
# 		yield Request(response.url,callback=self.parse)








