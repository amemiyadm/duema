import random

from abc import ABC, abstractmethod


class CardAbility(ABC):
    def to_dict(self):
        return {'name': self.name}


class OnPlayAbility(CardAbility):
    @abstractmethod
    def activate(self, active_player, inactive_player):
        pass


class OnEndSelfTurnAbility(CardAbility):
    @abstractmethod
    def activate(self, active_player, inactive_player):
        pass


class SelfActiveGraveyardToHandAbility(OnPlayAbility):
    ability_conditions = 'select'
    compulsion = False

    def __init__(self, select_count, zone_cards):
        self.select_count = select_count
        self.zone_cards = zone_cards

    def activate(self, active_player, inactive_player, graveyard_index):
        sorted_indices = sorted(graveyard_index, reverse=True)
        for index in sorted_indices:
            card = next(card for card in active_player.graveyard if card.instance_id == index)
            active_player.graveyard_to_hand(card)


class SelfActiveGraveyardToManaZoneAbility(OnPlayAbility):
    ability_conditions = 'select'
    compulsion = False

    def __init__(self, select_count, zone_cards):
        self.select_count = select_count
        self.zone_cards = zone_cards

    def activate(self, active_player, inactive_player, graveyard_index):
        sorted_indices = sorted(graveyard_index, reverse=True)
        for index in sorted_indices:
            card = next(card for card in active_player.graveyard if card.instance_id == index)
            active_player.graveyard_to_mana_zone(card)


class SelfDrawAbility(OnPlayAbility):
    ability_conditions = 'count'

    def __init__(self, select_count):
        self.select_count = select_count

    def activate(self, active_player, inactive_player, count):
        for _ in range(count):
            active_player.deck_to_hand()


class OpponentActiveDestroyAbility(OnPlayAbility):
    ability_conditions = 'select'
    compulsion = True

    def __init__(self, select_count, zone_cards):
        self.select_count = select_count
        self.zone_cards = zone_cards

    def activate(self, active_player, inactive_player, battle_zone_index):
        sorted_indices = sorted(battle_zone_index, reverse=True)
        for index in sorted_indices:
            card = next(card for card in active_player.battle_zone if card.instance_id == index)
            inactive_player.battle_zone_to_graveyard(card)


class OpponentActiveBattleZoneToManaZoneAbility(OnPlayAbility):
    ability_conditions = 'select'
    compulsion = True

    def __init__(self, select_count, zone_cards, passive):
        self.select_count = select_count
        self.zone_cards = zone_cards
        self.passive = passive

    def activate(self, active_player, inactive_player, battle_zone_index):
        sorted_indices = sorted(battle_zone_index, reverse=True)
        for index in sorted_indices:
            card = next(card for card in inactive_player.battle_zone if card.instance_id == index)
            inactive_player.battle_zone_to_mana_zone(card)


class SelfActiveHandToManaZoneAbility(OnPlayAbility):
    ability_conditions = 'select'
    compulsion = False

    def __init__(self, select_count, zone_cards):
        self.select_count = select_count
        self.zone_cards = zone_cards

    def activate(self, active_player, inactive_player, hand_index):
        sorted_indices = sorted(hand_index, reverse=True)
        for index in sorted_indices:
            card = next(card for card in active_player.hand if card.instance_id == index)
            active_player.hand_to_mana_zone(card)


class SelfDeckToManaZoneAbility(OnPlayAbility):
    def __init__(self, fixed_count):
        self.fixed_count = fixed_count

    def activate(self, active_player, inactive_player):
        for _ in range(self.fixed_count):
            active_player.deck_to_mana_zone(0)


class DeckToMana2Ability(OnPlayAbility):
    def activate(self, active_player, inactive_player):
        active_player.deck_to_mana_zone(0)
        active_player.deck_to_mana_zone(0)


class AllActiveBattleZoneToHandAbility(OnPlayAbility):
    ability_conditions = 'select'

    def __init__(self, select_count, zone_cards, compulsion):
        self.select_count = select_count
        self.zone_cards = zone_cards
        self.compulsion = compulsion

    def activate(self, active_player, inactive_player, battle_zone_index):
        sorted_indices = sorted(battle_zone_index, reverse=True)
        for index in sorted_indices:
            if card := next((card for card in active_player.battle_zone if card.instance_id == index), None):
                active_player.battle_zone_to_hand(card)
            elif card := next((card for card in inactive_player.battle_zone if card.instance_id == index), None):
                inactive_player.battle_zone_to_hand(card)

class magumageizaaAbility(OnPlayAbility):
    ability_conditions = 'select'

    def __init__(self, select_count, zone_cards, compulsion):
        self.select_count = select_count
        self.zone_cards = zone_cards
        self.compulsion = compulsion

    def activate(self, active_player, inactive_player, battle_zone_index):
        sorted_indices = sorted(battle_zone_index, reverse=True)
        for index in sorted_indices:
            card = next((card for card in active_player.battle_zone if card.instance_id == index), None)
            card._static_abilities.append('magumageizaa')


class AllDestroyAbility(OnPlayAbility):
    def __init__(self, conditions):
        self.conditions = conditions

    def activate(self, active_player, inactive_player):
        for i in range(len(active_player.battle_zone) - 1, -1, -1):
            creature = active_player.battle_zone[i]
            if self.conditions(creature):
                active_player.battle_zone_to_graveyard(creature)

        for i in range(len(inactive_player.battle_zone) - 1, -1, -1):
            creature = inactive_player.battle_zone[i]
            if self.conditions(creature):
                inactive_player.battle_zone_to_graveyard(creature)


class AllBattleZoneToHandAbility(OnPlayAbility):
    def __init__(self, conditions):
        self.conditions = conditions

    def activate(self, active_player, inactive_player):
        for i in range(len(active_player.battle_zone) - 1, -1, -1):
            creature = active_player.battle_zone[i]
            if self.conditions(creature):
                active_player.battle_zone_to_hand(creature)

        for i in range(len(inactive_player.battle_zone) - 1, -1, -1):
            creature = inactive_player.battle_zone[i]
            if self.conditions(creature):
                inactive_player.battle_zone_to_hand(creature)


class OpponentHandToGraveyardAbility(OnPlayAbility):
    def activate(self, active_player, inactive_player):
        card = inactive_player.hand[random.randint(0, len(inactive_player.hand) - 1)]
        inactive_player.hand_to_graveyard(card)


class OpponentTapAllAbility(OnPlayAbility):
    def activate(self, active_player, inactive_player):
        for creature in inactive_player.battle_zone:
            if not creature.is_tap:
                creature.tap()


class SelfUnTapAllAbility(OnEndSelfTurnAbility):
    ability_conditions = 'optional'

    def activate(self, active_player, inactive_player):
        for creature in active_player.battle_zone:
            creature.untap()
