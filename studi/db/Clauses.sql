CREATE TABLE Clauses (
    clause_id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    contents TEXT NOT NULL,
    FOREIGN KEY(note_id) REFERENCES Notes(note_id)
);