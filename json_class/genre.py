class Genre:
    def __init__(self, genre, title, book_url, author_url, author,
                 rating, rating_count, review_count):
        self.json_category = "Genre"
        self.genre = genre
        self.title = title
        self.book_url = book_url
        self.author_url = author_url
        self.image_url = image_url
        self.author = author
        self.rating = rating
        self.rating_count = rating_count
        self.review_count = review_count