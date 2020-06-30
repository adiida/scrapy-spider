# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from article_crawler.items import ArticleCrawlerItem
from scrapy.conf import settings



class ArticleCrawlerSpider(Spider):
	name = 'article_crawler'
	allowed_domains = ['hi-news.ru']
	start_urls = ['https://hi-news.ru/']
	css_path_settings = []

	def parse(self, response):
		# handle domain names different element size
		url_elements = response.url.strip('/').split('/')
		domain_name = url_elements[2]
		if len(url_elements) > 4:
			domain_name = url_elements[2] + '/' + url_elements[3]

		self.log('Domain name: ' + domain_name)
		self.css_path_settings = settings['WEBSITE_CSS_PATH'][domain_name]

		article_iter = 0
		for item in response.css('div.roll > div.item'):
			article = ArticleCrawlerItem()

			# set css path to css elements that contain data we want to crawl
			title_url_css_path = response.css(self.css_path_settings[0])[article_iter]
			author_css_path = response.css(self.css_path_settings[1])[article_iter]
			category_css_path = response.css(self.css_path_settings[2])[article_iter] ###
			intro_text_css_path = response.css(self.css_path_settings[3])[article_iter]
			intro_img_css_path = response.css(self.css_path_settings[4])[article_iter]
			
			# set item fields with data from web page
			article['article_title'] = title_url_css_path.css(self.css_path_settings[5]).extract_first()
			article['article_author'] = author_css_path.css(self.css_path_settings[6]).extract_first()
			article['article_category'] = category_css_path.css(self.css_path_settings[8]).extract_first() ###
			article['intro_text'] = ''.join(intro_text_css_path.css(self.css_path_settings[9])[:-1].extract())
			article['intro_img'] = intro_img_css_path.css(self.css_path_settings[10]).extract_first()
			article['full_text_url'] = title_url_css_path.css(self.css_path_settings[11]).extract_first()
			
			# get full text from web page through url
			full_text_url = title_url_css_path.css(self.css_path_settings[11]).extract_first()

			# go through url
			request = Request(url=full_text_url, callback=self.parse_full_text)
			request.meta['article'] = article

			article_iter += 1
			yield request

		next_page_url = response.css(self.css_path_settings[13]).extract_first()
		if next_page_url:
			yield Request(url=next_page_url, callback=self.parse)

	def parse_full_text(self, response):
		article = response.meta['article']
		article['article_datetime'] = response.css(self.css_path_settings[7]).extract_first()
		article['full_text'] = ''.join(response.css(self.css_path_settings[12]).extract())
		yield article
