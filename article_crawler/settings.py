# -*- coding: utf-8 -*-

# Scrapy settings for article_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'article_crawler'

SPIDER_MODULES = ['article_crawler.spiders']
NEWSPIDER_MODULE = 'article_crawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'article_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'article_crawler.middlewares.ArticleCrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'article_crawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
	'article_crawler.pipelines.DuplicatesPipeline' : 500,
	'article_crawler.pipelines.MySQLdbPipeline': 800,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Dictionary that store css path to data that we need to crawl
# Dictionary structure: website name: list of css path
# List structure: ['article tittle and url css path', 'article author css path',
# 'article category css path', intro text css path', 'intro image css path', 
# 'article title css element', 'article author css element', 'article datetime css element', 
# 'article category css element', 'intro text css element', 'intro image css element', 
# 'full text url css element', 'full text css element', 'next web page url (link)']
# List elements type: string
WEBSITE_CSS_PATH = {
	'hi-news.ru':['div.item > h2', 'div.item > ul.info > li', 'div.item > div.subjects',		# hi-news.ru
	'div.item > div.text', 'div.item > div.cover-wrap > div.cover > a', 'a::text', 'a::text', 
	'time.long::attr(datetime)', 'a::text', 'p', 'img', 'a::attr(href)', 
	'div.text > div > span > div > p', 'div.wp-pagenavi > a.nextpostslink::attr(href)'],
	'hi-news.ru/page':['div.item > h2', 'div.item > ul.info > li', 'div.item > div.subjects',	# hi-news.ru/page
	'div.item > div.text', 'div.item > div.cover-wrap > div.cover > a', 'a::text', 'a::text', 
	'time.long::attr(datetime)', 'a::text', 'p', 'img', 'a::attr(href)', 
	'div.text > div > span > div > p', 'div.wp-pagenavi > a.nextpostslink::attr(href)'],
}

# MySQLdb connection settings
MYSQLDB_HOST = "localhost"
MYSQLDB_USER = "root"
MYSQLDB_PASS = "admin"
MYSQLDB_DB_MYSQL = "articles" # database for store in MySQL database
MYSQLDB_DB_DUPLICATE = "web_crawl_database" # database for handle duplicate article
MYSQLDB_CHARSET = "utf8"
MYSQLDB_INIT_COMMAND = "SET NAMES UTF8, sql_mode = ''"