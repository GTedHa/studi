from sqlalchemy import or_
from studi import app
from .models.extentions import db
from .models.notes import Notes
from .models.clauses import Clauses
from .models.clausePoints import ClausePoints


# Create table (defalut, production = False)
def create_db(Production=False):
    # Create testing DB (test_studi.db)
    if not Production:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'
    db.create_all()
    return db

def drop_db(Production=False):
    # Drop testing DB (test_studi.db)
    if not Production:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test_studi.db'
    db.drop_all()
    return db

# Insert ata to table you want to
def insert_data_to_db(table, model):
    # Id list to return by table
    id_list = {'Clauses': 'clause', 'Notes': 'note', 'ClausePoints' : 'clause'}
    db.session.add(model)
    db.session.commit()
    id = getattr(model, id_list[table] + '_id')
    db.session.close()
    return id


# Get all data from table
def get_all_data_from_db(table):
    """
    :param table: data model object
    :return: (dict) result
    """
    items = db.session.query(table)
    results = []
    if items:
        for item in items:
            result = dict()
            for key in item.column:
                result[key] = getattr(item, key)
            results.append(result)
    db.session.close()
    return results


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

    results = []
    if items:
        for item in items:
            result = dict()
            for key in item.column:
                result[key] = getattr(item, key)
            results.append(result)
    db.session.close()
    return results


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
    db.session.close()
    return items


# delete only one note
def delete_note_and_related_data_from_db(note_id):
    query = db.session.query(Notes)
    note = query.filter(getattr(Notes, 'note_id') == note_id).one()
    # all() return list []
    db.session.delete(note)
    db.session.commit()
    db.session.close()
    return note


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

    models = query.all()

    for model in models:
        for key, value in update_data.items():
            setattr(model, key, value)
    db.session.commit()

    results = []
    if models:
        for item in models:
            result = dict()
            for key in item.column:
                result[key] = getattr(item, key)
            results.append(result)
    db.session.close()
    return results
