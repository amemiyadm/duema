import random
from itertools import groupby
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from flask_socketio import SocketIO, emit, join_room
from functools import wraps
from user import *
from game import *
from card_list import card_list
from card import CardFactory


app = Flask(__name__)
app.secret_key = 'your-very-secret-key'
socketio = SocketIO(app, cors_allowed_origins='*')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    return User.get(username)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register-user', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']

    if len(username) == 0:
        return jsonify({'error': 'ユーザー名を入力してください。'})
    if len(password) == 0:
        return jsonify({'error': 'パスワードを入力してください。'})
    if len(username) > 8:
        return jsonify({'error': 'ユーザー名は8文字までです。'})
    if len(password) < 0:
        return jsonify({'error': 'パスワードを入力してください。'})
    if len(password) < 4:
        return jsonify({'error': 'パスワードが短すぎます。'})

    new_user, error = User.create_user(username, password)
    if new_user:
        login_user(new_user)
        return jsonify({'redirect_url': url_for('menu')})
    else:
        jsonify({'error': error})


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.find_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({'redirect_url': url_for('menu')})
    else:
        return jsonify({'error': 'ログインに失敗しました。'})


@app.route('/menu')
def menu():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        deck = cursor.execute(
            '''
            SELECT decks.key_card_id, decks.deckname
            FROM decks
            INNER JOIN users
                ON decks.id = users.deck_to_used
            WHERE users.id = ?
            ''',
            (current_user.id, )
        ).fetchone()

    username = current_user.username
    compose_cards = random.sample(card_list, 3)
    key_card = next(card for card in card_list if card['id'] == deck[0])
    deckname = deck[1]
    return render_template('menu.html', username=username, compose_cards=compose_cards, key_card=key_card, deckname=deckname)


@app.route('/playmat-config')
def playmat_config():
    return render_template('playmat_config.html')


@app.route('/management-deck')
def management_deck():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    decks = cursor.execute(
        '''
        SELECT * FROM decks
        WHERE user_id = ?
        ''',
        (current_user.id, )
    ).fetchall()
    conn.close()
    return render_template('management_deck.html', decks=decks)


@app.route('/delete-deck/<int:id>', methods=['POST'])
def delete_deck(id):
    if current_user.deck_to_used != id:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                DELETE
                FROM decks
                WHERE id = ?
                ''',
                (id, )
            )
            cursor.execute(
                '''
                DELETE
                FROM deck_cards
                WHERE deck_id = ?
                ''',
                (id, )
            )
            conn.commit()
            conn.close()
            return redirect(url_for('management_deck'))
        except Exception as e:
            print(e)
    return redirect(url_for('management_deck'))


@app.route('/confirm-deck', methods=['POST'])
def confirm_deck():
    deck_id = request.form['deck-id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    cards = cursor.execute(
        '''
        SELECT * FROM decks
        LEFT JOIN deck_cards
            ON decks.id = deck_cards.deck_id
        WHERE decks.id = ?
        ORDER BY decks.id
        ''',
        (deck_id, )
    ).fetchall()
    conn.close()

    deck = {
        'deckname': cards[0]['deckname'],
        'cards': [card['card_id'] for card in cards]
    }
    return jsonify({'deck': deck})


@app.route('/create-deck')
def create_deck():
    all_cards = [card['id'] for card in card_list]
    return render_template('create_deck.html', all_cards=all_cards)


@app.route('/save-deck', methods=['POST'])
def save_deck():
    cards = request.form['cards'].split(',')
    deckname = request.form['deckname']
    deck_id = request.form.get('deck-id', None)
    print(deck_id)
    if deck_id and current_user.deck_to_used != deck_id:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                DELETE
                FROM decks
                WHERE id = ?
                ''',
                (deck_id, )
            )
            cursor.execute(
                '''
                DELETE
                FROM deck_cards
                WHERE deck_id = ?
                ''',
                (deck_id, )
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO decks (user_id, deckname, key_card_id) VALUES (?, ?, ?)',
            (current_user.id, deckname, cards[0])
        )
        new_deck_id = cursor.lastrowid
        new_deck = [(new_deck_id, card) for card in cards]
        sql = 'INSERT INTO deck_cards (deck_id, card_id) VALUES (?, ?)'
        cursor.executemany(sql, new_deck)
        conn.commit()
        conn.close()
        return jsonify({'redirect_url': url_for('management_deck')})
    except Exception as e:
        print(e)
        return jsonify({'error': '保存に失敗しました。'})


@app.route('/deck-change/<int:id>', methods=['POST'])
def deck_change(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE users
            SET deck_to_used = ?
            WHERE id = ?
            ''',
            (id, current_user.id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('menu'))
    except Exception as e:
        print(e)


@app.route('/deck-update/<int:id>', methods=['POST'])
def deck_update(id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cards = cursor.execute(
            '''
            SELECT deck_cards.card_id, decks.deckname, decks.id
            FROM decks
            LEFT JOIN deck_cards
                ON decks.id = deck_cards.deck_id
            WHERE decks.id = ?
            ORDER BY decks.id
            ''',
            (id, )
        ).fetchall()
    deck_id = cards[0]['id']
    deckname = cards[0]['deckname']
    deck_cards = [card['card_id'] for card in cards]
    all_cards = [card['id'] for card in card_list]
    return render_template('update_deck.html', deck_cards=deck_cards, all_cards=all_cards, deckname=deckname, deck_id=deck_id)


def game_active_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if game_instance and game_instance.game_over:
            alert = 'ゲームは既に終了しています。'
            emit('alert', {**game_instance.to_dict(),
                 'alert': alert}, include_self=True)
            return
        return f(*args, **kwargs)
    return decorated_function


game_instance = None


@app.route('/join-game', methods=['POST'])
def entry_game():
    global game_instance
    if not game_instance:
        player_id = 1
        game_instance = Game()
    elif not game_instance.player2:
        player_id = 2
    else:
        return jsonify({'alert': '満員のためゲームに参加できませんでした。'})

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.row_factory = sqlite3.Row
    cards = cursor.execute(
        '''
        SELECT *
        FROM decks
        LEFT JOIN deck_cards
            ON decks.id = deck_cards.deck_id
        WHERE decks.id = ?
        ORDER BY decks.id
        ''',
        (current_user.deck_to_used, )
    ).fetchall()
    conn.close()

    deck_ids = [card['card_id'] for card in cards]
    deck = [CardFactory.create_card(next(
        card for card in card_list if card['id'] == card_id)) for card_id in deck_ids]
    game_instance.set_player(current_user.username, player_id, deck)
    return jsonify({'player_id': player_id})


@app.route('/game')
def game():
    return render_template('game.html')


@socketio.on('connect')
def connect(data):
    game_id = game_instance.id
    join_room(game_id)
    if data['id'] == '1':
        game_instance.player1.set_id(request.sid)
    elif data['id'] == '2':
        game_instance.player2.set_id(request.sid)
    if game_instance.player2:
        game_instance.start_game()
        emit('game-start', game_instance.to_dict(), room=game_instance.id)


@socketio.on('disconnect')
def disconnect():
    global game_instance
    if game_instance.game_over or not game_instance.player2:
        game_instance = None
    else:
        game_instance.game_over = True
        alert = '退出したプレイヤーがいるためゲームを中断しました。'
        emit('alert', {**game_instance.to_dict(),
             'alert': alert}, room=game_instance.id)


@socketio.on('rendering')
def rendering():
    emit('rendering', game_instance.to_dict(), room=game_instance.id)


@socketio.on('charge-mana')
@game_active_required
def charge_mana(data):
    card_uuid = data['card-uuid']
    turn = game_instance.current_turn
    can_charge_mana, alert = turn.can_charge_mana()
    if not can_charge_mana:
        emit('alert', {**game_instance.to_dict(),
             'alert': alert}, include_self=True)
        return
    turn.charge_mana(card_uuid)
    emit('rendering', game_instance.to_dict(), room=game_instance.id)


@socketio.on('play-card-prepare')
@game_active_required
def play_card_prepare(data):
    card_uuid = data['card-uuid']
    turn = game_instance.current_turn
    can_play_card, alert, cost = turn.can_play_card(card_uuid)
    if not can_play_card:
        emit('alert', {**game_instance.to_dict(),
             'alert': alert}, include_self=True)
        return
    turn.set_pending_card(card_uuid)
    emit('play-card-prepare', {
        **game_instance.to_dict(),
        'cost': cost
    }, include_self=True)


@socketio.on('play-card-execute')
@game_active_required
def play_card_execute(data):
    mana_used = data['select-cards']
    turn = game_instance.current_turn
    card_uuid = turn.pending_card
    can_use_mana, alert = turn.can_use_mana(card_uuid, mana_used)
    if not can_use_mana:
        emit('alert', {**game_instance.to_dict(),
             'alert': alert}, include_self=True)
        return
    turn.play_card(card_uuid, mana_used)
    emit('rendering', game_instance.to_dict(), room=game_instance.id)
    if turn.stock:
        execute_stock()
    else:
        emit('rendering', game_instance.to_dict(), room=game_instance.id)


@socketio.on('execute-random')
@game_active_required
def execute_random(data):
    turn = game_instance.current_turn
    card_uuid = turn.pending_card
    can_use_random, alert, mana_used = turn.can_use_random(card_uuid)
    if not can_use_random:
        emit('alert', {**game_instance.to_dict(),
             'alert': alert}, include_self=True)
        return
    turn.random_tap_play_card(card_uuid, mana_used)
    emit('rendering', game_instance.to_dict(), room=game_instance.id)
    if turn.stock:
        execute_stock()
    else:
        emit('rendering', game_instance.to_dict(), room=game_instance.id)


def execute_stock():
    turn = game_instance.current_turn
    #     if turn.stock[0].ability_conditions == 'optional':
    #         emit('optional-ability', {
    #             **game_instance.to_dict(),
    #             'card_name': turn.stock[0].card_name
    #         }, include_self=True)
    if turn.stock[0].ability_conditions == 'count':
        emit('count-ability', {
            **game_instance.to_dict(),
            'select_count': turn.stock[0].select_count
        }, include_self=True)
    elif turn.stock[0].ability_conditions == 'select':
        if getattr(turn.stock[0], 'passive', None):
            emit('select-ability', {
                **game_instance.to_dict(),
                'select_count': turn.stock[0].select_count,
                'compulsion': turn.stock[0].compulsion,
                'zone_cards': [card.to_dict() for card in turn.stock[0].zone_cards(turn.active_player, turn.inactive_player)]
            }, room=game_instance.id, include_self=False)

            emit('strong-alert', {
                **game_instance.to_dict(),
                'alert': '効果処理中です。'
            }, include_self=True)
        else:
            emit('select-ability', {
                **game_instance.to_dict(),
                'select_count': turn.stock[0].select_count,
                'compulsion': turn.stock[0].compulsion,
                'zone_cards': [card.to_dict() for card in turn.stock[0].zone_cards(turn.active_player, turn.inactive_player)]
            }, include_self=True)


# @socketio.on('optional-ability')
# @game_active_required
# def play_card_execute(data):
#     option = data['option']
#     turn = game_instance.current_turn
#     if option:
#         turn.optional_ability()
#     emit('rendering', {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('count-ability')
@game_active_required
def count_ability(data):
    count = int(data['count'])
    turn = game_instance.current_turn
    turn.stock[0].activate(turn.active_player, turn.inactive_player, count)
    turn.stock.pop(0)
    emit('rendering', {**game_instance.to_dict()}, room=game_instance.id)
    emit('strong-alert-close',
         {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('select-ability')
@game_active_required
def select_ability(data):
    selects = data['select-cards']
    turn = game_instance.current_turn
    if turn.stock[0].compulsion and len(selects) != turn.stock[0].select_count:
        emit('select-ability', {
            **game_instance.to_dict(),
            'select_count': turn.stock[0].select_count,
            'compulsion': turn.stock[0].compulsion,
            'zone_cards': [card.to_dict() for card in turn.stock[0].zone_cards(turn.active_player, turn.inactive_player)]
        }, include_self=True)
    turn.stock[0].activate(turn.active_player, turn.inactive_player, selects)
    turn.stock.pop(0)
    emit('rendering', {**game_instance.to_dict()}, room=game_instance.id)
    emit('strong-alert-close',
         {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('count-ability-trigger')
@game_active_required
def count_ability(data):
    count = int(data['count'])
    turn = game_instance.current_turn
    turn.stock[0].activate(turn.inactive_player, turn.active_player,  count)
    turn.stock.pop(0)
    emit('strong-alert-close',
         {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('select-ability-trigger')
@game_active_required
def select_ability(data):
    selects = data['select-cards']
    turn = game_instance.current_turn
    if turn.stock[0].compulsion and len(selects) != turn.stock[0].select_count:
        emit('select-ability', {
            **game_instance.to_dict(),
            'select_count': turn.stock[0].select_count,
            'compulsion': turn.stock[0].compulsion,
            'zone_cards': [card.to_dict() for card in turn.stock[0].zone_cards(turn.inactive_player, turn.active_player)]
        }, include_self=True)
    turn.stock[0].activate(turn.inactive_player, turn.active_player, selects)
    turn.stock.pop(0)
    emit('strong-alert-close',
         {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('attack-player-prepare')
@game_active_required
def attack_player_prepare(data):
    card_uuid = data['card-uuid']
    turn = game_instance.current_turn
    can_attack_player, break_count, alert = turn.can_attack_player(card_uuid)
    if not can_attack_player:
        emit('alert', {**game_instance.to_dict(),
             'alert': alert}, include_self=True)
        return
    blockers = turn.get_blockers(card_uuid)
    if blockers:
        turn.set_pending_card(card_uuid)
        emit('block', {
            **game_instance.to_dict(),
            'blockers': blockers,
            'break_count': break_count,
            'execute_target': 'block-player-attack'
        }, room=game_instance.id, include_self=False)

        emit('strong-alert', {
            **game_instance.to_dict(),
            'alert': ' ブロッカー処理中です。'
        }, include_self=True)
    else:
        if len(turn.inactive_player.shield_zone) > 0:
            turn.set_pending_card(card_uuid)
            emit('attack-player-prepare', {
                **game_instance.to_dict(),
                'break_count': break_count,
            }, include_self=True)
        else:
            turn.direct_attack(card_uuid)
            game_instance.winner = turn.active_player.name
            game_instance.game_over = True
            emit('end-game', {**game_instance.to_dict()},
                 room=game_instance.id)


@socketio.on('block-player-attack')
@game_active_required
def block_player_attack(data):
    blocker_index = data['select-cards']
    turn = game_instance.current_turn
    battle_zone_index = turn.pending_card
    if not blocker_index:
        _, break_count, _ = turn.can_attack_player(battle_zone_index)
        if len(turn.inactive_player.shield_zone) > 0:
            emit('strong-alert-close',
                 {**game_instance.to_dict()}, room=game_instance.id)
            emit('attack-player-prepare', {
                **game_instance.to_dict(),
                'break_count': break_count
            }, room=game_instance.id, include_self=False)
        else:
            turn.direct_attack(battle_zone_index)
            game_instance.winner = turn.active_player.name
            game_instance.game_over = True
            emit('strong-alert-close',
                 {**game_instance.to_dict()}, room=game_instance.id)
            emit('end-game', {**game_instance.to_dict()},
                 room=game_instance.id)
        return
    turn.block(battle_zone_index, blocker_index[0])
    emit('rendering', {**game_instance.to_dict()}, room=game_instance.id)
    emit('strong-alert-close',
         {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('attack-player-execute')
@game_active_required
def attack_player_execute(data):
    break_shield = data['select-cards']
    turn = game_instance.current_turn
    battle_zone_index = turn.pending_card
    can_break_shield, alert = turn.can_break_shield(
        battle_zone_index, break_shield)
    if not can_break_shield:
        emit('alert', {**game_instance.to_dict(),
             'alert': alert}, include_self=True)
        return
    shield_triggers = turn.break_shield(battle_zone_index, break_shield)
    if shield_triggers:
        emit('play-shield-triggers-prepare', {
            **game_instance.to_dict(),
            'shield_triggers': shield_triggers
        }, room=game_instance.id, include_self=False)

        emit('strong-alert', {
            **game_instance.to_dict(),
            'alert': 'シールドトリガー処理中です。'
        }, include_self=True)
        return
    emit('rendering', game_instance.to_dict(), room=game_instance.id)


@socketio.on('block-creature-attack')
@game_active_required
def block_creature_attack(data):
    blocker_index = data['select-cards']
    turn = game_instance.current_turn
    battle_zone_index = turn.pending_card
    if not blocker_index:
        global hoge_attack_target_index
        can_battle, alert = turn.can_battle(
            battle_zone_index, hoge_attack_target_index)
        if not can_battle:
            emit('alert', {**game_instance.to_dict(),
                 'alert': alert}, include_self=True)
            return
        turn.battle(battle_zone_index, hoge_attack_target_index)
        emit('strong-alert-close',
             {**game_instance.to_dict()}, room=game_instance.id)
        hoge_attack_target_index = None
    else:
        turn.block(battle_zone_index, blocker_index[0])
        emit('strong-alert-close',
             {**game_instance.to_dict()}, room=game_instance.id)
    emit('rendering', {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('attack-creature-prepare')
@game_active_required
def attack_creature_prepare(data):
    card_uuid = data['battle-zone-index']
    turn = game_instance.current_turn
    can_attack_creature, alert = turn.can_attack_creature(card_uuid)
    if not can_attack_creature:
        emit('alert', {**game_instance.to_dict(),
             'alert': alert}, include_self=True)
        return
    turn.set_pending_card(card_uuid)
    emit('attack-creature-prepare', {
        **game_instance.to_dict()
    }, include_self=True)


@socketio.on('attack-creature-execute')
@game_active_required
def attack_creature_execute(data):
    turn = game_instance.current_turn
    battle_zone_index = turn.pending_card
    if not data['select-cards']:
        alert = 'アタックする対象を選んでください。'
        emit('alert', {**game_instance.to_dict(),
             'alert': alert}, include_self=True)
        return
    can_battle, alert = turn.can_battle(
        battle_zone_index, data['select-cards'][0])
    if not can_battle:
        emit('alert', {**game_instance.to_dict(),
             'alert': alert}, include_self=True)
        return
    blockers = turn.get_blockers(battle_zone_index)
    if blockers:
        global hoge_attack_target_index
        hoge_attack_target_index = data['select-cards'][0]
        emit('block', {
            **game_instance.to_dict(),
            'battle_zone_index': battle_zone_index,
            'blockers': blockers,
            'execute_target': 'block-creature-attack'
        }, room=game_instance.id, include_self=False)

        emit('strong-alert', {
            **game_instance.to_dict(),
            'alert': ' ブロッカー処理中です。'
        }, include_self=True)
    else:
        attack_target_index = data['select-cards'][0]
        can_battle, alert = turn.can_battle(
            battle_zone_index, attack_target_index)
        if not can_battle:
            emit('alert', {**game_instance.to_dict(),
                 'alert': alert}, include_self=True)
            return
        turn.battle(battle_zone_index, attack_target_index)
    emit('rendering', game_instance.to_dict(), room=game_instance.id)


@socketio.on('play-shield-triggers-execute')
@game_active_required
def play_shield_trigger_execute(data):
    hand_indexs = data['select-cards']
    if not hand_indexs:
        emit('strong-alert-close',
             {**game_instance.to_dict()}, room=game_instance.id)
        return
    turn = game_instance.current_turn
    for hand_index in hand_indexs:
        turn.play_shield_trigger(hand_index)
        emit('rendering', game_instance.to_dict(), room=game_instance.id)
    if turn.stock:
        #     if turn.stock[0].ability_conditions == 'optional':
        #         emit('optional-ability', {
        #             **game_instance.to_dict(),
        #             'card_name': turn.stock[0].card_name
        #         }, include_self=True)
        if turn.stock[0].ability_conditions == 'count':
            emit('count-ability-trigger', {
                **game_instance.to_dict(),
                'select_count': turn.stock[0].select_count
            }, include_self=True)
        elif turn.stock[0].ability_conditions == 'select':
            if getattr(turn.stock[0], 'passive', None):
                emit('select-ability-trigger', {
                    **game_instance.to_dict(),
                    'select_count': turn.stock[0].select_count,
                    'compulsion': turn.stock[0].compulsion,
                    'zone_cards': [card.to_dict() for card in turn.stock[0].zone_cards(turn.inactive_player, turn.active_player)]
                }, room=game_instance.id, include_self=False)

                emit('strong-alert', {
                    **game_instance.to_dict(),
                    'alert': '効果処理中です。'
                }, include_self=True)
            else:
                emit('select-ability-trigger', {
                    **game_instance.to_dict(),
                    'select_count': turn.stock[0].select_count,
                    'compulsion': turn.stock[0].compulsion,
                    'zone_cards': [card.to_dict() for card in turn.stock[0].zone_cards(turn.inactive_player, turn.active_player)]
                }, include_self=True)
    else:
        emit('rendering', game_instance.to_dict(), room=game_instance.id)
        emit('strong-alert-close',
             {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('end-turn')
@game_active_required
def end_turn():
    turn = game_instance.current_turn
    if request.sid != turn.active_player.id:
        alert = 'ターンプレイヤーのみターン終了できます。'
        emit('alert', {**game_instance.to_dict(),
             'alert': alert}, include_self=True)
        return
    if next((creature for creature in turn.active_player.battle_zone if 'mustAttack' in creature._static_abilities and not creature.is_tap and not creature.is_summoning_sickness), None):
        alert = '攻撃しなければならないクリーチャーがいます。'
        emit('alert', {**game_instance.to_dict(),
             'alert': alert}, include_self=True)
        return
    for creature in turn.active_player.battle_zone:
        if 'magumageizaa' in creature._static_abilities:
            creature._static_abilities.remove('magumageizaa')
    turn.end()
    turn.start()
    emit('rendering', game_instance.to_dict(), room=game_instance.id)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, port=5001)
    socketio.run(app, debug=True, port=5001, host='0.0.0.0')
