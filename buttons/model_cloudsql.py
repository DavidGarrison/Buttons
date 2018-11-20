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

        
#def read(id):
#    result = Button.query.get(id)
#    if not result:
#        return None
#    return from_sql(result)

def list(sessionId):
    query = '''select c.id as comparisonId,
                bl.id as leftButtonId,
                bl.imageUrl as leftButtonImageUrl,
                bl.pressedImageUrl as leftButtonPressedImageUrl,
                br.id as rightButtonId,
                br.imageUrl as rightButtonImageUrl,
                br.pressedImageUrl as rightButtonPressedImageUrl
            from comparisons c
            join buttons bl
                on c.leftButtonName = bl.name
            join buttons br
                on c.rightButtonName = br.name
            where c.order = IFNULL((
                select max(c.order) + 1
                from trials t
                join comparisons c on t.comparisonId = c.id
                where t.sessionId = {0})
                ,1)'''.format(sessionId)
    result = db.engine.execute(query)
    
    buttons = {}
    
    for row in result:
        for tup in row.items():
            buttons = {**buttons, **{tup[0]: tup[1]}}

    return (buttons)

def buttonPress(sessionId, comparisonId, buttonId):
    query = '''INSERT INTO trials (sessionId, comparisonId, buttonPressedId, datetime, durationInSeconds)
                SELECT
					{0},
					{1},
					{2},
					now(),
					timestampdiff(second,IFNULL((select datetime from trials where sessionId = {0} and comparisonId = {1} - 1 limit 1),(select startdatetime from session where id = {0})) , now())
				WHERE NOT EXISTS (
					SELECT 1 FROM trials where sessionId = {0} and comparisonId = {1});'''.format(sessionId, comparisonId, buttonId)
                
    db.engine.execute(query)
    
def createSession():
    queryInsert = 'insert into session(startdatetime) values (now());'
    querySelect = 'select last_insert_id();'
    
    db.engine.execute(queryInsert)
    
    result = db.engine.execute(querySelect)
    
    session = 0
    
    for row in result:
        for tup in row.items():
            session = tup[1]

    return session


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
