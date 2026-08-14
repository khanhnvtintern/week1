from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Author,Book
from app.schemas.book import BookCreate, BookUpdate, BookRead


def to_book_read(book: Book) -> BookRead:
    return BookRead(
        id=book.id,
        title=book.title,
        year=book.year,
        summary=book.summary,
        author_id=book.author_id,
        author_name=book.author.name if book.author else None,
        )
    

def _ensure_author_exists(db : Session, author_id: int|None) -> None:
    if author_id is None:
        return None
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")


def _get_book_with_author(db: Session, book_id: int) -> Book:
    book = db.execute(
        select(Book).options(joinedload(Book.author)).where(Book.id==book_id)
    ).scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
    

def list_books(db : Session) -> list[BookRead]:
    books = db.scalars(
        select(Book)
        .options(joinedload(Book.author)).order_by(Book.id)).all()
    return [to_book_read(book) for book in books]


def get_book(db: Session, book_id: int) -> BookRead:
    return to_book_read(_get_book_with_author(db, book_id))


def create_book(db : Session, payload : BookCreate) -> BookRead:
    _ensure_author_exists(db, payload.author_id)
    new_book = Book(
    title=payload.title,
    year=payload.year,
    summary=payload.summary,
    author_id=payload.author_id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    book = _get_book_with_author(db, new_book.id)
    return to_book_read(book)
    
    
def update_book(db : Session, book_id : int, payload : BookUpdate) -> BookRead: 
    book = _get_book_with_author(db, book_id)
    
    _ensure_author_exists(db, payload.author_id)
    
    book.title = payload.title
    book.year = payload.year
    book.summary = payload.summary
    book.author_id = payload.author_id
    db.commit()
    
    book = _get_book_with_author(db, book_id)
    return to_book_read(book)


def delete_book(db : Session, book_id : int) -> None:
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return None


def list_books_by_author(db: Session, author_id: int) -> list[BookRead]:
    _ensure_author_exists(db, author_id)
    
    books = db.scalars(
        select(Book)
        .options(joinedload(Book.author))
        .where(Book.author_id==author_id)
        .order_by(Book.id)
    ).all()
    return [to_book_read(book) for book in books]
