

# Dependencies
from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    return browser    

def scrape():
    # browser = Browser('chrome', executable_path="chromedriver", headless=False)
    browser = init_browser()
   

    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')


    # find the title
    list_options = soup.find_all('div', class_='list_text')
    news_title = list_options[0].a.text
    print(news_title)
    #find paragraph
    # paragraph_options = soup.find_all('div', class_='list_text')
    news_p = list_options[0].get_text()
    print(news_p)
    
    time.sleep(2)


    # URL of page to be scraped

    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url_jpl)
    browser.click_link_by_partial_text('FULL IMAGE')

    html = browser.html
    soup = bs(html, 'html.parser')

    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, 'html.parser')
    feature_image = soup.find('img', class_ ='main_image')['src'] 
    feature_image 

    featured_image_url = 'https://www.jpl.nasa.gov' + feature_image  

    featured_image_url
    time.sleep(2)


    url_3 = 'https://space-facts.com/mars/'

    tables = pd.read_html(url_3)
    mars_df = tables[0]
    mars_df.columns=['Variable', 'Value']
    print(mars_df)




    mars_to_html = mars_df.to_html()
    print(mars_to_html)
    time.sleep(2)
    # mars_to_html.replace('\n', '')




    # URL of page to be scraped

    url_mars_img = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url_mars_img)

    html = browser.html
    soup = bs(html, 'html.parser')


    #get titles
    hemisphere_titles =[]
    all_titles = soup.find_all('div', class_='collapsible results')
    title = all_titles[0].find_all('h3')
    title
    for i in title:
        hemisphere_titles.append(i.text)

    hemisphere_titles

    #find urls
    img_group = all_titles[0].find_all('a')
    img_links = []

    for img in img_group:
        if(img.img):
            img_url = 'https://astroleology.usgs.gov/' + img['href']

            img_links.append(img_url)
    img_links




    #place in dict
    hemisphere_image_urls = pd.DataFrame({
            'titles': [],
            'image_url': []
        })

    for place in range(len(img_links)):
        hemisphere_singles = pd.DataFrame({
            'titles': [hemisphere_titles[place]],
            'image_url': [img_links[place]]
        })
        hemisphere_image_urls = hemisphere_image_urls.append(hemisphere_singles)
        
    hemisphere_image_urls
    time.sleep(2)

    mars_facts = {
        
        'titles': news_title,
        'paragraph': news_p,
        'images': featured_image_url,
        'mars_facts': mars_to_html,
        'hemi_images': hemishpere_image_urls

    }
    
    browser.quit()
    print(mars_facts)
    return browser

if __name__ == "__main__":
    scrape()









  





