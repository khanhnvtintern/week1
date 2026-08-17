from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate


def list_categories(db: Session) -> list[Category]:
    categories = db.scalars(
        select(Category)
        .order_by(Category.id)
    ).all()
    return list(categories)


def get_category(db: Session, category_id: int) -> Category:
     category = db.get(Category, category_id)
     if category is None:
         raise HTTPException(status_code=404, detail="Category not found")
     return category


def create_category(db: Session, payload: CategoryCreate) -> Category:
    new_category = Category(
        name=payload.name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def update_category(db: Session, category_id: int, payload: CategoryUpdate) -> Category:
    category = get_category(db, category_id)
    category.name = payload.name
    db.commit()
    return category


def delete_category(db: Session, category_id: int) -> None:
    category = get_category(db, category_id)
    db.delete(category)
    db.commit()
    return None
    