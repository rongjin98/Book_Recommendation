import re
import requests
import random
import json
from collections import defaultdict
from utils import helper, db_helper
from bs4 import BeautifulSoup
from pymongo import MongoClient
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By

DB_helper = db_helper.DB_Helper()
ARGUMENTS = DB_helper.get_arguments()
BOOK_LIMIT = ARGUMENTS.book_limit
AUTHOR_LIMIT = ARGUMENTS.author_limit
GENRE_LIMIT = ARGUMENTS.genre_limit
FILE_NAME = ARGUMENTS.json_file
HOME_LINK = ARGUMENTS.scaped_link
CONNECTION_STR = ARGUMENTS.connect_string

ALL_URLS = []
AUTHOR_URL = set()
GENRES = defaultdict(list)
BOOKS = []
AUTHORS = []

class MyScrapper:
    #Initialize data base
    def __init__(self, reset = True):
        self.BOOK_DB, self.AUTHOR_DB, self.GENRE_DB, self.RESULT_DB = DB_helper.initalize_db(reset)
        # self.opt = webdriver.ChromeOptions()
        # self.opt.add_argument("disable-popup-blocking")
        # self.opt.add_argument("disable-mediastream")
        # self.opt.add_argument("disable-geolocation")
    
    def load_webdriver(self, url):
        browser = webdriver.Chrome()
        browser.get(url)
        response = browser.page_source
        soup = BeautifulSoup(response, "html.parser")
        return browser, soup



    #return a list of urls with different genres
    def get_genres(self, home_url, num_genres):
        num_genres = 1 if not num_genres else num_genres        #At least 1 genre
        num_genres = min(num_genres, GENRE_LIMIT)               #Can not surpass genre limit
            
        response = requests.get(home_url).content
        soup = BeautifulSoup(response, 'html.parser')
        genres = soup.find_all('a', class_ = "gr-hyperlink", href = re.compile("/genres/"))
        all_collections = []
        for genre in genres:
            all_collections.append(genre['href'])
        return random.sample(all_collections, num_genres)

    #For each genre, choose the top k number of book, k is determined by num_genres & num_book
    def get_all_links(self, genres, num_book = BOOK_LIMIT):
        num_book = 1 if not num_book else num_book          #At least 1 book
        num_book = min(num_book, BOOK_LIMIT)                #Can not surpass book limit
        num_book_per_genre = num_book // len(genres)
        output = defaultdict(list)
        visited = set()

        genre_cnt = 0
        for genre in genres:
            genre_url = HOME_LINK + genre
            response = requests.get(genre_url).content
            soup = BeautifulSoup(response, 'html.parser')

            #Every time scrape 5 more books to avoid repetition books
            book_urls = soup.find_all("a", href = re.compile("/book/show/"), limit = num_book_per_genre + 5)
            for book_url in book_urls:
                if book_url['href'] in visited:
                    continue
                output[genre].append(book_url['href'])
                visited.add(book_url['href'])
                if len(output[genre]) == num_book_per_genre:
                    break
            genre_cnt += 1
            print("%2d out of %2d genres with total number of %2d books have been scraped" %(genre_cnt, len(genres), genre_cnt * num_book_per_genre))

        return output, num_book_per_genre*len(genres)
    
    #extract book_name, author of the book from its url
    def extract_information(self):
        """
        When opening a specific book url, one of two possible webpage will be opened
        1. Vanilla Webpage, which author url can be extracted by "books:author"        (most often 90%)
        2. Latest Webpage, which author url can only be extracted by "ContributorLink" (small-chance 10%)
        For each case, we need a differetn strategy: 
        extract_method = True -> 1, False -> 2
        """
        cnt= 0
        extract_method = True
        for genre_url in ALL_URLS:
            url_list = ALL_URLS[genre_url]
            genre_name = helper.extract_genre(genre_url)
            
            for sub_url in url_list:
                #Bug Case1: book_url is already a full URL
                #To handle the case, use book_url instead of link
                book_url = HOME_LINK + sub_url
                book_url = sub_url if sub_url[0] == "h" else book_url

                #Bug Case2: 'html.parser' can not successfully read the content -> return None
                #Check comment at the beginning of this function
                browser, soup = self.load_webdriver(book_url)
                try:
                    author_url = soup.find("meta", property="books:author")['content']
                    extract_method = True
                except:
                    author_url = soup.find("a", class_ = "ContributorLink")['href']
                    extract_method = False
                    if not author_url:
                        print("This url is not available")
                        continue

                if len(AUTHOR_URL) < AUTHOR_LIMIT:
                    AUTHOR_URL.add(author_url)

                print(extract_method)
                curr_book = helper.extract_book(soup, author_url, book_url, extract_method)
                curr_author = helper.extract_author(author_url)
                curr_genre = helper.format_to_genre(curr_book, genre_name)
                curr_book = helper.turn_to_dict(curr_book, 'book')
                curr_author = helper.turn_to_dict(curr_author, 'author')

                browser.quit()
                
                
                GENRES[genre_name].append(curr_genre)
                BOOKS.append(curr_book)
                AUTHORS.append(curr_author)
                self.BOOK_DB.insert_one(curr_book)
                self.AUTHOR_DB.insert_one(curr_author)
                
                cnt += 1
                if cnt % 20 == 0:
                    print("%2d books have been added" %(cnt))

            temp = {}
            temp[genre_name] = GENRES[genre_name]
            self.GENRE_DB.insert_one(temp)
            

if __name__ == "__main__":
    scraper = MyScrapper(reset=True)
    genres = scraper.get_genres(HOME_LINK, 5)

    ALL_URLS, num_book = scraper.get_all_links(genres, 40)
    scraper.extract_information()
    print("Done Getting Links")

    helper.write_to_path(BOOKS, AUTHORS, GENRES, FILE_NAME)
    print("Done Writing Files")

    helper.load_json_to_db(FILE_NAME, scraper.RESULT_DB)
    print("Done Loading JSON to DB")
