from flask import Blueprint, request, render_template, flash
from .database import mongo_db

home_view = Blueprint('views', __name__)
@home_view.route('/', methods = ['GET', 'POST'])
def home():
    # if request.method == 'GET':
    #     genres = mongo_db.db.genres.find()
    #     genre_list = []
    #     for genre_ in genres:
    #         for key in genre_.keys():
    #             if key != '_id':
    #                 genre_list.append(key)

    return render_template("home_page.html")