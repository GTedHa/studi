from .extentions import db


class Clauses(db.Model):
    __tablename__ = 'clauses'
    column = ['clause_id', 'note_id', 'title', 'contents']
    clause_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.note_id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    contents = db.Column(db.Text, nullable=False)

    clausePoints = db.relationship('ClausePoints', cascade="all, delete")

    def __init__(self, noteid=None, title=None, contents=None):
        self.note_id = noteid
        self.title = title
        self.contents = contents