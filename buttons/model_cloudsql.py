from flask import Flask
from flask_sqlalchemy import SQLAlchemy

builtin_list = list
db = SQLAlchemy()

def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)

def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

class Button(db.Model):
    __tablename__ = 'buttons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    imageUrl = db.Column(db.String(255))

    def __repr__(self):
        return "<Button %r>" % self.name

    #comparisonId = db.Column(db.Integer, primary_key=True)
    #leftButtonId = db.Column(db.Integer)
    #leftButtonImageUrl = db.Column(db.String(255))
    #rightButtonId = db.Column(db.Integer)
    #rightButtonImageUrl = db.Column(db.String(255))

        
def read(id):
    result = Button.query.get(id)
    if not result:
        return None
    return from_sql(result)

def list(comparison = 1):
    query = '''select c.id as comparisonId, bl.id as leftButtonId, bl.imageUrl as leftButtonImageUrl, br.id as rightButtonId, br.imageUrl as rightButtonImageUrl
            from comparisons c
            join buttons bl
                on c.leftButtonName = bl.name
            join buttons br
                on c.rightButtonName = br.name
            where c.order = {0}'''.format(comparison)
    result = db.engine.execute(query)
    
    buttons = {}
    
    for row in result:
        for tup in row.items():
            buttons = {**buttons, **{tup[0]: tup[1]}}

    return (buttons)
	
#class Book(db.Model):
#    __tablename__ = 'books'
#
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(255))
#    author = db.Column(db.String(255))
#    publishedDate = db.Column(db.String(255))
#    imageUrl = db.Column(db.String(255))
#    description = db.Column(db.String(4096))
#    createdBy = db.Column(db.String(255))
#    createdById = db.Column(db.String(255))
#
#    def __repr__(self):
#        return "<Book(title='%s', author=%s)" % (self.title, self.author)

#def list(limit=10, cursor=None):
#    cursor = int(cursor) if cursor else 0
#    query = (Book.query
#             .order_by(Book.title)
#             .limit(limit)
#             .offset(cursor))
#    books = builtin_list(map(from_sql, query.all()))
#    next_page = cursor + limit if len(books) == limit else None
#    return (books, next_page)

def list_by_user(user_id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Book.query
             .filter_by(createdById=user_id)
             .order_by(Book.title)
             .limit(limit)
             .offset(cursor))
    books = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)

#def read(id):
#    result = Book.query.get(id)
#    if not result:
#        return None
#    return from_sql(result)

def create(data):
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return from_sql(book)

def update(data, id):
    book = Book.query.get(id)
    for k, v in data.items():
        setattr(book, k, v)
    db.session.commit()
    return from_sql(book)

def delete(id):
    Book.query.filter_by(id=id).delete()
    db.session.commit()

if __name__ == '__main__':
    _create_database()
