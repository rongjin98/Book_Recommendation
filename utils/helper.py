import re
import time
import json
from bs4 import BeautifulSoup
from bson import json_util
import urllib.request as request
from json_class.book import Book
from json_class.author import Author
from json_class.genre import Genre
import os



def extract_genre(input_genre):
    temp = input_genre.split("/")
    return temp[-1]

def extract_book(soup, author_url, book_url, extract_method):
    if extract_method:
        print("Extracting Book Vanilla")
        return extract_book_vanila(soup, author_url, book_url)

    print("Extracting Book Neo")
    return extract_book_neo(soup, author_url, book_url)

def get_similar_book_name(similar_books):
    names = set()
    for i in similar_books:
        names.add(i['alt'])
    return list(names)

def get_similar_book_name_author(similar_books):
    names = []
    for i in range(1, len(similar_books)):
        content = similar_books[i].find("span")
        if content and not content.isdigit():
            names.append(content.text)
    return names

#When classic webpage is opened
def extract_book_vanila(soup, author_url, book_url):
    # If book_url, check json_class/book.py for format
    if book_url:
        title_author = soup.title.string.split(" by ")
        book_id = (book_url.split("show/")[1]).split(".")[0]
        title = title_author[0]
        author = title_author[1]

        try:
            img_url = soup.find(property='og:image')['content']
        except:
            img_url = "Unknown"
        
        try:
            isbn = soup.find(property='books:isbn')['content']
        except:
            isbn = "000000"

        rating = soup.find(itemprop='ratingValue')
        if rating is None:
            rating = "Unknown"
            rating_count = "Unknown"
            review_count = "Unknown"
        else:
            rating = rating.string.split('\n')[1]
            rating_count = soup.find(itemprop='ratingCount')['content']
            review_count = soup.find(itemprop='reviewCount')['content']

        similar_books = soup.find(id=re.compile("relatedWorks"))
        if similar_books:
            similar_books = soup.find_all(src=re.compile("https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/"))
            similar_books = get_similar_book_name(similar_books)
        else:
            similar_books = ["Not Available"]
        return Book(title, book_url, book_id, isbn, author_url, author, rating, rating_count,
                review_count, img_url, similar_books)
    
    #If author_url, check json_class/author.py for format

def extract_author(author_url):
    curr_content = request.urlopen(author_url)
    soup = BeautifulSoup(curr_content, "lxml")

    try:
        name = soup.find(property='og:title')['content']
    except:
        name = "Anonymous"
    
    try:
        author_id = soup.find(property="fb:app_id")['content']
    except:
        author_id = "Unavailable"
    
    rating = soup.find(itemprop='ratingValue')
    if rating is None:
        rating = "Unknown"
        rating_count = "Unknown"
        review_count = "Unknown"
    else:
        rating = rating.string
        rating_count = soup.find(itemprop='ratingCount')['content']
        review_count = soup.find(itemprop='reviewCount')['content']
    img_url = soup.find(property='og:image')['content']
    written_books = get_similar_book_name_author(soup.findAll('a', class_ = "bookTitle", limit=5))
    return Author(name, author_url, author_id, rating, rating_count, review_count, img_url,
                  written_books)


#When new JS-Rendered Webpage is opened
def extract_book_neo(soup, author_url, book_url):
    title_author = soup.title.string.split(" by ")
    title = title_author[0]
    author = title_author[1].split(" | ")[0]
    book_id = (book_url.split("show/")[1]).split(".")[0]
    data_collection = soup.find("script", type = "application/ld+json").contents[0]
    data_collection = json.loads(data_collection)

    try:
        img_url = data_collection["image"]
    except:
        img_url = "Unknown"

    #Get isbn
    try:
        isbn = data_collection["isbn"]
    except:
        isbn = "000000"
        print("No isbn available")

    #Get rating
    rating = data_collection["aggregateRating"]["ratingValue"]
    if rating is None:
        rating = "Unknown"
        rating_count = "Unknown"
        review_count = "Unknown"
    else:
        rating_count = data_collection["aggregateRating"]["ratingCount"]
        review_count = data_collection["aggregateRating"]["reviewCount"]
    
    #Get similar
    similar = soup.find(class_="BookPage__relatedTopContent").find_all(class_="BookCard__title")
    if not similar:
        time.sleep(1)
        similar = soup.find(class_="BookPage__relatedTopContent").find_all(class_="BookCard__title")
    similar_books = set()
    for item in similar:
        if not item.text.isdigit():
            similar_books.add(item.text)
    similar_books = list(similar_books)

    return Book(title, book_url, book_id, isbn, author_url, author, rating, rating_count,
                review_count, img_url, similar_books)


def turn_to_dict(var, var_type):
    new_dict = {}
    if var_type == "book":
        new_dict["title"] = var.title
        new_dict["book_id"] = var.book_id
        new_dict["ISBN"] = var.isbn
        new_dict["author"] = var.author
        new_dict["similar_books"] = var.similar_books
        new_dict["book_url"] = var.book_url
    else:
        new_dict['name'] = var.name
        new_dict['author_id'] = var.author_id
        new_dict["author_books"] = var.author_books

    new_dict["author_url"] = var.author_url
    new_dict["image_url"] = var.image_url
    new_dict["rating"] = var.rating
    new_dict["rating_count"] = var.rating_count
    new_dict["review_count"] = var.review_count

    return new_dict


def format_to_genre(book, genre):
    new_dict = {}
    new_dict["genre"] = genre
    new_dict["title"] = book.title
    new_dict["author"] = book.author
    new_dict["book_url"] = book.book_url
    new_dict["author_url"] = book.author_url
    new_dict["rating"] = book.rating
    new_dict["rating_count"] = book.rating_count
    new_dict["review_count"] = book.review_count
    new_dict["image_url"] = book.image_url

    return new_dict

def write_to_path(books, authors, genres, path):
    book_dict = {}
    book_dict['books'] = books
    author_dict = {}
    author_dict['authors'] = authors
    genre_dict = {}
    genre_dict['genres'] = genres
    result = [book_dict, author_dict, genre_dict]
    with open(path, 'w') as f:
        f.write(json_util.dumps(result))

def load_json_to_db(path, result_db):
    with open(path, 'r') as f:
        loaded_result = json.load(f)
        result_db.insert_many(loaded_result)