PRAGMA foreign_keys = ON;

 -- Удаление старых таблиц (сначала зависимые таблицы)
DROP TABLE IF EXISTS messages_in_tickets;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS users_device;
DROP TABLE IF EXISTS users;

 -- Удаление старых таблиц (после независимые таблицы)
 DROP TABLE IF EXISTS user_roles;
 DROP TABLE IF EXISTS ticket_categories;
 DROP TABLE IF EXISTS ticket_status;

-- Роли пользователей(клиент, сотрудник)
CREATE TABLE user_roles (
    user_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Пользователи
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT NOT NULL,
    login TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    user_role INTEGER NOT NULL,

    FOREIGN KEY (user_role) REFERENCES user_roles(user_role_id)
);

CREATE TABLE users_device (
    device_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Категории заявок
CREATE TABLE ticket_categories (
    category_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Статусы заявок
CREATE TABLE ticket_status (
    ticket_status_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Таблица заявок
CREATE TABLE tickets (
    ticket_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ticket_category_id INTEGER NOT NULL,
    ticket_description TEXT NOT NULL,
    current_status TEXT NOT NULL,
    ticket_created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_updated_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    executor_id INTEGER,

    FOREIGN KEY (ticket_category_id) REFERENCES ticket_categories(category_id),
    FOREIGN KEY (current_status) REFERENCES ticket_status(name),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (executor_id) REFERENCES users(user_id)
);

-- Таблица сообщений внутри заявок(Диалог между сотрудником техподдержки и пользователем)
CREATE TABLE messages_in_tickets(
    message_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    message_text TEXT NOT NULL,
    written_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE, -- В случае удаления заявки, будут удалены все сообщения
    FOREIGN KEY (sender_id) REFERENCES users(user_id)
);

INSERT INTO user_roles(name)
VALUES ('Client'), ('Admin');

INSERT INTO ticket_categories(name)
VALUES ('Auth&Profile'), ('Techincal&Bugs'), ('Billing&Payments'), ('Features&Content'), ('General&Requests');

INSERT INTO ticket_status(name)
VALUES ('Sent / Awaiting response'), ('Response received'), ('Deleted');