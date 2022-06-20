import json
from flask import Blueprint, render_template, request, flash, jsonify
from flask import redirect, url_for
from .database import mongo_db
from utils import api_helper
from web_scrapper import scrape_on_request
from bson.objectid import ObjectId


pages = Blueprint('pages', __name__)
BOOKSHELF = []

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
            api_helper.add_to_dict(result_dict, book_info, 'book')
        flash("These are the books we recommend based on your chosed genre", category='success')
        result_dict = json.dumps(result_dict)
        return redirect(url_for('pages.recommendation', result_dict = result_dict))

@pages.route('/books', methods=['GET', 'POST'])
def books():
    # if request.method == 'GET':
    return render_template("search_method.html", method = 'Books')

@pages.route('/authors', methods=['GET', 'POST'])
def authors():
    if request.method == 'GET':
        authors = mongo_db.db.authors.find().limit(40)
        num_authors = 0
        result_dict = {'author':[], 'img':[], 'rating':[], 'author_url':[], 'len':[]}
        for author in authors:
            author_info = api_helper.add_author_info(author)
            api_helper.add_to_dict(result_dict, author_info, 'author')
            num_authors += 1
        result_dict['len'].append(num_authors)
        flash("These are the authors we have in our database", category='success')
        return render_template("search_method.html", result_dict = result_dict, method = 'Authors', num_books = 5)

    if request.method == 'POST':
        author_info = request.form.get("author_url")
        author_url, author = author_info.split("@")
        DefualtAmount = 5

        book_lists = mongo_db.db.books.find({"author":author}).limit(5)
        cnt = 0 
        result_dict = {'author':[], 'title':[], 'img':[], 'rating':[], 'book_url':[], 'len':[]}
        for book in book_lists:
            book_info = api_helper.add_book_info(book)
            api_helper.add_to_dict(result_dict, book_info, 'book')
            cnt += 1
        
        if cnt >= 5:
            result_dict['len'].append(cnt)
            result_dict = json.dumps(result_dict)
            return redirect(url_for('pages.recommendation', result_dict = result_dict))
        else:
            book_lists = scrape_on_request.scrape_by_author(DefualtAmount - cnt, author_url)
            for i in range(len(book_lists)):
                book_info = api_helper.add_book_info(book_lists[i])
                api_helper.add_to_dict(result_dict, book_info, 'book')
            result_dict['len'].append(len(result_dict['title']))
        result_dict = json.dumps(result_dict)
        return redirect(url_for('pages.recommendation', result_dict = result_dict))



@pages.route('/bookshelf', methods = ['GET', 'POST'])
def bookshelf():
    if request.method == 'GET':
        result_dict = {'author':[], 'title':[], 'img':[], 'rating':[], 'book_url':[], 'len':[]}
        _books = mongo_db.db.books.find()
        cnt = 0
        for _book in _books:
            book_info = api_helper.add_book_info(_book)
            api_helper.add_to_dict(result_dict, book_info,'book')
            cnt += 1
        result_dict['len'].append(cnt)
    return render_template("recommendation.html", result_dict = result_dict)


@pages.route('/dashboard', methods = ['GET', 'POST'])
def library():
    if request.method == 'POST':
        book_id = request.form.get("book_info")
        mongo_db.db.book_shelf.delete_one({'_id': ObjectId(book_id)})
        flash("Book Reomved", category='success')
    
    books = mongo_db.db.book_shelf.find()
    book_list = []
    for book_ in books:
        id = None
        for key in book_.keys():
            if key == "_id":
                id = book_[key]
            else:
                url, image = book_[key]
                book_list.append((key, url, image, id))
    return render_template("dashboard.html", num_books = len(book_list), book_list=book_list)

@pages.route('/recommendation', methods = ['GET'])
def recommendation():
    result_dict = request.args.get('result_dict')
    result_dict = json.loads(result_dict)
    return render_template("recommendation.html", result_dict = result_dict)

@pages.route('/add-book', methods = ['POST'])
def add_book():
    book_info = request.form.get("book_info")
    book_info = book_info.split('@')
    book_info = {book_info[0]: (book_info[1], book_info[2])}
    if mongo_db.db.book_shelf.count_documents(book_info) == 0:
        mongo_db.db.book_shelf.insert_one(book_info)
        flash("Book is added to dashboard", category='success')
    flash("Book already exists", category='error')
    return ('', 204)
