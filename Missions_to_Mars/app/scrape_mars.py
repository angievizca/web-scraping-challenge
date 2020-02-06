from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import datetime as dt

def scrape_all():
    executable_path = {"executable_path": "chromedriver"}
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
    news_soup=BeautifulSoup(html, 'html.parser')
    try:
        slide_element=news_soup.select_one("ul.item_list li.slide")
        news_title=slide_element.find("div", class_="content_title").get_text()
        news_p=slide_element.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None,None

    return news_title, news_p        


def featured_image(browser):
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    full_image_element=browser.find_by_id("full_image")
    full_image_button.click()

    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    img = image_soup.select_one("figure.lede a img")
    try:
        img_url = img.get("src")
    except AttributeError:
        return None 

    img_url = f"https://www.jpl.nasa.gov{img_url}"
    return img_url

def twitter_weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    
    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")
    
    mars_weather_tweet = weather_soup.find("div", 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })
    mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    return mars_weather

def mars_facts():
    try:
        df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    df.columns=["Description", "Value"]
    df.set_index("Description", inplace=True)

    return df.to_html(classes="table table-striped")

def hemisphere(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css("a.product-item h3")[item].click()
        
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        hemisphere["title"] = browser.find_by_css("h2.title").text

        hemisphere_image_urls.append(hemisphere)

        browser.back()
    return hemisphere_image_urls

def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere

    
scrape_all()
