# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager   #  NOT NEEDED?
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path)
    #### browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in a dictionary
    data = {
        "image_url": image_url,
        "title": title
    }
    # Store old code
    # data = {
    #     "news_title": news_title,
    #     "news_paragraph": news_paragraph,
    #     "featured_image": featured_image(browser),
    #     "facts": mars_facts(),
    #     "hemispheres": hemispheres(browser),
    #     "last_modified": dt.datetime.now()
    # }
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Next executable line checks for specific HTML code and 
    # has optional delay of 1 second for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide') # Selects item_list class of ul tag and slide class of li element
        # See Module 10.3.3 (middle) for more explanation on CSS

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1) # Boolean response confirming target; wait_time provide time to load site
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        # figure.lede looks for the figure tag in the lede class
        # a is the next tag nested inside figure tag
        # img tag also present
        # .get ("src") pulls the link to the image
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():

    try:
        df = pd.read_html('http://space-facts.com/mars/')[0] # read_html returns a list of tables; [0] selects the first table

    except BaseException:
        return None

    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


def hemi_facts():
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls = []
    html=browser.html
    hemi_soup=soup(html, 'html.parser')
    hemi_series=hemi_soup.find('div', class_='collapsible results').find_all(class_='item')
    for hemi_segment in hemi_series:
        path_png = f"https://astrogeology.usgs.gov{hemi_segment.find(class_='thumb').get('src')}"
        title_value = hemi_segment.find(class_='thumb').get('alt')
        new_dict={'image_url':path_png, 'title':title_value} 
        hemisphere_image_urls.append(new_dict)

    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

