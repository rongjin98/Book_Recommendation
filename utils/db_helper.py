import re
import argparse
import requests
import urllib.parse
from pymongo import MongoClient

class DB_Helper:
    def __init__(self, save_dir = "result.json", 
                       home_link = "https://www.goodreads.com", 
                       connect_str = "mongodb+srv://rongjin74:"
                                    + urllib.parse.quote("password") +
                                    "@cluster0.zyy93.mongodb"
                                    ".net/?"
                                    "retryWrites=true&w=majority"):

        self.PARSER = argparse.ArgumentParser(description = 'Parsing Input to Web Scraper')
        self.PARSER.add_argument("--json_file", type = str, default = save_dir)
        self.PARSER.add_argument("--scaped_link", type = str, default = home_link)
        self.PARSER.add_argument("--connect_string", type = str, default = connect_str)
        self.connect_str = connect_str
        self.client = MongoClient(self.connect_str)
    
    def get_arguments(self):
        return self.PARSER.parse_args()
    
    def initalize_db(self, clear_prev = True):
        MY_DB = self.client["book_database"]
        #Remove all previous data
        if MY_DB['results'] is not None and clear_prev:
            MY_DB['books'].delete_many({})
            MY_DB['authors'].delete_many({})
            MY_DB['genres'].delete_many({})
        
        BOOK_DB = MY_DB['books']
        AUTHOR_DB = MY_DB['authors']
        GENRE_DB = MY_DB['genres']
        
        return BOOK_DB, AUTHOR_DB, GENRE_DB
    
    def check_if_unique(self, cur_dict, target_db):
        MY_DB = self.client["book_database"]
        MY_DB = MY_DB[target_db]
        if target_db == 'books':
            title_ = cur_dict['title']
            if MY_DB.count_documents({'title' : title_}) > 0:
                print(f'Book: [{title_}] already exists in DB')
                return False
        elif target_db == 'authors':
            name_ = cur_dict['name']
            if MY_DB.count_documents({'name' : name_}) > 0:
                print(f'Author: [{name_}] already exists in DB')
                return False
        return True

        

