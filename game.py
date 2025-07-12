import uuid
from turn import Turn
from player import Player


class Game:
    def __init__(self):
        self.id = uuid.uuid4()
        self.player1 = None
        self.player2 = None
        self.current_turn = Turn()
        self.winner = None
        self.game_over = False

    def set_player(self, player_name, player_id, deck):
        if player_id == 1:
            self.player1 = Player(player_name, player_id, deck)
        elif player_id == 2:
            self.player2 = Player(player_name, player_id, deck)

    def start_game(self):

        self.player1.shuffle()
        self.player2.shuffle()
        for _ in range(5):
            self.player1.deck_to_shield_zone()
            self.player2.deck_to_shield_zone()
            self.player1.deck_to_hand()
            self.player2.deck_to_hand()
        self.current_turn.decide_first_player(self.player1, self.player2)

    def to_dict(self):
        if len(self.player1.deck) == 0:
            self.winner = self.player2.name
            self.game_over = True
        if len(self.player2.deck) == 0:
            self.winner = self.player1.name
            self.game_over = True
        return {
            'player1': self.player1.to_dict(),
            'player2': self.player2.to_dict(),
            'current_turn': self.current_turn.to_dict(),
            'winner': self.winner
        }
