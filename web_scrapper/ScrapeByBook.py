import re
import requests
from bs4 import BeautifulSoup

class ScrapeByBook:
    def __init__(self, book_limit = 10):
        self.book_limit = book_limit

    def send_request(self, book_url):
        initial_content = requests.get(book_url).content
        soup = BeautifulSoup(initial_content, 'html.parser')
        urls = soup.find("div", id=re.compile("relatedWorks"))
        return urls

    def get_links(self, book_url, num_books = 5):
        links = []
        num_books = min(num_books, self.book_limit)
        
        urls = self.send_request(book_url)
        while not urls:
            print("Re-requesting Webpage")
            urls = self.send_request(book_url)

        print("Request Complete")

        urls = urls.find_all("a", href=re.compile("https://www.goodreads.com/book/show/"), limit=num_books)
        for url in urls:
            curr_url = url['href']
            if curr_url != book_url and curr_url not in links:
                num_books = num_books + 1
                links.append(curr_url)
        return links