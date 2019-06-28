# Dependencies
import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

def scrape_text():
   executable_path = {'executable_path': 'chromedriver.exe'}
   browser = Browser('chrome', **executable_path, headless=False)

   url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
   browser.visit(url)

   html = browser.html
   soup = bs(html, 'html.parser')
   title = news_title(soup)
   paragraph= news_paragraph(soup)
   image= browser_images()
   weather= browser_weather()
   facts= browser_facts()
   hemispheres= browser_hemispheres()

   dict_news ={'title_1': title, 'paragraph_1': paragraph, 'image_1': image, 'weather_1':weather, 'facts_1': facts, 'hemispheres_1': hemispheres}
   return dict_news
   
def news_title(soup_obj):
   news_title=[]
   for link in soup_obj.find_all('div', class_='content_title'):
      news_title.append(link.get_text())
      news_title_last=news_title[0]
   return news_title_last

def news_paragraph(soup_obj):
   news_p=[]
   for link in soup_obj.find_all('div', class_='article_teaser_body'):
      news_p.append(link.get_text())
   news_p_last=news_p[0]
   return news_p_last

# JPL Mars Space Images - Featured Image
def browser_images():
   executable_path = {'executable_path': 'chromedriver.exe'}
   browser = Browser('chrome', **executable_path, headless=False)
   url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
   browser.visit(url_2)

   html = browser.html
   soup = bs(html, 'html.parser')

   image = soup.find_all('a', class_='button fancybox')
   featured_image_url= 'http://www.jpl.nasa.gov'+ image[0]['data-fancybox-href']
   return featured_image_url

# # Mars Weather
def browser_weather():
   executable_path = {'executable_path': 'chromedriver.exe'}
   browser = Browser('chrome', **executable_path, headless=False)
   url_3 = 'https://twitter.com/marswxreport?lang=en'
   browser.visit(url_3)

   html = browser.html
   soup = bs(html, 'html.parser')

   mars_weather=[]
   for link in soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'):
      mars_weather.append(link.get_text())
      mars_weather_last= mars_weather[0]
      return mars_weather_last

# # Mars Facts
def browser_facts():
   url_4 = 'https://space-facts.com/mars/'
   tables = pd.read_html(url_4)
   df = tables[0]
   df.columns = ['Parameters', 'Meassures']
   return df.to_html(classes="table table-striped")

# # Mars Hemispheres

def browser_hemispheres():
   executable_path = {'executable_path': 'chromedriver.exe'}
   browser = Browser('chrome', **executable_path, headless=False)
   url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
   browser.visit(url_5)

   html = browser.html
   soup = bs(html, 'html.parser')

   hemispheres = soup.find_all('a', class_='itemLink product-item')

   list_links= []
   array_length = len(hemispheres)
   for i in range(array_length):
      list_links.append(hemispheres[i]['href'])
   
   list_names=[]
   for link in soup.find_all('a', class_='itemLink product-item'):
      list_names.append(link.get_text())
   
   dictionary = dict(zip(list_names, list_links))
   return dictionary

