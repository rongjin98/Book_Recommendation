import re
import requests
import random
from collections import defaultdict
from bs4 import BeautifulSoup
from collections import defaultdict

class ScrapeByGenre:
    #Initialize data base
    def __init__(self, genre_limit = 20, book_limit = 200):
        self.genre_limit = genre_limit
        self.book_limit = book_limit
        self.home_link = "https://www.goodreads.com"


    #return a list of urls with different genres
    def get_genres(self, num_genres):
        num_genres = 1 if not num_genres else num_genres        #At least 1 genre
        num_genres = min(num_genres, self.genre_limit)               #Can not surpass genre limit
            
        response = requests.get(self.home_link).content
        soup = BeautifulSoup(response, 'html.parser')
        genres = soup.find_all('a', class_ = "gr-hyperlink", href = re.compile("/genres/"))
        all_collections = []
        for genre in genres:
            all_collections.append(genre['href'])
        return random.sample(all_collections, num_genres)

    #For each genre, choose the top k number of book, k is determined by num_genres & num_book
    def get_all_links(self, genres, num_book = 5):
        num_book = len(genres) if not num_book else num_book          #At least 1 book
        num_book = min(num_book, self.book_limit)                #Can not surpass book limit
        num_book_per_genre = num_book // len(genres)
        output = defaultdict(list)
        visited = set()

        genre_cnt = 0
        for genre in genres:
            genre_url = self.home_link + genre
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

        return output
            

# if __name__ == "__main__":
#     scraper = MyScrapper(reset=True)
#     genres = scraper.get_genres(HOME_LINK, 5)

#     ALL_URLS, num_book = scraper.get_all_links(genres, 40)
#     scraper.extract_information()
#     print("Done Getting Links")

#     helper.write_to_path(BOOKS, AUTHORS, GENRES, FILE_NAME)
#     print("Done Writing Files")

#     helper.load_json_to_db(FILE_NAME, scraper.RESULT_DB)
#     print("Done Loading JSON to DB")
