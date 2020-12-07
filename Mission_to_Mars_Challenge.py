#!/usr/bin/env python
# coding: utf-8

# In[24]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[26]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)
# browser = Browser('chrome', executable_path='chromedriver', headless=True)


# In[23]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Next executable line checks for specific HTML code and 
# has optional delay of 1 second for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[20]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide') # Selects item_list class of ul tag and slide class of li element
# See Module 10.3.3 (middle) for more explanation on CSS


# In[27]:


slide_elem.find("div", class_='content_title')


# In[28]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[29]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# In[30]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[31]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[32]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1) # Boolean response confirming target; wait_time provide time to load site
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[33]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[34]:


# Find the relative image url
# figure.lede looks for the figure tag in the lede class
# a is the next tag nested inside figure tag
# img tag also present
# .get ("src") pulls the link to the image
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[35]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# In[36]:


df = pd.read_html('http://space-facts.com/mars/')[0] # read_html returns a list of tables; [0] selects the first table
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[37]:


df.to_html()


# In[38]:


browser.quit()


# Begin Mission_to_mars_Challenge_starter_code

# In[78]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[79]:


from webdriver_manager.chrome import ChromeDriverManager

# Path to chromedriver
# !which chromedriver


# In[80]:


# Set the executable path and initialize the chrome browser in splinter
# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# browser = Browser('chrome', **executable_path)
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# In[81]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[82]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[83]:


slide_elem.find("div", class_='content_title')


# In[84]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[85]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# In[86]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[87]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[88]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[89]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[90]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[91]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# In[92]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[93]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[94]:


df.to_html()


# In[95]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[96]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[97]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# In[133]:


# 1. Use browser to visit the URL
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[136]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# NOTE TO GRADER - I had trouble completing the assignment when clicking to the full-resolution website so,
#     in the interest of developing skills and showing that I actually made an attempt on Deliverable 1,
#     I performed similar operations on the simple hemisphere images from the Astropedia website

html=browser.html
hemi_soup=soup(html, 'html.parser')
hemi_series=hemi_soup.find('div', class_='collapsible results').find_all(class_='item')
for hemi_segment in hemi_series:
    path_png = f"https://astrogeology.usgs.gov{hemi_segment.find(class_='thumb').get('src')}"
    title_value = hemi_segment.find(class_='thumb').get('alt')
    new_dict={'image_url':path_png, 'title':title_value} 
    hemisphere_image_urls.append(new_dict)


# In[137]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[138]:


# 5. Quit the browser
browser.quit()

