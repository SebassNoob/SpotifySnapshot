DROP TABLE IF EXISTS endUser;

  
CREATE TABLE endUser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    url TEXT NOT NULL
);