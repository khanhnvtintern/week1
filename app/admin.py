from sqladmin import Admin, ModelView
from app.models import Book, Author

class BookAdmin(ModelView, model=Book):
    column_list = [Book.id, Book.title,Book.author_id, Book.year, Book.summary]
    # TODO: thêm Book.author, Book.year vào column_list
    name = "Book"
    name_plural = "Books"
class AuthorAdmin(ModelView, model = Author):
    column_list = [Author.id, Author.name]
    name = "Author"
    name_plural = "Authors"

def setup_admin(app,engine):
    admin = Admin(app, title="Books Admin", engine=engine)
    admin.add_view(BookAdmin)
    admin.add_view(AuthorAdmin)
    return admin