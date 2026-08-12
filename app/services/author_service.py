from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Author
from app.schemas.author import AuthorCreate, AuthorUpdate


def list_authors(db: Session) -> list[Author]:
    authors = db.execute(select(Author).order_by(Author.id)).scalars().all()
    return list(authors)


def get_author(db: Session, author_id: int) -> Author:
    author = db.get(Author,author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def create_author(db: Session, payload: AuthorCreate) -> Author:
    author = Author(
        name=payload.name,
        bio=payload.bio,
        country=payload.country,
        birth_year=payload.birth_year
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def update_author(db: Session, author_id: int, payload: AuthorUpdate) -> Author:
    author = get_author(db,author_id)
    author.name= payload.name
    author.bio= payload.bio
    author.country= payload.country
    author.birth_year= payload.birth_year
    db.commit() 
    db.refresh(author)
    return author


def delete_author(db: Session, author_id: int) -> None:
    author = get_author(db,author_id)
    db.delete(author)
    db.commit()
    return None