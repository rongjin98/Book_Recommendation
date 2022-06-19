class Book:
    def __init__(self, title, book_url, book_id, isbn, author_url, author,
                 rating, rating_count, review_count, image_url, similar_books):
        self.json_category = "Book"
        self.title = title
        self.book_url = book_url
        self.book_id = book_id
        self.isbn = isbn
        self.author_url = author_url
        self.author = author
        self.rating = rating
        self.rating_count = rating_count
        self.review_count = review_count
        self.image_url = image_url
        self.similar_books = "\n".join(similar_books)