import re
import argparse
import requests
import urllib.parse
from pymongo import MongoClient

class DB_Helper:
    def __init__(self, book_limit = 200,
                       author_limit = 200, 
                       genre_limit = 10, 
                       save_dir = "result.json", 
                       home_link = "https://www.goodreads.com", 
                       connect_str = "mongodb+srv://rongjin74:"
                                    + urllib.parse.quote("A980704@h") +
                                    "@cluster0.zyy93.mongodb"
                                    ".net/?"
                                    "retryWrites=true&w=majority"):

        self.PARSER = argparse.ArgumentParser(description = 'Parsing Input to Web Scraper')
        self.PARSER.add_argument("--book_limit", type = int, default = book_limit)
        self.PARSER.add_argument("--author_limit", type = int, default = author_limit)
        self.PARSER.add_argument("--genre_limit", type = int, default = genre_limit)
        self.PARSER.add_argument("--json_file", type = str, default = save_dir)
        self.PARSER.add_argument("--scaped_link", type = str, default = home_link)
        self.PARSER.add_argument("--connect_string", type = str, default = connect_str)
        self.connect_str = connect_str
    
    def get_arguments(self):
        return self.PARSER.parse_args()
    
    def connect_to_db(self):
        return MongoClient(self.connect_str)
    
    def initalize_db(self, clear_prev = True):
        CLIENT = self.connect_to_db()
        MY_DB = CLIENT["book_database"]
        #Remove all previous data
        if MY_DB['results'] is not None and clear_prev:
            MY_DB['books'].delete_many({})
            MY_DB['authors'].delete_many({})
            MY_DB['results'].delete_many({})
            MY_DB['genres'].delete_many({})
        
        BOOK_DB = MY_DB['books']
        AUTHOR_DB = MY_DB['authors']
        GENRE_DB = MY_DB['genres']
        RESULT_DB =  MY_DB['results']
            
        
        return BOOK_DB, AUTHOR_DB, GENRE_DB, RESULT_DB

