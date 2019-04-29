from .extentions import db

class Notes(db.Model):
    __tablename__ = 'notes'
    column = ['note_id', 'note_name']
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_name = db.Column(db.Text, nullable=False)

    def __init__(self, notename):
        self.note_name = notename

    clauses = db.relationship("Clauses", cascade="all, delete")
    clausePoints = db.relationship('ClausePoints', cascade="all, delete")

