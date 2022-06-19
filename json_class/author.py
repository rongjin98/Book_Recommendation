class Author:
    def __init__(self, name, author_url, author_id,
                 rating, rating_count, review_count, image_url, author_books):
        self.json_category = "Author"
        self.name = name
        self.author_url = author_url
        self.author_id = author_id
        self.rating = rating
        self.rating_count = rating_count
        self.review_count = review_count
        self.image_url = image_url
        self.author_books = "\n".join(author_books)