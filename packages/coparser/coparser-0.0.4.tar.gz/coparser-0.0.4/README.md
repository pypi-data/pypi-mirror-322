Universal Web Scraping Code Created by AI 

www.coprser.com


```python

from coparser.amazon_com import *
def get_html(url):
    import time
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url,wait_until='domcontentloaded')       
        time.sleep(10)
        page_source = page.content()
        browser.close()
        with open("debug.html", "w", encoding="utf-8") as file:
            file.write(page_source)
        return page_source

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
