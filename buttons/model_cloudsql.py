from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)

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
