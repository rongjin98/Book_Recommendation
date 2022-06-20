import re
import requests
from bs4 import BeautifulSoup

class ScrapeByAuthor:
    def __init__(self, book_limit = 10):
        self.book_limit = book_limit
        self.home_link = "https://www.goodreads.com"
    
    def send_request(self, author_url, num_books):
        initial_content = requests.get(author_url).content
        soup = BeautifulSoup(initial_content, 'html.parser')
        urls = soup.find_all("tr", itemtype = "http://schema.org/Book", limit=num_books)
        return urls

    def get_links(self, author_url, num_books = 5):
        links = []
        num_books = min(num_books, self.book_limit)
        urls = self.send_request(author_url, num_books)
        while not urls:
            print("Re-requesting Webpage")
            urls = self.send_request(author_url, num_books)

        print("Request Complete")

        for url in urls:
            url = url.find("a", href=re.compile("/book/show/"))
            complete_url = self.home_link + url['href'] if url['href'][0] != 'h' else url['href']
            links.append(complete_url)
        return links

if __name__ == "__main__":
    scrapper = ScrapeByAuthor()
    url = "https://www.goodreads.com/author/show/4039811.Veronica_Roth"
    scrapper.get_links(url, 5)