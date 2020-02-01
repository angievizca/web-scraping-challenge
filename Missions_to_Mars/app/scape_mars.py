from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import datetime as dt

def scrape_all():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser=Browser("chrome", **executable_path, headless=True)
    news_title, news_paragraph=mars_news(browser)

    data={
        "news_title":news_title,
        "news_paragraph":news_paragraph,
        "featured_image":featured_image(browser),
        "hemispheres":hemisphere(browser),
        "weather":twitter_weather(browser),
        "facts":mars_facts(),
        "last_modified":dt.datetime.now()
    }

    browser.quit()
    return data

def mars_news(browser):
    url="https://mars.nasa.gov/news/"
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    html=browser.html
    news_soup=BeautifulSoup(html, 'htaml.parser')
    try:
        slide_element=news_soup.select_one("ul.item_list li.slide")
        news_title=slide_element.find("div", class_="content_title").get_text()
        news_p=slide_element.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None,None

    return news_title, news_p        


scrape_all()
