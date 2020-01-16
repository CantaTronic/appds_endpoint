CREATE TABLE user (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, pass_sha1 TEXT NOT NULL);
INSERT INTO user VALUES (1, 'test_user', 'c1d65c4ba0d33773aa58ac68196867d5481161b6');
CREATE TABLE request (id INTEGER PRIMARY KEY, uuid TEXT NOT NULL UNIQUE, user_id INTEGER NOT NULL, format TEXT NOT NULL, status TEXT NOT NULL);
CREATE INDEX request_user_idx ON request(user_id);
INSERT INTO request VALUES (1, '60a1fa84-3aa7-46a8-a17e-5a99336b8d69', 1, 'ASCII', 'completed');
