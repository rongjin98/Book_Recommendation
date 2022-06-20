from website import create_app
import urllib.parse

url = "mongodb+srv://rongjin74:" + urllib.parse.quote("<password>") +"@cluster0.zyy93.mongodb.net/book_database"
app = create_app(url)

if __name__ == "__main__":
    app.run(debug=True)