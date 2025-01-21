Universal Web Scraping Code Created by AI 

www.coprser.com


```python
from coparser.amazon-com import *

if __name__ == '__main__':
        import lxml.html
        url='https://www.amazon.com/dp/B0D8GB6VRD/ref=sspa_dk_detail_2'
        html=get_html(url)
        tree = lxml.html.fromstring(html)
        result={}
        
        result['SellPrice']=extract_SellPrice(tree)
        result['ProductName']=extract_ProductName(tree)
        result['TotalReview']=extract_TotalReview(tree)
        result['Availability']=extract_Availability(tree)
        result['ProductImage']=extract_ProductImage(tree)
        result['AverageReview']=extract_AverageReview(tree)

        print(result)


```
