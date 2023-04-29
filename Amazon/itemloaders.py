import re
import json
from datetime import datetime
from w3lib.html import remove_tags
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Join, Identity

def checkNone(txt):
    return None if txt.strip() == None else txt.strip()

def getImages(txt):
    json_data = json.loads(re.findall(r"colorImages':.*'initial':\s*(\[.+?\])},\n", txt)[0])
    images_link = []
    for i in json_data:
        images_link.append(i['large'])
    return images_link

class AmazonProductLoader(ItemLoader):
    
    default_output_processor = TakeFirst()
    
    name_in = MapCompose(checkNone)
    name_out = Join(" ")
    
    price_in = MapCompose(lambda x: x.replace(",", ""), str.strip, int)
    
    asin_code_in = MapCompose(str.strip)
    url_in = MapCompose(str.strip)
    
    features_in = MapCompose(checkNone)
    features_out = Identity()
    
    images_in = MapCompose(getImages)
    images_out = Identity()
    
    average_rating_in = MapCompose(checkNone, lambda x: x.split(" ")[0], float)
    ratings_count_in = MapCompose(checkNone, lambda x: x.split(" ")[0].replace(",", "").strip(), int)
    
    

def get_date(txt):
    if txt.strip():
        date_str = txt.split("on")[-1].strip()
        date_object = datetime.strptime(date_str, '%d %B %Y')
        return date_object.strftime('%d-%m-%Y')
  

class AmazonReviewLoader(ItemLoader):
    
    default_output_processor = TakeFirst()  
    
    asin_code_in = Identity()
    
    reviewer_name_in = MapCompose(str.strip)
    
    summary_in = MapCompose(str.strip)
    
    rating_in = MapCompose(lambda x: x.strip().split(" ")[0], float)
    
    verified_purchase_in = MapCompose(bool)
    
    location_in = MapCompose(lambda x: x.split("in")[-1].split("on")[0].strip())
    
    date_in = MapCompose(get_date)
    
    review_in = MapCompose(str.strip)
    review_out = Join(" ")
    