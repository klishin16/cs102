import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    headline_list = parser.findAll("a", {"class": "storylink"})
    news_table_list = parser.find_all("td", {"class": "subtext"})
    for item in range(len(headline_list)):
        headline = headline_list[item].text
        points = news_table_list[item].find("span", {"class": "score"}).text.split()[0]
        author = news_table_list[item].find("a", {"class": "hnuser"}).text
        comments = news_table_list[item].find_all("a")[5].text
        url = headline_list[item]['href']
        if comments == "discuss":
            comments = "0"
        new = {
            'author': author,
            'points': points,
            'title': headline,
            'comments': comments,
            'url': url
        }
        news_list.append(new)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    next_page_url = parser.find("a", {"class": "morelink"})['href']
    return next_page_url


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


