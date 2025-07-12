import sqlite3
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


def get_db_connection():
    conn = sqlite3.connect('sqlite/database.db')
    conn.row_factory = sqlite3.Row
    return conn


class User(UserMixin):
    def __init__(self, id, username, password_hash, deck_to_used):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.deck_to_used = deck_to_used

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        user_data = cursor.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        if user_data:
            return User(user_data['id'], user_data['username'], user_data['password'], user_data['deck_to_used'])
        return None

    @staticmethod
    def find_by_username(username):
        conn = get_db_connection()
        cursor = conn.cursor()
        user_data = cursor.execute(
            'SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user_data:
            return User(user_data['id'], user_data['username'], user_data['password'], user_data['deck_to_used'])
        return None

    @staticmethod
    def create_user(username, password):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                hashed_password = generate_password_hash(password)
                cursor.execute(
                    'INSERT INTO users (username, password) VALUES (?, ?)',
                    (username, hashed_password)
                )
                new_user_id = cursor.lastrowid

                cursor.execute(
                    'INSERT INTO decks (user_id, deckname, key_card_id) VALUES (?, ?, ?)',
                    (new_user_id, '青黒緑スナイパー', 'dm01-s03')
                )
                new_deck_id = cursor.lastrowid

                cursor.execute(
                    'UPDATE users SET deck_to_used = ? WHERE id = ?',
                    (new_deck_id, new_user_id)
                )

                new_deck = (
                    [(new_deck_id, 'dm01-s03')] * 4 +
                    [(new_deck_id, 'dm01-005')] * 4 +
                    [(new_deck_id, 'dm01-006')] * 4 +
                    [(new_deck_id, 'dm01-010')] * 2 +
                    [(new_deck_id, 'dm01-018')] * 2 +
                    [(new_deck_id, 'dm01-020')] * 4 +
                    [(new_deck_id, 'dm01-035')] * 2 +
                    [(new_deck_id, 'dm01-039')] * 2 +
                    [(new_deck_id, 'dm01-056')] * 4 +
                    [(new_deck_id, 'dm01-069')] * 4 +
                    [(new_deck_id, 'dm01-080')] * 4 +
                    [(new_deck_id, 'dm01-106')] * 4
                )
                sql = 'INSERT INTO deck_cards (deck_id, card_id) VALUES (?, ?)'
                cursor.executemany(sql, new_deck)

                cursor.execute(
                    'INSERT INTO decks (user_id, deckname, key_card_id) VALUES (?, ?, ?)',
                    (new_user_id, '赤青速攻', 'dm01-100')
                )
                new_deck_id = cursor.lastrowid

                new_deck = (
                    [(new_deck_id, 'dm01-s07')] * 2 +
                    [(new_deck_id, 'dm01-020')] * 4 +
                    [(new_deck_id, 'dm01-021')] * 4 +
                    [(new_deck_id, 'dm01-033')] * 4 +
                    [(new_deck_id, 'dm01-050')] * 2 +
                    [(new_deck_id, 'dm01-052')] * 4 +
                    [(new_deck_id, 'dm01-080')] * 4 +
                    [(new_deck_id, 'dm01-086')] * 4 +
                    [(new_deck_id, 'dm01-097')] * 4 +
                    [(new_deck_id, 'dm01-098')] * 4 +
                    [(new_deck_id, 'dm01-100')] * 4
                )
                sql = 'INSERT INTO deck_cards (deck_id, card_id) VALUES (?, ?)'
                cursor.executemany(sql, new_deck)

                cursor.execute(
                    'INSERT INTO decks (user_id, deckname, key_card_id) VALUES (?, ?, ?)',
                    (new_user_id, '白青黒コントロル', 'dm01-001')
                )
                new_deck_id = cursor.lastrowid

                new_deck = (
                    [(new_deck_id, 'dm01-s04')] * 4 +
                    [(new_deck_id, 'dm01-001')] * 4 +
                    [(new_deck_id, 'dm01-006')] * 2 +
                    [(new_deck_id, 'dm01-011')] * 2 +
                    [(new_deck_id, 'dm01-013')] * 2 +
                    [(new_deck_id, 'dm01-015')] * 4 +
                    [(new_deck_id, 'dm01-027')] * 4 +
                    [(new_deck_id, 'dm01-052')] * 4 +
                    [(new_deck_id, 'dm01-071')] * 2 +
                    [(new_deck_id, 'dm01-074')] * 4 +
                    [(new_deck_id, 'dm01-093')] * 4 +
                    [(new_deck_id, 'dm01-094')] * 4
                )
                sql = 'INSERT INTO deck_cards (deck_id, card_id) VALUES (?, ?)'
                cursor.executemany(sql, new_deck)

                cursor.execute(
                    'INSERT INTO decks (user_id, deckname, key_card_id) VALUES (?, ?, ?)',
                    (new_user_id, '青赤緑ビート', 'dm01-007')
                )
                new_deck_id = cursor.lastrowid

                new_deck = (
                    [(new_deck_id, 'dm01-s07')] * 4 +
                    [(new_deck_id, 'dm01-003')] * 4 +
                    [(new_deck_id, 'dm01-007')] * 4 +
                    [(new_deck_id, 'dm01-010')] * 4 +
                    [(new_deck_id, 'dm01-039')] * 4 +
                    [(new_deck_id, 'dm01-052')] * 4 +
                    [(new_deck_id, 'dm01-069')] * 4 +
                    [(new_deck_id, 'dm01-086')] * 4 +
                    [(new_deck_id, 'dm01-106')] * 4 +
                    [(new_deck_id, 'dm01-109')] * 4
                )
                sql = 'INSERT INTO deck_cards (deck_id, card_id) VALUES (?, ?)'
                cursor.executemany(sql, new_deck)

                conn.commit()

                return User.get(new_user_id), None
            except sqlite3.IntegrityError as e:
                conn.rollback()
                if 'UNIQUE constraint failed: users.username' in str(e):
                    return None, 'そのユーザー名は既に存在します。'
                else:
                    return None, f'{e}が発生しました。'
