from studi import app
from studi import module_path
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


class Clauses(db.Model):
    column = ['clause_id', 'note_id', 'title', 'contents']
    clause_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.note_id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    contents = db.Column(db.Text, nullable=False)

    # setting for foreignkey
    Note = db.relationship('Note', backref=db.backref('clauses', lazy=True))

    def __init__(self, noteid, title, contents):
        self.note_id = noteid
        self.title = title
        self.contents = contents


class ClausePoints(db.Model):
    column = ['clause_id', 'note_id', 'imp', 'und']
    clause_id = db.Column(db.Integer, db.ForeignKey('clauses.clause_id'), primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.note_id'), nullable=False)
    imp = db.Column(db.Integer, nullable=False, default=0)
    und = db.Column(db.Integer, nullable=False, default=0)

    # setting for foreignkey
    Clauses = db.relationship('Clauses', backref=db.backref('clausePoints', lazy=True))
    Note = db.relationship('Note', backref=db.backref('clausePoints', lazy=True))

    def __init__(self, clauseid, noteid, imp=0, und=0):
        self.clause_id = clauseid
        self.note_id = noteid
        self.imp = imp
        self.und = und


# Create table
def init_db_table():
    db.create_all()


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
        query.filter(getattr(table, attr) == value)
    result = query.all()
    return result


#delete all data where *args
#@Todo if note have to be deleted, consider that forienKey in clauses, clausePoints table
def delete_data_from_db(table, *args):
    """
    :param table: Data model object (Note, Clause, ClausePoints)
    :param args: condition where you use in 'where' statement
    :return: (dict) result
    """
    args = args[0]
    query = db.session.query(table)
    for attr, value in args.items():
        query.filter(getattr(table, attr) == value)
    items = query.all()
    result = []
    for item in items:
        db.session.delete(item)
        db.session.commit()
        result.append(item.note_id)
    return result


def delete_note_and_related_data_from_db(node_id):
    pass


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
        query.filter(getattr(table, attr))
    item = query.first()
    for attr, value in update_data.items():
        item[attr] = value
    db.session.commit()