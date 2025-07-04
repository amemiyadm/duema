import time

from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit, join_room
from functools import wraps

from game import *
from turn import *
from player import *
from card import *


def game_active_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if game_instance and game_instance.game_over:
            alert = 'ゲームは既に終了しています。'
            emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
            return
        return f(*args, **kwargs)
    return decorated_function


app = Flask(__name__)
app.debug = True
socketio = SocketIO(app, cors_allowed_origins="*")

game_instance = None
hoge_attack_target_index = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/join-game', methods=['POST'])
def entry_game():
    player_name = request.form['player-name']
    deck = int(request.form['deck'])
    global game_instance
    if not game_instance:
        player_id = 1
        game_instance = Game()
    elif not game_instance.player2:
        player_id = 2
    else:
        return jsonify({'alert': '満員のためゲームに参加できませんでした。'})
    game_instance.set_player(player_name, player_id, deck)
    return jsonify({'player_id': player_id})


@app.route('/game')
def game():
    return render_template('game.html', timestamp=int(time.time()))


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
        emit('alert', {**game_instance.to_dict(), 'alert': alert}, room=game_instance.id)


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
        emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
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
        emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
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
        emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
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
        emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
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
    emit('strong-alert-close', {**game_instance.to_dict()}, room=game_instance.id)


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
    emit('strong-alert-close', {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('count-ability-trigger')
@game_active_required
def count_ability(data):
    count = int(data['count'])
    turn = game_instance.current_turn
    turn.stock[0].activate(turn.inactive_player, turn.active_player,  count)
    turn.stock.pop(0)
    emit('strong-alert-close', {**game_instance.to_dict()}, room=game_instance.id)


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
    emit('strong-alert-close', {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('attack-player-prepare')
@game_active_required
def attack_player_prepare(data):
    card_uuid = data['card-uuid']
    turn = game_instance.current_turn
    can_attack_player, break_count, alert = turn.can_attack_player(card_uuid)
    if not can_attack_player:
        emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
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
            emit('end-game', {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('block-player-attack')
@game_active_required
def block_player_attack(data):
    blocker_index = data['select-cards']
    turn = game_instance.current_turn
    battle_zone_index = turn.pending_card
    if not blocker_index:
        _, break_count, _ = turn.can_attack_player(battle_zone_index)
        if len(turn.inactive_player.shield_zone) > 0:
            emit('strong-alert-close', {**game_instance.to_dict()}, room=game_instance.id)
            emit('attack-player-prepare', {
                **game_instance.to_dict(),
                'break_count': break_count
            }, room=game_instance.id, include_self=False)
        else:
            turn.direct_attack(battle_zone_index)
            game_instance.winner = turn.active_player.name
            game_instance.game_over = True
            emit('strong-alert-close', {**game_instance.to_dict()}, room=game_instance.id)
            emit('end-game', {**game_instance.to_dict()}, room=game_instance.id)
        return
    turn.block(battle_zone_index, blocker_index[0])
    emit('rendering', {**game_instance.to_dict()}, room=game_instance.id)
    emit('strong-alert-close', {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('attack-player-execute')
@game_active_required
def attack_player_execute(data):
    break_shield = data['select-cards']
    turn = game_instance.current_turn
    battle_zone_index = turn.pending_card
    can_break_shield, alert = turn.can_break_shield(battle_zone_index, break_shield)
    if not can_break_shield:
        emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
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
        can_battle, alert = turn.can_battle(battle_zone_index, hoge_attack_target_index)
        if not can_battle:
            emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
            return
        turn.battle(battle_zone_index, hoge_attack_target_index)
        emit('strong-alert-close', {**game_instance.to_dict()}, room=game_instance.id)
        hoge_attack_target_index = None
    else:
        turn.block(battle_zone_index, blocker_index[0])
        emit('strong-alert-close', {**game_instance.to_dict()}, room=game_instance.id)
    emit('rendering', {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('attack-creature-prepare')
@game_active_required
def attack_creature_prepare(data):
    card_uuid = data['battle-zone-index']
    turn = game_instance.current_turn
    can_attack_creature, alert = turn.can_attack_creature(card_uuid)
    if not can_attack_creature:
        emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
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
        emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
        return
    can_battle, alert = turn.can_battle(battle_zone_index, data['select-cards'][0])
    if not can_battle:
        emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
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
        can_battle, alert = turn.can_battle(battle_zone_index, attack_target_index)
        if not can_battle:
            emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
            return
        turn.battle(battle_zone_index, attack_target_index)
    emit('rendering', game_instance.to_dict(), room=game_instance.id)


@socketio.on('play-shield-triggers-execute')
@game_active_required
def play_shield_trigger_execute(data):
    hand_indexs = data['select-cards']
    if not hand_indexs:
        emit('strong-alert-close', {**game_instance.to_dict()}, room=game_instance.id)
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
        emit('strong-alert-close', {**game_instance.to_dict()}, room=game_instance.id)


@socketio.on('end-turn')
@game_active_required
def end_turn():
    turn = game_instance.current_turn
    if request.sid != turn.active_player.id:
        alert = 'ターンプレイヤーのみターン終了できます。'
        emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
        return
    if next((creature for creature in turn.active_player.battle_zone if 'mustAttack' in creature._static_abilities and not creature.is_tap and not creature.is_summoning_sickness), None):
        alert = '攻撃しなければならないクリーチャーがいます。'
        emit('alert', {**game_instance.to_dict(), 'alert': alert}, include_self=True)
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
