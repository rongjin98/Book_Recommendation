from web_scrapper import ScrapeByAuthor
from web_scrapper import ScrapeByGenre
from web_scrapper import ScrapeByBook
from myScrapper import MyScrapper

def scrape_by_genre(num_genres, num_books, reset):
    genre_scraper = ScrapeByGenre()
    genre_urls = genre_scraper.get_genres(num_genres)
    book_urls = genre_scraper.get_all_links(genre_urls, num_books)

    my_scrapper = MyScrapper(reset=reset)
    books = my_scrapper.extract_info_by_genre(book_urls, DB=True)
    return books

def scrape_by_book(num_books, book_url):
    book_scraper = ScrapeByBook()
    book_urls = book_scraper.get_links(book_url, num_books)

    my_scrapper = MyScrapper(reset=False)
    books = my_scrapper.extract_info_by_book(book_urls, DB=True)
    return books

def scrape_by_author(num_books, author_url):
    author_scraper = ScrapeByAuthor()
    book_urls = author_scraper.get_links(author_url, num_books)

    my_scrapper = MyScrapper(reset=False)
    books = my_scrapper.extract_info_by_book(book_urls, DB=True)
    return books

if __name__ == "__main__":
    scrape_by_genre(10, 200, reset=True)