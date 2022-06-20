from pymongo import MongoClient
import urllib.parse

if __name__ == "__main__":
    url = "mongodb+srv://rongjin74:" + urllib.parse.quote("A980704@h") +"@cluster0.zyy93.mongodb.net/book_database"
    client = MongoClient(url)
    db = client['book_database']
    db = db['books']
    print(db.count_documents({"title": "Book Lovers"}))

