function addBook(img, title_, author, rating, cnt) {
    window.print(img, title_, author, rating, cnt)
    fetch("/add-books", {
      method: "POST",
      body: JSON.stringify({title_: [title_]}),
    });
    
  }