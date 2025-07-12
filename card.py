import uuid
from ability import *


class Card:
    def __init__(self, id, name, civilizations, cost, power, race, card_type, trigger_abilities, static_abilities, mana_symbol):
        self.instance_id = str(uuid.uuid4())
        self.id = id
        self.name = name
        self.civilizations = civilizations
        self.cost = cost
        self.power = power
        self.race = race
        self.card_type = card_type
        self._trigger_abilities = []
        self._static_abilities = static_abilities
        self.mana_symbol = mana_symbol
        self.is_tap = False
        self.current_index = None

        for ab_data in trigger_abilities:
            ability_type = ab_data.get('type')
            ability_name = ab_data.get('name')
            ability_select_count = ab_data.get('select_count')
            ability_fixed_count = ab_data.get('fixed_count')
            ability_zone_cards = ab_data.get('zone_cards')
            ability_conditions = ab_data.get('conditions')
            ability_compulsion = ab_data.get('compulsion')
            ability_passive = ab_data.get('passive') or False
            if ability_name == 'AllActiveBattleZoneToHandAbility':
                self._trigger_abilities.append(AllActiveBattleZoneToHandAbility(ability_select_count, ability_zone_cards, ability_compulsion))
            if ability_name == 'magumageizaaAbility':
                self._trigger_abilities.append(magumageizaaAbility(ability_select_count, ability_zone_cards, ability_compulsion))
            if ability_name == 'SelfActiveHandToManaZoneAbility':
                self._trigger_abilities.append(SelfActiveHandToManaZoneAbility(ability_select_count, ability_zone_cards))
            if ability_name == 'OpponentActiveDestroyAbility':
                self._trigger_abilities.append(OpponentActiveDestroyAbility(ability_select_count, ability_zone_cards))
            if ability_name == 'OpponentActiveBattleZoneToManaZoneAbility':
                self._trigger_abilities.append(OpponentActiveBattleZoneToManaZoneAbility(ability_select_count, ability_zone_cards, ability_passive))
            if ability_name == 'SelfActiveGraveyardToHandAbility':
                self._trigger_abilities.append(SelfActiveGraveyardToHandAbility(ability_select_count, ability_zone_cards))
            if ability_name == 'SelfActiveGraveyardToManaZoneAbility':
                self._trigger_abilities.append(SelfActiveGraveyardToManaZoneAbility(ability_select_count, ability_zone_cards))
            if ability_name == 'SelfDrawAbility':
                self._trigger_abilities.append(SelfDrawAbility(ability_select_count))
            if ability_name == 'AllDestroyAbility':
                self._trigger_abilities.append(AllDestroyAbility(ability_conditions))
            if ability_name == 'AllBattleZoneToHandAbility':
                self._trigger_abilities.append(AllBattleZoneToHandAbility(ability_conditions))
            if ability_name == 'OpponentHandToGraveyardAbility':
                self._trigger_abilities.append(OpponentHandToGraveyardAbility())
            if ability_name == 'OpponentTapAllAbility':
                self._trigger_abilities.append(OpponentTapAllAbility())
            if ability_name == 'SelfUnTapAllAbility':
                self._trigger_abilities.append(SelfUnTapAllAbility())
            if ability_name == 'SelfDeckToManaZoneAbility':
                self._trigger_abilities.append(SelfDeckToManaZoneAbility(ability_fixed_count))

    def get_on_play_abilities(self):
        return [ab for ab in self._trigger_abilities if isinstance(ab, OnPlayAbility)]
    
    def get_on_end_self_turn_abilities(self):
        return [ab for ab in self._trigger_abilities if isinstance(ab, OnEndSelfTurnAbility)]

    def tap(self):
        self.is_tap = True

    def untap(self):
        self.is_tap = False

    def play(self):
        pass

    def set_index(self, index):
        self.current_index = index
        return self
    
    # def unset_index(self):
    #     self.current_index = None

    def to_dict(self):
        return {
            'instance_id': self.instance_id,
            'id': self.id,
            'name': self.name,
            'civilizations': self.civilizations,
            'cost': self.cost,
            'power': self.power,
            'race': self.race,
            'card_type': self.card_type,
            'abilities': None,
            'mana_symbol': self.mana_symbol,
            'is_tap': self.is_tap,
            'current_index': self.current_index
        }


class Creature(Card):
    def __init__(self, id, name, civilizations, cost, power, race, card_type, trigger_abilities, static_abilities, mana_symbol):
        super().__init__(id, name, civilizations, cost, power, race, card_type, trigger_abilities, static_abilities, mana_symbol)
        self.is_summoning_sickness = True

    def play(self):
        pass

    def sickness(self):
        self.is_summoning_sickness = True

    def to_dict(self):
        return {
            **super().to_dict(),
            'is_summoning_sickness': self.is_summoning_sickness
        }


class Spell(Card):
    def __init__(self, id, name, civilizations, cost, power, race, card_type, trigger_abilities, static_abilities, mana_symbol):
        super().__init__(id, name, civilizations, cost, power, race, card_type, trigger_abilities, static_abilities, mana_symbol)

    def play(self):
        pass


class CardFactory:
    @staticmethod
    def create_card(card):
        if card['card_type'] == 'creature':
            return Creature(card['id'], card['name'], card['civilizations'], card['cost'], card['power'], card['race'], card['card_type'], card['trigger_abilities'], card['static_abilities'], card['mana_symbol'])
        if card['card_type'] == 'spell':
            return Spell(card['id'], card['name'], card['civilizations'], card['cost'], card['power'], card['race'], card['card_type'], card['trigger_abilities'], card['static_abilities'], card['mana_symbol'])
