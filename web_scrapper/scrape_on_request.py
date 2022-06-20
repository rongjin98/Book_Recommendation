from .ScrapeByAuthor import ScrapeByAuthor
from .ScrapeByBook import ScrapeByBook
from .ScrapeByGenre import ScrapeByGenre
from .myScrapper import MyScrapper

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
    book_url = "https://www.goodreads.com/book/show/58690308-book-lovers"
    author_url = "https://www.goodreads.com/author/show/13905555.Emily_Henry"

    scrape_by_book(2, book_url)
    print("Done scraping by book")

    scrape_by_author(2, author_url)
    print("Done scraping by author")