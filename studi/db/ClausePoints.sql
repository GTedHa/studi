CREATE TABLE ClausePoints (
    clause_id INTEGER PRIMARY KEY,
    note_id INTEGER NOT NULL,
    imp INTEGER NOT NULL DEFAULT 0,
    und INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(clause_id) REFERENCES Clauses(clause_id),
    FOREIGN KEY(note_id) REFERENCES Notes(note_id)
);