PRAGMA foreign_keyes = ON;

CREATE TABLE user_roles (
    user_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE
);