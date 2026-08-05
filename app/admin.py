from sqladmin import Admin, ModelView
from app.models import Book

class BookAdmin(ModelView, model=Book):
    column_list = [Book.id, Book.title, Book.author, Book.year]
    # TODO: thêm Book.author, Book.year vào column_list
    name = "Book"
    name_plural = "Books"
    
def setup_admin(app,engine):
    admin = Admin(app, title="Books Admin", engine=engine)
    admin.add_view(BookAdmin)
    return admin