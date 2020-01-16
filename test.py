from .Scraper import CraigslistScraper


def extract_post_information(self):
    all_posts = self.driver.find_elements_by_class_name('result-row')

    titles = []
    dates = []
    prices = []

    for post in all_posts:
        title = post.text.split('$')
        print(title)
        if title[0] == '':
            title = title[:]
        else:
            title = title[0]
        print(title)

        title = title.split('\n')
        price = title[0]
        title = title[-1]

        title = title.split(' ')
        month = title[0]
        day = title[1]
        title = ' '.join(title[2:])
        date = month + ' ' + day

        print('Price ' + price)
        print('Title ' + title)
        print('Date ' + date)

        titles.append(title)
        dates.append(date)
        prices.append(price)
    return titles, prices, dates