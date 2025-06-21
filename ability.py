import random

from abc import ABC, abstractmethod


class CardAbility(ABC):
    def __init__(self, name):
        self.name = name

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
        super().__init__("Destruction")
        self.select_count = select_count
        self.zone_cards = zone_cards

    def activate(self, active_player, inactive_player, graveyard_index):
        sorted_indices = sorted(graveyard_index, reverse=True)
        for index in sorted_indices:
            active_player.graveyard_to_hand(int(index))


class SelfActiveGraveyardToManaZoneAbility(OnPlayAbility):
    ability_conditions = 'select'
    compulsion = False

    def __init__(self, select_count, zone_cards):
        super().__init__("Destruction")
        self.select_count = select_count
        self.zone_cards = zone_cards

    def activate(self, active_player, inactive_player, graveyard_index):
        sorted_indices = sorted(graveyard_index, reverse=True)
        for index in sorted_indices:
            active_player.graveyard_to_mana_zone(int(index))


class SelfDrawAbility(OnPlayAbility):
    ability_conditions = 'count'

    def __init__(self, select_count):
        super().__init__("Destruction")
        self.select_count = select_count

    def activate(self, active_player, inactive_player, count):
        for _ in range(count):
            active_player.deck_to_hand()


class OpponentActiveDestroyAbility(OnPlayAbility):
    ability_conditions = 'select'
    compulsion = True

    def __init__(self, select_count, zone_cards):
        super().__init__("Destruction")
        self.select_count = select_count
        self.zone_cards = zone_cards

    def activate(self, active_player, inactive_player, battle_zone_index):
        sorted_indices = sorted(battle_zone_index, reverse=True)
        for index in sorted_indices:
            inactive_player.battle_zone_to_graveyard(int(index))


class OpponentActiveBattleZoneToManaZoneAbility(OnPlayAbility):
    ability_conditions = 'select'
    compulsion = True

    def __init__(self, select_count, zone_cards, passive):
        super().__init__("Destruction")
        self.select_count = select_count
        self.zone_cards = zone_cards
        self.passive = passive

    def activate(self, active_player, inactive_player, battle_zone_index):
        sorted_indices = sorted(battle_zone_index, reverse=True)
        for index in sorted_indices:
            inactive_player.battle_zone_to_mana_zone(int(index))


class SelfActiveHandToManaZoneAbility(OnPlayAbility):
    ability_conditions = 'select'
    compulsion = False

    def __init__(self, select_count, zone_cards):
        super().__init__("Destruction")
        self.select_count = select_count
        self.zone_cards = zone_cards

    def activate(self, active_player, inactive_player, hand_index):
        sorted_indices = sorted(hand_index, reverse=True)
        for index in sorted_indices:
            active_player.hand_to_mana_zone(int(index))


class SelfDeckToManaZoneAbility(OnPlayAbility):
    def __init__(self, fixed_count):
        super().__init__("Destruction")
        self.fixed_count = fixed_count

    def activate(self, active_player, inactive_player):
        for _ in range(self.fixed_count):
            active_player.deck_to_mana_zone(0)


class DeckToMana2Ability(OnPlayAbility):
    def __init__(self):
        super().__init__("Destruction")

    def activate(self, active_player, inactive_player):
        active_player.deck_to_mana_zone(0)
        active_player.deck_to_mana_zone(0)


class AllActiveBattleZoneToHandAbility(OnPlayAbility):
    ability_conditions = 'select'

    def __init__(self, select_count, zone_cards, compulsion):
        super().__init__("Destruction")
        self.select_count = select_count
        self.zone_cards = zone_cards
        self.compulsion = compulsion

    def activate(self, active_player, inactive_player, battle_zone_index):
        sorted_indices = sorted(battle_zone_index, reverse=True)
        for index in sorted_indices:
            if int(index) > len(active_player.battle_zone) - 1:
                inactive_player.battle_zone_to_hand(int(index) - len(active_player.battle_zone))
            else:
                active_player.battle_zone_to_hand(int(index))


class AllDestroyAbility(OnPlayAbility):
    def __init__(self, conditions):
        super().__init__("All Destruction")
        self.conditions = conditions

    def activate(self, active_player, inactive_player):
        for i in range(len(active_player.battle_zone) - 1, -1, -1):
            creature = active_player.battle_zone[i]
            if self.conditions(creature):
                active_player.battle_zone_to_graveyard(i)

        for i in range(len(inactive_player.battle_zone) - 1, -1, -1):
            creature = inactive_player.battle_zone[i]
            if self.conditions(creature):
                inactive_player.battle_zone_to_graveyard(i)


class AllBattleZoneToHandAbility(OnPlayAbility):
    def __init__(self, conditions):
        super().__init__("All Destruction")
        self.conditions = conditions

    def activate(self, active_player, inactive_player):
        for i in range(len(active_player.battle_zone) - 1, -1, -1):
            creature = active_player.battle_zone[i]
            if self.conditions(creature):
                active_player.battle_zone_to_hand(i)

        for i in range(len(inactive_player.battle_zone) - 1, -1, -1):
            creature = inactive_player.battle_zone[i]
            if self.conditions(creature):
                inactive_player.battle_zone_to_hand(i)


class OpponentHandToGraveyardAbility(OnPlayAbility):
    def __init__(self):
        super().__init__("RandomHandDestruction")

    def activate(self, active_player, inactive_player):
        inactive_player.hand_to_graveyard(random.randint(0, len(inactive_player.hand) - 1))


class OpponentTapAllAbility(OnPlayAbility):
    def __init__(self):
        super().__init__("All Tap")

    def activate(self, active_player, inactive_player):
        for creature in inactive_player.battle_zone:
            if not creature.is_tap:
                creature.tap()


class SelfUnTapAllAbility(OnEndSelfTurnAbility):
    ability_conditions = 'optional'

    def __init__(self):
        super().__init__("All UnTap")

    def activate(self, active_player, inactive_player):
        for creature in active_player.battle_zone:
            creature.untap()
