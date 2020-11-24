from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    # The path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    mars_data = {}

    # Visit NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Retrieve the latest title
    news_title = soup.select_one('div.content_title a').text

    # Store result in mars_data dictionary
    mars_data['news_title'] = news_title

    # Retrieve the latest paragraph
    news_p = soup.select_one('div.article_teaser_body').text

    # Store result in mars_data dictionary
    mars_data['news_p'] = news_p

    # Visit JPL Mars Space Images - Featured Image
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    time.sleep(1)

    # Find the full image botton and click
    img_elem = browser.find_by_id('full_image')
    img_elem.click()

    # Find the more info button and click
    browser.is_element_present_by_text('more info', wait_time=3)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the html result with soup
    img_html = browser.html
    img_soup = bs(img_html, 'html.parser')

    # Find the relative image url
    img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    mars_data['img_url'] = img_url

    # URL
    facts_url = 'https://space-facts.com/mars/'

    # Read html by Pandas
    tables = pd.read_html(facts_url)

    # Slice off dataframes that needed
    mars_df = tables[0]

    # Set columns
    mars_df.columns = ['Description', 'Mars']
    mars_df.set_index('Description', inplace=True)

    # Extract table to html
    mars_html = mars_df.to_html(
        classes="dataframe table table-striped, table-bordered table-hover")

    # Store result in mars_data dictionary
    mars_data['facts'] = mars_html

    # Mars Hemispheres
    hem_list = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']
    hemisphere_image_urls = []

    for hem in hem_list:
        # Visit URL
        hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hem_url)

        time.sleep(1)

        # Find the hemisphere images and click
        hem_elem = browser.links.find_by_partial_text(hem)
        hem_elem.click()

        time.sleep(1)

        # Find original to download full img
        hem_elem_org = browser.find_by_text("Original", wait_time=1)
        hem_elem_org.click()

        time.sleep(1)

        # Scrape the Mars website
        hem_html = browser.html
        hem_soup = bs(hem_html, 'html.parser')

        hem_title = hem_soup.h2.text
        hem_url = hem_soup.select_one('li a')['href']

        hem_dict = {
            'title': hem_title,
            'img_url': hem_url
        }

        hemisphere_image_urls.append(hem_dict)

    # Store result in mars_data dictionary
    mars_data['hemisphere'] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
