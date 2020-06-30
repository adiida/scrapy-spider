# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ArticleCrawlerItem(Item):
    # define the fields for your item here like:
    article_title = Field()
    article_author = Field()
    article_datetime = Field()
    article_category = Field()
    intro_text = Field()
    intro_img = Field()
    full_text_url = Field()
    full_text = Field()


