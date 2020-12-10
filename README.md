# MISSION TO MARS

Building a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

***Here is the video of how the websites will be scraped!***

[<img align="center" src="https://img.youtube.com/vi/7Qa42EAzCWk/maxresdefault.jpg" width="100%">](https://youtu.be/7Qa42EAzCWk)

## Sources

- [NASA Mars News](https://mars.nasa.gov/news/)

- [JPL Mars Space Images](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)

- [Mars Facts](https://space-facts.com/mars/)

- [Mars Hemispheres](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)

## Part I - Scraping data

*Accompanied by Jupyter NoteBook* [Click here to view](https://nbviewer.jupyter.org/github/abpuccini/web-scraping-challenge/blob/main/mission_to_mars/mission_to_mars.ipynb) 

### The lasted Mars news title and paragraph

Retrived the latest Mars news title and paragraph and stored them in the variables.

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

Retrived a featured Mars image and stored it in a variable.

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

Retrived Mars fact table and stored it in a variable.

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

Retrived Mars hemispheres name and image url, and stored them in the variables.

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

## Part II - MongoDB and Flask Application

Developed Flask application to render HTML page based on data stored in a database.

### MongoDB 

Scraped websites to retrieve all data that is required, and stored in a dictionary. The dictionary from this step will be used in Flask application. (This code is similar to code in Jupyter Notebook except time.sleep() and appending list which will use to store in the database in the next step)

**Code:** [(see completed code click here)](scrape_mars.py)

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

### Flask application

Developed Flask application to render HTML page by using data store in the previous step. There are two step as following.

**Code:** [(see completed code click here)](app.py)

- Created an Flask application and database connection
        
        # Create an instance of Flask
        app = Flask(__name__)

        # Use PyMongo to establish Mongo connection
        mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

- Home route

        @app.route("/")
        def home():

            # Find one record of data from the mongo database
            mars_data = mongo.db.mars_data.find_one()

            # Return template and data
            return render_template("index.html", mars_data=mars_data)

- Scrape route

        @app.route("/scrape")
        def scrape():

            # Run the scrape function
            mission_data = scrape_mars.scrape_info()

            # Update the Mongo database using update and upsert=True
            mongo.db.mars_data.update({}, mission_data, upsert=True)

            # Redirect back to home page
            return redirect("/")

---
© [Atcharaporn B Puccini](https://www.linkedin.com/in/abpuccini/)
