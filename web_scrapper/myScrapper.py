from collections import defaultdict
from utils import helper, db_helper
from bs4 import BeautifulSoup
from collections import defaultdict
from selenium import webdriver


DB_helper = db_helper.DB_Helper()
ARGUMENTS = DB_helper.get_arguments()
FILE_NAME = ARGUMENTS.json_file
HOME_LINK = ARGUMENTS.scaped_link
CONNECTION_STR = ARGUMENTS.connect_string

class MyScrapper:
    #Initialize data base
    def __init__(self, reset = True):
        self.BOOK_DB, self.AUTHOR_DB, self.GENRE_DB = DB_helper.initalize_db(reset)
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
    
    def extract_info_by_genre(self, URLS, DB = False):
        """
        When opening a specific book url, one of two possible webpage will be opened
        1. Vanilla Webpage, which author url can be extracted by "books:author"        (most often 90%)
        2. Latest Webpage, which author url can only be extracted by "ContributorLink" (small-chance 10%)
        For each case, we need a differetn strategy: 
        extract_method = True -> 1, False -> 2
        """
        cnt= 0
        extract_method = True
        GENRES = defaultdict(list)
        for genre_url in URLS:
            url_list = URLS[genre_url]
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
               
                curr_book = helper.extract_book(soup, author_url, book_url, extract_method)
                curr_author = helper.extract_author(author_url)
                curr_genre = helper.format_to_genre(curr_book, genre_name)
                curr_book = helper.turn_to_dict(curr_book, 'book')
                curr_author = helper.turn_to_dict(curr_author, 'author')
                print(curr_author["author_books"])
                browser.quit()
                
                if DB:
                    GENRES[genre_name].append(curr_genre)
                    self.BOOK_DB.insert_one(curr_book)
                    self.AUTHOR_DB.insert_one(curr_author)

                cnt += 1
                if cnt % 20 == 0:
                    print("%2d books have been added" %(cnt))
                
            if DB:
                temp = {}
                temp[genre_name] = GENRES[genre_name]
                self.GENRE_DB.insert_one(temp)
        return 

    def extract_info_by_book(self, book_urls, DB = False, check_duplicate = True):
        BOOKS = []
        for book_url in book_urls:
            extract_method = True
            browser, soup = self.load_webdriver(book_url)
            try:
                author_url = soup.find("meta", property="books:author")['content']
                extract_method = True
            except:
                author_url = soup.find("a", class_ = "ContributorLink")['href']
                extract_method = False
                if not author_url:
                    print("This url is not available")
        
            curr_book = helper.extract_book(soup, author_url, book_url, extract_method)
            curr_author = helper.extract_author(author_url)
            curr_book = helper.turn_to_dict(curr_book, 'book')
            curr_author = helper.turn_to_dict(curr_author, 'author')
            BOOKS.append(curr_book)
            browser.quit()
            if DB:
                if not check_duplicate:
                    self.BOOK_DB.insert_one(curr_book)
                    self.AUTHOR_DB.insert_one(curr_author)
                else:
                    if DB_helper.check_if_unique(curr_book, 'books'):
                        self.BOOK_DB.insert_one(curr_book)
                    if DB_helper.check_if_unique(curr_author, 'authors'):
                        self.AUTHOR_DB.insert_one(curr_author)
        
        return BOOKS