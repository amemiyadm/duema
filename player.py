import random


class Player():
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.deck = []
        self.shield_zone = []
        self.hand = []
        self.mana_zone = []
        self.graveyard = []
        self.battle_zone = []
        self.available_mana = 10

    def deck_to_hand(self):
        if len(self.deck) > 0:
            card = self.deck.pop(0)
            self.hand.append(card)

    def deck_to_shield_zone(self):
        if len(self.deck) > 0:
            card = self.deck.pop(0)
            self.shield_zone.append(card)

    def deck_to_mana_zone(self, deck_index):
        if len(self.deck) > 0:
            card = self.deck.pop(deck_index)
            self.mana_zone.append(card)

    def deck_to_graveyard(self):
        if len(self.deck) > 0:
            card = self.deck.pop(0)
            self.graveyard.append(card)

    def shield_zone_to_hand(self, index):
        card = self.shield_zone.pop(index)
        self.hand.append(card)
        return len(self.hand) - 1

    def shield_zone_to_graveyard(self, index):
        card = self.shield_zone.pop(index)
        self.graveyard.append(card)

    def hand_to_mana_zone(self, index):
        card = self.hand.pop(index)
        self.mana_zone.append(card)
        self.available_mana += 1

    def hand_to_battle_zone(self, hand_index):
        self.battle_zone.append(self.hand.pop(hand_index))

    def hand_to_graveyard(self, hand_index):
        self.graveyard.append(self.hand.pop(hand_index))

    def graveyard_to_hand(self, graveyard_index):
        self.hand.append(self.graveyard.pop(graveyard_index))

    def graveyard_to_mana_zone(self, graveyard_index):
        self.mana_zone.append(self.graveyard.pop(graveyard_index))

    def battle_zone_to_hand(self, index):
        card = self.battle_zone.pop(index)
        card.untap()
        card.sickness()
        self.hand.append(card)

    def battle_zone_to_graveyard(self, index):
        card = self.battle_zone.pop(index)
        card.untap()
        card.sickness()
        self.graveyard.append(card)

    def battle_zone_to_mana_zone(self, index):
        card = self.battle_zone.pop(index)
        card.untap()
        card.sickness()
        self.mana_zone.append(card)

    def shuffle(self):
        self.deck = random.sample(self.deck, len(self.deck))

    def untap_mana(self):
        for card in self.mana_zone:
            card.is_tap = False

    def untap_battle_zone(self):
        for creature in self.battle_zone:
            creature.is_tap = False

    def cure_summoning_sickness(self):
        for creature in self.battle_zone:
            creature.is_summoning_sickness = False

    def break_shield(self, break_shield):
        shield_triggers = []
        sorted_indices = sorted(break_shield, reverse=True)
        for shield_index in sorted_indices:
            card_index = self.shield_zone_to_hand(int(shield_index))
            if 'shieldTrigger' in self.hand[card_index]._static_abilities:
                shield_triggers.append(card_index)
        return shield_triggers

    def count_available_mana(self):
        self.available_mana = len([mana for mana in self.mana_zone if not mana.is_tap])
        return self.available_mana

    def to_dict(self):
        return {
            'name': self.name,
            'number': self.number,
            'deck': [card.to_dict() for card in self.deck],
            'shield_zone': [card.to_dict() for card in self.shield_zone],
            'hand': [card.to_dict() for card in self.hand],
            'mana_zone': [card.to_dict() for card in self.mana_zone],
            'graveyard': [card.to_dict() for card in self.graveyard],
            'battle_zone': [card.to_dict() for card in self.battle_zone],
            'available_mana': self.count_available_mana()
        }
