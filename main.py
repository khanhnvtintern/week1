from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db, Base, engine, DB_URL
from app.models import Book,Author

from app.admin import setup_admin
from app.database import engine

app = FastAPI(title="booksAPI")


setup_admin(app, engine)
class BookCreate(BaseModel):
    title: str
    author_id: int | None = None
    year : int
    summary : str | None = None
#books: dict[int, Book] = {}

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/books")
def read_books(db : Session = Depends(get_db)):
    ## TODO: return db.query(Book).all()
    return db.query(Book).all()

@app.get("/books/{book_id}")
def read_book(book_id: int, db : Session = Depends(get_db)):
    # TODO: book = db.get(Book, book_id)
    # TODO: nếu book is None → raise HTTPException(status_code=404, detail="Book not found")
    # TODO: return book
    book = db.get(Book, book_id)
    if book is None:
         raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", status_code=201)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    if payload.author_id is not None:
        author = db.get(Author, payload.author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")

    new_book = Book(
        title=payload.title,
        year=payload.year,
        summary=payload.summary,
        author_id=payload.author_id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.put("/books/{book_id}")
def update_book(book_id: int, payload: BookCreate, db: Session = Depends(get_db)):
    # TODO: lấy book theo id; không có → 404
    # TODO: gán title/author/year từ payload; commit; refresh; return
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if payload.author_id is not None : 
        author = db.get(Author, payload.author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
    book.title = payload.title
    book.author_id = payload.author_id  
    book.year = payload.year
    book.summary = payload.summary
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # TODO: lấy book; không có → 404; db.delete; commit; return None
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return None

class AuthorCreate(BaseModel):
    name: str

@app.get("/authors")
def read_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()
@app.get("/authors/{author_id}")
def read_author(author_id : int, db : Session = Depends(get_db)):
    author = db.get(Author,author_id)
    if author is None: 
        raise HTTPException(status_code=404, detail="Author not found")
    return author
@app.post("/authors",status_code=201)
def create_author(payload : AuthorCreate, db : Session = Depends(get_db)):
    new_author = Author(name = payload.name)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author