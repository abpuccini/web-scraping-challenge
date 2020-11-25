# MISSION TO MARS

## Background

Building a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

## Sources

- [NASA Mars News](https://mars.nasa.gov/news/)

- [JPL Mars Space Images](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)

- [Mars Facts](https://space-facts.com/mars/)

- [Mars Hemispheres](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)

## Part I: Scraping data

***Accompanied by Jupyter NoteBook*** [Click here to view](https://nbviewer.jupyter.org/github/abpuccini/web-scraping-challenge/blob/main/mission_to_mars.ipynb) 

### The lasted Mars news title and paragraph

Retrived the latest Mars news title and paragraph and store them in the variables.

**Source:** [NASA Mars News](https://mars.nasa.gov/news/)

**Code:**

    # Visit URL
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Parse the html result with soup 
    html = browser.html
    soup = bs(html, 'html.parser')

    # Retrieve the latest news title and paragraph
    news_title = soup.select_one('div.content_title a').text
    news_p = soup.select_one('div.article_teaser_body').text

### Featured Mars Image

Retrived a featured Mars image and store it in a variable.

**Source:** [JPL Mars Space Images](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)

**Code:**

    # Visit URL
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

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

### Mars Facts

Retrived Mars fact table and store it in a variable.

**Source:** [Mars Facts](https://space-facts.com/mars/)

**Code:**

    # URL
    facts_url = 'https://space-facts.com/mars/'

    # Read html by Pandas
    tables = pd.read_html(facts_url)

    # Slice off dataframes that needed
    mars_df = tables[0]

    # Set columns
    mars_df.columns = ['Description', 'Mars']
    mars_df.set_index('Description', inplace=True)

    mars_html = mars_df.to_html()

### Mars Hemispheres

**Source:** [Mars Hemispheres](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)

**Code:**

    hem_list = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']
    hemisphere_image_urls = []

    for hem in hem_list:
        # Visit URL
        hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hem_url)
        
        # Find the hemisphere images and click
        hem_elem = browser.links.find_by_partial_text(hem)
        hem_elem.click()
        
        # Find original to download full img
        hem_elem_org = browser.find_by_text("Original", wait_time=1)
        hem_elem_org.click()
        
        # Scrape the Mars website 
        hem_html = browser.html
        hem_soup = bs(hem_html, 'html.parser')
        
        # Retrive Mars Hemisphere name
        hem_title = hem_soup.h2.text

        # Retrive Mars Hemisphere img url
        hem_url = hem_soup.select_one('li a')['href']
        
        # Store result in a dictionary
        hem_dict = {
            'title': hem_title,
            'img_url': hem_url
        }
        
        # Store a dictionary in a list
        hemisphere_image_urls.append(hem_dict)

