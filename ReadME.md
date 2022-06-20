# Book Recommendation System

### 1. Requirement:

1. Flask
2. Bson
3. pymongo
4. MongoDB
5. Selenium
6. Beautiful Soup 4



### 2. Introduction:

1. Use web-scrapper to scrape books info from `google reads`, and save the info in MongoDB cluster
2. Design responsive website UI using HTML, CSS, Bootstrap and Flask
3. Integrate web-scraper with website as the search-engine
4. Apply REST API and CRUD application to the website



### 3. Instruction:

1. Change the **connection_str** in `web_app.py(named as url)` and in  `utils/db_helper.py(named as connect_str)` to your own Mongodb Cluster
2. Manually run `scrape_on_request.py` for initializing database
3. Run `web_app.py`



### 4. Future Improvement:

1. `Selenium and Chromedriver()` is used to handle the issue of zero-scraping during the scraping process, which is proved to be an overkill. Web-scrape by `Selenium` is stable but with slow-speed and popping-up webpage.  One can simply reload the page, if the page can not be scrapped initially. **(Refer the method in `web_scrapper/ScrapeByAuthor.py` )**
2. `website/templates/search_method.html` and `website/pages.py` is constructed in a way makes `ADD ('POST')` have to be applied with `redirect(url_for('pages.recommendation', result_dict = result_dict)) `, which results to a super long suffix of `/recommendation`. **Try to pass value through href, and perform searching in recommendation instead of in search-method**

3. Javascript is completely not used. The Project could be facilitated using JS.