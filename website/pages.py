from flask import Blueprint, render_template, request, flash, jsonify
from flask import redirect, url_for
from .database import mongo_db
from utils import api_helper

pages = Blueprint('pages', __name__)
@pages.route('/genres', methods=['GET', 'POST'])
def genres():
    genres = mongo_db.db.genres.find()
    if request.method == 'GET':
        genre_list = []
        num_books = 0
        for genre_ in genres:
            for key in genre_.keys():
                if key != '_id':
                    genre_list.append(key)
                    if not num_books:
                        num_books = len(genre_[key])
        return render_template("search_method.html", method = 'genres', genres = genre_list, num_books = num_books)

    if request.method == 'POST':
        selected_genre = request.form.get("select_genre")
        num_books = int(request.form.get("myRange"))
        if not num_books:
            num_books = 1
            flash("At least one book will be recommended", category='error')

        book_lists = None
        for genre_ in genres:
            if selected_genre in genre_.keys():
                book_lists = genre_[selected_genre]
                break
            else:
                continue
        
        result_dict = {'author':[], 'title':[], 'img':[], 'rating':[], 'book_url':[], 'len':[num_books]}
        for i in range(num_books):
            book_info = api_helper.add_book_info(book_lists[i])
            api_helper.add_to_book_dict(result_dict, book_info)
        flash("These are the books we recommend based on your chosed genre", category='success')
        return render_template("recommendation.html", result_dict = result_dict)

@pages.route('/books', methods=['GET', 'POST'])
def books():
    # if request.method == 'GET':
    return render_template("search_method.html", method = 'Books', num_books = 5)

@pages.route('/authors', methods=['GET', 'POST'])
def authors():
    # if request.method == 'GET':
    return render_template("search_method.html", method = 'Authors', num_books = 5)


@pages.route('/bookshelf', methods = ['GET', 'POST'])
def bookshelf():
    if request.method == 'GET':
        result_dict = {'author':[], 'title':[], 'img':[], 'rating':[], 'book_url':[], 'len':[]}
        _books = mongo_db.db.books.find()
        cnt = 0
        for _book in _books:
            book_info = api_helper.add_book_info(_book)
            api_helper.add_to_book_dict(result_dict, book_info)
            cnt += 1
            # authors.append(_book['author'])
            # titles.append(_book['title'])
            # img_urls.append(_book['img_url'])
            # ratings.append(_book['rating'])
        result_dict['len'].append(cnt)
    return render_template("recommendation.html", result_dict = result_dict)


@pages.route('/dashboard', methods = ['GET', 'POST'])
def library():
    return render_template("base.html")