import scrapy
import random
from Amazon.items import AmazonProductItem
from urllib.parse import urlencode, urljoin
from Amazon.itemloaders import AmazonProductLoader
from Amazon.user_agent_and_proxy_lists import user_agent_list, proxies_list


class AmazonProductSpider(scrapy.Spider):
    name = "amazon_product"
        
    def start_requests(self):
        for page_no in range(1, 21):
            search_detail = {"k": "smartphones", "page": page_no}
            search_url = "https://www.amazon.in/s?" + urlencode(search_detail)
            
            yield scrapy.Request(
                url= search_url,
                callback=self.parse_product_url,
                headers={"User-Agent": user_agent_list[random.randint(0, len(user_agent_list)-1)]},
                meta={"proxy": proxies_list[random.randint(0, len(proxies_list)-1)]}
            )
                

    def parse_product_url(self, response):
        
        products_list = response.css("div[data-component-type='s-search-result']")
        
        for product in products_list:
            url = product.css("h2 a::attr(href)").get()
            product_url = urljoin("https://www.amazon.in/", url).split("?keywords")[0]
            
            yield scrapy.Request(
                url= product_url,
                callback=self.parse_product_data,
                headers={"User-Agent": user_agent_list[random.randint(0, len(user_agent_list)-1)]},
                meta={"proxy": proxies_list[random.randint(0, len(proxies_list)-1)]}
            )
            
        """ for _ in range(2, 21):
            page_links = response.css("a.s-pagination-item::attr(href)").getall()
            next_page_url = "https://www.amazon.in" + page_links[-1]
            
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_product_url,
                meta={"page": page+1, "keyword": Keyword}
            )
             """
            
    
    def parse_product_data(self, response):
        
        Product_loader  = AmazonProductLoader(item=AmazonProductItem(), response=response)
        
        Product_loader.add_css('name', 'h1 #productTitle::text')
        Product_loader.add_css('price', 'input#twister-plus-price-data-price::attr(value)')
        Product_loader.add_css('asin_code', 'input#asin::attr(value)')
        Product_loader.add_value('url', [response.request.url])
        Product_loader.add_css('features', "#feature-bullets li span::text")
        Product_loader.add_css('average_rating', "i[data-hook=average-star-rating] span::text")
        Product_loader.add_css('ratings_count', "span#acrCustomerReviewText::text")
        Product_loader.add_value('images', response.text)
        
        yield Product_loader.load_item()
        
