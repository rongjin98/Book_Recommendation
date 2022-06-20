def add_author_info(_author):
    name = _author['name']
    rating = (_author['rating'], _author['rating_count'])
    author_url = _author['author_url']
    img_url = _author['image_url']
    return [name, rating, img_url, author_url]



def add_book_info(_book):
    author = _book['author']
    title = _book['title']
    img = _book['image_url']
    rating = (_book['rating'],_book['rating_count'])
    book_url = _book['book_url']
    return [author, rating,  img,  title, book_url]

def add_to_dict(result_dict, _info, method):
    if method == 'book':
        result_dict['title'].append(_info[3])
        result_dict['book_url'].append(_info[-1]) 
    else:
        result_dict['author_url'].append(_info[-1])
    result_dict['author'].append(_info[0])
    result_dict['rating'].append(_info[1])
    result_dict['img'].append(_info[2])
    
    
