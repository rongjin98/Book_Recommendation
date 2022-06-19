from sympy import im


def add_book_info(_book):
    author = _book['author']
    title = _book['title']
    img = _book['image_url']
    rating = _book['rating']
    book_url = _book['book_url']
    return [author, title, img, rating, book_url]

def add_to_book_dict(result_dict, book_info):
    result_dict['author'].append(book_info[0])
    result_dict['title'].append(book_info[1])
    result_dict['img'].append(book_info[2])
    result_dict['rating'].append(book_info[3])
    result_dict['book_url'].append(book_info[4])
