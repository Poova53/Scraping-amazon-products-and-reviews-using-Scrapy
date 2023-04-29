# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class AmazonPipeline:
    def __init__(self) -> None:
        pass
        self.con = sqlite3.connect("smartphones.db")
        self.cur = self.con.cursor()
        self.create_tables()
        
    def process_item(self, item, spider):
        if spider.name == "amazon_product":
        
            if self.item_exist(item["asin_code"]):
                spider.logger.info(f" {item['asin_code']}: Item already Exists")
            
            else:
                try:
                    self.update_product_table(item)
                    self.update_image_table(item)
                    self.update_feature_table(item)
                    spider.logger.info("Item added to database!")
                    
                except Exception as e:
                    spider.logger.error(e)
                    
        if spider.name == "amazon_review":
            try:
                self.update_review_table(item)
                spider.logger.info("Item added to database!")
            
            except Exception as e:
                spider.logger.error(e)
            
    
    def create_tables(self):
        self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS Product(
                        Id integer PRIMARY KEY,
                        Asin_code text UNIQUE,
                        Name text NOT NULL,
                        Price int,
                        Url text NOT NULL,
                        Average_rating real,
                        Ratings_count int
                    )
                    """)
        
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS ProductImage(
                             Id integer PRIMARY KEY,
                             Asin_code FOREIGNKEY REFERENCES Product (Asin_code),
                             Image_link text
                         )
                         """)
        
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS ProductFeature(
                             Id integer PRIMARY KEY,
                             Asin_code FOREIGNKEY REFERENCES Product(Asin_code),
                             Feature text
                         )
                         """)
        
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Review(
                Id integer PRIMARY KEY,
                Asin_code FOREIGNKEY REFERENCES Product (Asin_code),
                Reviewer_name text,
                Summary text,
                Rating real,
                Verified_purchase integer,
                Location text,
                Date text,
                Review text
            )
            """)

        self.con.commit()


    def item_exist(self, asin_code):
        self.cur.execute("""
                         SELECT Asin_code FROM Product
                         WHERE Asin_code = ?
                         """,
                         (asin_code,)
                         )
        
        if self.cur.fetchone() == None:
            return False
        return True
    
    
    def update_product_table(self, item):
        self.cur.execute("""
                         INSERT INTO Product(Asin_code, Name, Price, Url, Average_rating, Ratings_count) VALUES(?, ?, ?, ?, ?, ?)
                         """,
                         (
                             item['asin_code'],
                             item['name'],
                             item['price'],
                             item['url'],
                             item.get('average_rating', ""),
                             item.get('ratings_count', "")
                         )
                         )
        self.con.commit()
        
        
    def update_image_table(self, item):
        for image_link in item['images']:
            self.cur.execute("""
                              INSERT INTO ProductImage(Id, Asin_code, Image_link) VALUES(NULL, ?, ?)
                              """,
                              (item['asin_code'], image_link)
                              )
            self.con.commit()
    
    
    def update_feature_table(self, item):
        for feature in item['features']:
            self.cur.execute("""
                              INSERT INTO ProductFeature(Id, Asin_code, Feature) VALUES(NULL, ?, ?)
                              """,
                              (item['asin_code'], feature)
                              )
            self.con.commit()
            
    def update_review_table(self, item):
        self.cur.execute("""
            INSERT INTO Review(Asin_code, Reviewer_name, Summary, Rating, Verified_purchase, Location, Date, Review) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item['asin_code'],
                item.get('reviewer_name', None),
                item.get('summary', None),
                item.get('rating', None),
                item.get('verified_purchase', None),
                item.get('location', None),
                item.get('date', None),
                item.get('review', None)
            )
            )

        self.con.commit()
        
    
    
