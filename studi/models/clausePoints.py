from .extentions import db

class ClausePoints(db.Model):
    __tablename__ = 'clause_points'
    column = ['clause_id', 'note_id', 'imp', 'und']
    clause_id = db.Column(db.Integer, db.ForeignKey('clauses.clause_id'), primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.note_id'), nullable=False)
    imp = db.Column(db.Integer, nullable=False, default=0)
    und = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, clauseid=None, noteid=None, imp=0, und=0):
        self.clause_id = clauseid
        self.note_id = noteid
        self.imp = imp
        self.und = und
