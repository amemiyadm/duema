DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS decks;
DROP TABLE IF EXISTS deck_cards;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    deck_to_used INTEGER
);

CREATE TABLE decks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    deckname TEXT NOT NULL,
    key_card_id INTEGER NOT NULL
);

CREATE TABLE deck_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deck_id INTEGER NOT NULL,
    card_id  INTEGER NOT NULL
);
