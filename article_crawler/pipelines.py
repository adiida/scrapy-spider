# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import time
import MySQLdb
from scrapy.conf import settings


class MySQLdbPipeline(object):

	def __init__(self):
		self.conn = MySQLdb.connect(
			host = settings['MYSQLDB_HOST'],
			user = settings['MYSQLDB_USER'],
			passwd = settings['MYSQLDB_PASS'],
			db = settings['MYSQLDB_DB_MYSQL'],
			charset = settings['MYSQLDB_CHARSET'],
			init_command = settings['MYSQLDB_INIT_COMMAND'])

	def process_item(self, item, spider):

		if item:
			article_datetime = time.strftime('%Y-%m-%d %H:%M:%S')

			article_title = item['article_title']
			article_author =  item['article_author']
			if article_author:
				article_author = '<p> Автор: ' + article_author + '</p>'
			else:
				article_author = '<p> Автор: Hi-News.ru </p>'

			# check if we can get datetime from article commentы
			# process and change article_datetime (store current_datetime)
			article_dt = item['article_datetime']
			if article_dt:
				article_datetime = article_dt.split('T')[0] + ' ' + article_dt.split('T')[1].split('+')[0]

			article_category = item['article_category']
			intro_text = item['intro_text']
			intro_img = item['intro_img']
			# intro with image
			intro_text = article_author + intro_img + intro_text
			full_text = item['full_text']
			full_text_url = item['full_text_url']
			full_text = article_author + full_text + '<p><a href= "%s" rel="nofollow"> Источник статьи </a></p>' % full_text_url
			article_alias = full_text_url.strip('/').split('/')[-1].replace('.html', '')

			initial_datetime = '0000-00-00 00:00:00'
			images_ = '{"image_intro":"","float_intro":"","image_intro_alt":"","image_intro_caption":"",'\
			'"image_fulltext":"","float_fulltext":"","image_fulltext_alt":"","image_fulltext_caption":""}'
			urls_ = '{"urla":false,"urlatext":"","targeta":"","urlb":false,"urlbtext":"","targetb":"",'\
			'"urlc":false,"urlctext":"","targetc":""}'
			attribs_ = '{"show_title":"","link_titles":"","show_tags":"","show_intro":"",'\
			'"info_block_position":"0","show_category":"","link_category":"",'\
			'"show_parent_category":"","link_parent_category":"","show_author":"",'\
			'"link_author":"","show_create_date":"","show_modify_date":"",'\
			'"show_publish_date":"","show_item_navigation":"","show_icons":"",'\
			'"show_print_icon":"","show_email_icon":"","show_vote":"","show_hits":"",'\
			'"show_noauth":"","urls_position":"","alternative_readmore":"",'\
			'"article_layout":"","show_publishing_options":"","show_article_options":"",'\
			'"show_urls_images_backend":"","show_urls_images_frontend":""}'
			metadata_ = '{"robots":"","author":"","rights":"","xreference":""}'

			con = self.conn.cursor()

			try:
				con.execute("select max(asset_id) from f72po_content")
				max_asset_id = con.fetchone()
				int_max_asset_id = int(max_asset_id[0]) + 1
				inc_max_asset_id = str(int_max_asset_id)
				print ("asset_id max value : %s " % inc_max_asset_id)

				con.execute("select max(ordering) from f72po_content")
				max_ordering = con.fetchone()
				int_max_ordering = int(max_ordering[0]) + 1
				inc_max_ordering = str(int_max_ordering)
				print ("ordering max value : %s " % inc_max_ordering)

				query = """insert into f72po_content (asset_id, title, alias, introtext, 
				`fulltext`, state, catid, created, created_by, created_by_alias, 
				modified, modified_by, checked_out, checked_out_time, publish_up, 
				publish_down, images, urls, attribs, version, ordering, metakey, 
				metadesc, access, hits, metadata, featured, `language`, xreference) 
				values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 
				'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 
				'%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (inc_max_asset_id, article_title, 
					article_alias, intro_text, full_text, '1', '28', article_datetime, '412', '', initial_datetime, '', '412', 
					initial_datetime, article_datetime, initial_datetime, images_, urls_, attribs_, '1', inc_max_ordering, 
					'', '', '1', '1', metadata_, '0', '*', '')

				con.execute(query)
				self.conn.commit()
			except:
				self.conn.rollback()

			return item

	def close_spider(self, spider):
		self.conn.close()




class DuplicatesPipeline(object):

	def __init__(self):
		self.conn = MySQLdb.connect(
			host = settings['MYSQLDB_HOST'],
			user = settings['MYSQLDB_USER'],
			passwd = settings['MYSQLDB_PASS'],
			db = settings['MYSQLDB_DB_DUPLICATE'],
			charset = settings['MYSQLDB_CHARSET'],
			init_command = settings['MYSQLDB_INIT_COMMAND'])

	def process_item(self, item, spider):

		con = self.conn.cursor()
		article_title = item['article_title']

		try:
			query = """SELECT article_title FROM crawl_article_title WHERE article_title = '%s'""" % (article_title)
			con.execute(query)
			res = con.fetchone()
			if not res:
				query = """insert into crawl_article_title (article_title) values('%s')""" % (article_title)
				con.execute(query)
				self.conn.commit()
				return item
		except:
			self.conn.rollback()

	def close_spider(self, spider):
		self.conn.close()