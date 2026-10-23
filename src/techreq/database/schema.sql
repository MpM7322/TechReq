-- Для работы через sqlite3
PRAGMA foreign_keys = ON;

-- Удаляем таблицы, если они уже существуют(сначала зависимые, потом независимые)
DROP TABLE IF EXISTS executor_categories;
DROP TABLE IF EXISTS ticket_resolutions;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS ticket_status;
DROP TABLE IF EXISTS ticket_categories;
DROP TABLE IF EXISTS user_roles;

-- Таблица ролей пользователй
CREATE TABLE user_roles (
    user_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Таблица категорий заявок
CREATE TABLE ticket_categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Таблица статусов заявок
CREATE TABLE ticket_status (
    ticket_status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Таблица пользователей
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

-- Таблица заявок
CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_category_id INTEGER NOT NULL,
    ticket_description TEXT NOT NULL,
    current_status_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    executor_id INTEGER,

    FOREIGN KEY (ticket_category_id) REFERENCES ticket_categories(category_id),
    FOREIGN KEY (current_status_id) REFERENCES ticket_status(ticket_status_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (executor_id) REFERENCES users(user_id)
);

-- Таблица с решениями заявок
CREATE TABLE ticket_resolutions (
    resolution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL UNIQUE,
    solution_text TEXT NOT NULL,

    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE -- Если удаляется в главной таблице, то удалится и в зависимой
);

-- Таблица с возможностями сотрудников
CREATE TABLE executor_categories (
    executor_category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    executor_id INTEGER NOT NULL,
    ticket_category_id INTEGER NOT NULL,

    FOREIGN KEY (executor_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (ticket_category_id) REFERENCES ticket_categories(category_id) ON DELETE CASCADE
);

INSERT INTO user_roles (name)
VALUES ('Клиент'), ('Администратор');

INSERT INTO ticket_categories (name)
VALUES ('Авторизация и профиль'), ('Технические проблемы и баги'), ('Оплата и счета'), ('Функционал и контент'), ('Общие вопросы');

INSERT INTO ticket_status (name)
VALUES ('Отправлено / Ожидает ответа'), ('Получен ответ'), ('Удалено');


INSERT INTO users (name, surname, patronymic, login, password, user_role)
VALUES
    ('Иван', 'Иванов', 'Иванович', 'ivan_client', 'hash_pass_1', 1),
    ('Петр', 'Петров', 'Петрович', 'petr_client', 'hash_pass_2', 1),
    ('Анна', 'Сидорова', 'Алексеевна', 'anna_client', 'hash_pass_3', 1),
    ('Алексей', 'Админов', 'Сергеевич', 'alex_admin', 'admin_pass_1', 2),
    ('Дмитрий', 'Мастеров', 'Игоревич', 'dima_admin', 'admin_pass_2', 2),
    ('Елена', 'Техподдержкова', 'Владимировна', 'elena_admin', 'admin_pass_3', 2);

INSERT INTO executor_categories (executor_id, ticket_category_id)
VALUES (4, 1), (4, 2), (5, 3), (6, 2);

INSERT INTO tickets (ticket_category_id, ticket_description, current_status_id, user_id, executor_id)
VALUES
    (1, 'Не могу зайти на сайт, пишет неверный пароль', 2, 1, 4),
    (3, 'Дважды списались деньги за подписку', 1, 2, 5),
    (2, 'Мобильное приложение вылетает при запуске', 2, 3, 6);


INSERT INTO ticket_resolutions (ticket_id, solution_text)
VALUES
    (1, 'Сбросили пароль в панели управления. Новый отправлен на почту.'),
    (3, 'Проблема обнаружена в логах приложения. Обновите приложение.');