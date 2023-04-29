# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonProductItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    asin_code = scrapy.Field()
    url = scrapy.Field()
    features = scrapy.Field()
    images = scrapy.Field()
    average_rating = scrapy.Field()
    ratings_count = scrapy.Field()


class AmazonReviewItem(scrapy.Item):
    asin_code = scrapy.Field()
    reviewer_name = scrapy.Field()
    summary = scrapy.Field()
    rating = scrapy.Field()
    verified_purchase = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field()
    review = scrapy.Field()