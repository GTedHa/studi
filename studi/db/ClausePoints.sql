CREATE TABLE ClausePoints (
    clause_id INTEGER PRIMARY KEY,
    imp INTEGER NOT NULL DEFAULT 0,
    und INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(clause_id) REFERENCES Clauses(clause_id)
);