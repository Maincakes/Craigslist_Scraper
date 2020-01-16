import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import urllib.request


class CraigslistScraper(object):
    dir = os.path.dirname(__file__)
    chrome_driver_path = dir + "\chromedriver.exe"

    def __init__(self, location, max_price, query, min_price, radius, postal):
        self.location = location
        self.max_price = max_price
        self.min_price = min_price
        self.query = query
        self.radius = radius
        self.postal = postal

        self.url = f"https://{location}.craigslist.org/search/sss?query={query}&sort=rel&bundleDuplicates=1&" \
                   f"search_distance={radius}&postal={postal}&min_price={min_price}&max_price={max_price}"

        self.driver = webdriver.Chrome(os.path.dirname(__file__) + "\chromedriver.exe")
        self.delay = 1

    def test(self):
        print(self.url)

    def load_craigslist_url(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            # This is telling Selenium to wait until the craigslist page has loaded. It is doing this by waiting until
            # it can see the searchform which is the main form of the craigslist website that lists the items.
            wait.until(EC.presence_of_element_located((By.ID, 'searchform')))
            print(self.url)
            print('Page is ready')
        except TimeoutException:
            # If this message is coming up you may need to increase the delay time.
            print('Loading took too much time')

    def extract_post_information(self):
        all_posts = self.driver.find_elements_by_class_name('result-title')
        all_prices = self.driver.find_elements_by_class_name('result-meta')
        all_info = self.driver.find_elements_by_class_name('result-info')

        titles = []
        prices = []
        dates = []

        for post in all_posts:
            title = post.text
            if len(title) > 0:
                titles.append(title)

        for price in all_prices:
            price = price.text.split(' ')
            if len(price) < 2:
                continue
            else:
                price = price[0]
                prices.append(price)

        for info in all_info:
            # data comes in as month day and then post information. So if you split it by a space you can get the date
            # of the post by using the first element and the day by grabbing the second element.
            date = info.text.split(' ')
            if len(date) < 2:
                continue
            else:
                month = date[0]
                day = date[1]
                full_date = month + ' ' + day
                dates.append(full_date)

        return titles, prices, dates

    def extract_post_url(self):
        url_list = []
        html_page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(html_page, features='html.parser')
        for link in soup.findAll('a', {'class': 'result-title hdrlnk'}):
            # print(link['href'])
            url_list.append(link['href'])

        return url_list

    def detail_url(self):
        url_list = []
        detail_data = []
        html_page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(html_page, features='html.parser')
        for link in soup.findAll('a', {'class': 'result-title hdrlnk'}):
            # print(link['href'])
            url_list.append(link['href'])

        details = urllib.request.urlopen(url_list[1])
        detail_soup = BeautifulSoup(details, features='html.parser')
        for detail in detail_soup.findAll('div', {'class': 'mapAndAttrs'}):
            detail_data.append(detail)

        return detail_data



    def quit(self):
        self.driver.close()


location = 'bend'
max_price = '5000'
min_price = '1000'
query = 'subaru'
radius = '25'
postal = '97701'

scraper = CraigslistScraper(location, max_price, query, min_price, radius, postal)
scraper.load_craigslist_url()
titles, prices, dates = scraper.extract_post_information()
print(len(titles))
print(len(prices))
print(len(dates))
urls = scraper.extract_post_url()
#print(urls)
print(len(urls))
detailed = scraper.detail_url()
print(detailed)


#df = pd.DataFrame(data={'col1': titles, 'col2': prices, 'col3': dates, 'col4': urls})
#df.to_csv('./file.csv', sep=',', index=False)

#scraper.quit()
