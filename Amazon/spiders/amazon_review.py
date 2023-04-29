import scrapy
import random
import sqlite3
from Amazon.items import AmazonReviewItem
from Amazon.itemloaders import AmazonReviewLoader
from Amazon.user_agent_and_proxy_lists import user_agent_list, proxies_list


class AmazonReviewSpider(scrapy.Spider):
    name = "amazon_review"
    
    def start_requests(self):
        con = sqlite3.connect("smartphones.db")
        cur = con.cursor()
        
        cur.execute("""SELECT Asin_code, Ratings_count from Product""")
        product_list = cur.fetchall()
        
        for product in product_list: # Product will be like (asin_code, ratings_count)
            if product[1] != "":
                review_url = "https://www.amazon.in/product-reviews/" + product[0]
                
                yield scrapy.Request(
                    url=review_url,
                    callback=self.parse_review_data,
                    headers={"User-Agent": user_agent_list[random.randint(0, len(user_agent_list)-1)]},
                    meta={"proxy": proxies_list[random.randint(0, len(proxies_list)-1)], "asin_code": product[0]}
                )

    def parse_review_data(self, response):
        asin_code = response.meta["asin_code"]
        
        review_list = response.css("div#cm_cr-review_list .review")
        
        for review in review_list:
            Review_loader = AmazonReviewLoader(item=AmazonReviewItem(), selector=review)
            
            Review_loader.add_value('asin_code', asin_code)
            Review_loader.add_css('reviewer_name', '.a-profile-name::text')
            Review_loader.add_css('summary', 'a.review-title span::text')
            Review_loader.add_css('rating', ".review-rating span::text")
            Review_loader.add_css('verified_purchase', "span.a-declarative span[data-hook='avp-badge']::text")
            Review_loader.add_css('location', 'span.review-date::text')
            Review_loader.add_css('date', 'span.review-date::text')
            Review_loader.add_css('review', 'span.review-text ::text')
            
            yield Review_loader.load_item()
            
