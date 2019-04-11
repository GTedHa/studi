from studi import app
from sqlalchemy import or_, and_
from flask_sqlalchemy import SQLAlchemy


# if set to True(default) Falst-SQLAlchemy will track modifications of object and emit signals.
# This requires extra memory and can be disabled if not needed.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/studi.db'
db = SQLAlchemy(app)


class Note(db.Model):
    column = ['note_id', 'note_name']
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_name = db.Column(db.Text, nullable=False)

    def __init__(self, notename):
        self.note_name = notename

    clauses = db.relationship("Clauses", cascade="all, delete")
    clausePoints = db.relationship('ClausePoints', cascade="all, delete")


class Clauses(db.Model):
    column = ['clause_id', 'note_id', 'title', 'contents']
    clause_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.note_id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    contents = db.Column(db.Text, nullable=False)

    clausePoints = db.relationship('ClausePoints', cascade="all, delete")

    def __init__(self, noteid=None, title=None, contents=None):
        self.note_id = noteid
        self.title = title
        self.contents = contents


class ClausePoints(db.Model):
    column = ['clause_id', 'note_id', 'imp', 'und']
    clause_id = db.Column(db.Integer, db.ForeignKey('clauses.clause_id'), primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.note_id'), nullable=False)
    imp = db.Column(db.Integer, nullable=False, default=0)
    und = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, clauseid=None, noteid=None, imp=0, und=0):
        self.clause_id = clauseid
        self.note_id = noteid
        self.imp = imp
        self.und = und


# Create table (defalut, production = False)
def create_db(Production=False):
    if Production:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/studi.db'
        db.create_all()
        return

    # Create testing DB (test_studi.db)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'
    db.create_all()
    return db

def drop_db(Production=False):
    if Production:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/studi.db'
        db.drop_all()
        return

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'
    db.drop_all()
    return db

# Insert ata to table you want to
def insert_data_to_db(table, model):
    # Id list to return by table
    id_list = {'Clauses': 'clause', 'Note': 'note', 'ClausePoints' : 'clause'}
    db.session.add(model)
    db.session.commit()
    id = getattr(model, id_list[table] + '_id')
    return id


# Get all data from table
def get_all_data_from_db(table):
    """
    :param table: data model object
    :return: (dict) result
    """
    return table.query.all()


# get all data where *args from table
def get_item_from_db(table, *args):
    """
    :param table: data model object
    :param args: condition where you use in 'where' statement
    :return: (dict) result
    """
    args = args[0]
    query = db.session.query(table)
    for attr, value in args.items():
        value = value

        if not isinstance(value, list):
            value = [value]

        or_query = []
        for v in value:
            or_query.append(getattr(table, attr) == v)
        query = query.filter(or_(*or_query))
    items = query.all()
    return items


#delete all data where *args
def delete_data_from_db(table, *args):
    """
    :param table: Data model object (Note, Clause, ClausePoints)
    :param args: condition where you use in 'where' statement
    :return: (dict) result

    ex)
    args = {'note_id' : [1,2], 'note_name' : 'test1'}
    ('note_id' : 1 or 'note_id' : 2) and ('note_name' : 'test1')
    """
    args = args[0]
    query = db.session.query(table)
    for attr, value in args.items():
        value = value

        if not isinstance(value, list):
            value = [value]

        or_query = []
        for v in value:
            or_query.append(getattr(table, attr) == v)
        query = query.filter(or_(*or_query))
    items = query.all()

    for item in items:
        db.session.delete(item)
        db.session.commit()


# delete only one note
def delete_note_and_related_data_from_db(note_id):
    query = db.session.query(Note)
    note = query.filter(getattr(Note, 'note_id') == note_id).one()
    # all() return list []
    db.session.delete(note)
    db.session.commit()


# update data where condition (clause_id, note_id)
def update_data_to_db(table, condition, update_data):
    """
    :param table(object): Data model object (Note, Clause, ClausePoints)
    :param condition(dict): where condition(ex) clause_id or note_id
    :param update_data(dict): update data
    :return: update row's id
    """
    query = db.session.query(table)
    for attr, value in condition.items():
        query = query.filter(getattr(table, attr) == value)

    query.update(update_data)
    db.session.commit()
