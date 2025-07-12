import random
import itertools


class Turn:
    def __init__(self):
        self.active_player = None
        self.inactive_player = None
        self.mana_charged = False
        self.card_played = False
        self.attacked = False
        self.stock = []
        self.pending_card = None

    def set_pending_card(self, card_uuid):
        self.pending_card = card_uuid

    def decide_first_player(self, player1, player2):
        self.active_player = random.choice([player1, player2])
        self.inactive_player = player1 if self.active_player == player2 else player2

    def start(self):
        self.active_player.untap_mana()
        self.active_player.untap_battle_zone()
        self.active_player.cure_summoning_sickness()
        self.active_player.deck_to_hand()

    def end(self):
        # for creature in self.active_player.battle_zone:
        #     for ability in creature.get_on_end_self_turn_abilities():
        #         if hasattr(ability, 'ability_conditions'):
        #             self.stock.append(ability)
        #         else:
        #             ability.activate(self.active_player, self.inactive_player)
        self.active_player, self.inactive_player = self.inactive_player, self.active_player
        self.mana_charged = False
        self.card_played = False
        self.attacked = False

    def can_charge_mana(self):
        if self.card_played or self.attacked:
            return False, 'チャージステップは終了しています。'
        if self.mana_charged:
            return False, '既にマナチャージをしています。'
        return True, None

    def charge_mana(self, card_uuid):
        card = next(card for card in self.active_player.hand if card.instance_id == card_uuid)
        self.active_player.hand_to_mana_zone(card)
        self.mana_charged = True

    def can_play_card(self, card_uuid):
        card = next(card for card in self.active_player.hand if card.instance_id == card_uuid)
        if self.attacked:
            return False, 'プレイステップは終了しています。', None
        if card.cost > self.active_player.available_mana:
            return False, 'マナの数が足りません。', None
        return True, None, card.cost

    def can_use_mana(self, card_uuid, mana_used):
        card = next(card for card in self.active_player.hand if card.instance_id == card_uuid)
        if card.cost > len(mana_used):
            return False, 'マナの数が足りません。'
        for civilization in card.civilizations:
            if not civilization in list(itertools.chain.from_iterable([next(card for card in self.active_player.mana_zone if card.instance_id == mana_index).civilizations for mana_index in mana_used])):
                return False, 'マナの文明が足りません。'
        for mana_index in mana_used:
            if next(card for card in self.active_player.mana_zone if card.instance_id == mana_index).is_tap:
                return False, 'タップ済みのカードはタップできません。'
        return True, None

    def play_card(self, card_uuid, mana_used):
        for mana_index in mana_used:
            next(card for card in self.active_player.mana_zone if card.instance_id == mana_index).tap()
        self.card_played = True
        card = next(card for card in self.active_player.hand if card.instance_id == card_uuid)
        for ability in card.get_on_play_abilities():
            if hasattr(ability, 'ability_conditions'):
                    if ability.ability_conditions == 'count':
                        self.stock.append(ability)
                    if ability.ability_conditions == 'select':
                        if not len(ability.zone_cards(self.active_player, self.inactive_player)) == 0:
                            self.stock.append(ability)
            else:
                ability.activate(self.active_player, self.inactive_player)
        if card.card_type == 'creature':
            self.active_player.hand_to_battle_zone(card)
        if card.card_type == 'spell':
            self.active_player.hand_to_graveyard(card)

    def can_use_random(self, card_uuid):
        card = next(card for card in self.active_player.hand if card.instance_id == card_uuid)
        mana_used = []
        for i, mana in enumerate(self.active_player.mana_zone):
            if card.civilizations[0] in mana.civilizations and not mana.is_tap:
                mana_used.append(i)
                break
        if not mana_used:
            return False, 'マナの文明が足りません。', None
        if card.cost != 1:
            for i, mana in enumerate(self.active_player.mana_zone):
                if not mana_used[0] == i and not mana.is_tap:
                    mana_used.append(i)
                    if len(mana_used) == card.cost:
                        break
        if card.cost > len(mana_used):
            return False, 'マナの数が足りません。', None
        for civilization in card.civilizations:
            if not civilization in list(itertools.chain.from_iterable([self.active_player.mana_zone[int(mana_index)].civilizations for mana_index in mana_used])):
                return False, 'マナの文明が足りません。', None
        for mana_index in mana_used:
            if self.active_player.mana_zone[int(mana_index)].is_tap:
                return False, 'タップ済みのカードはタップできません。', None
        return True, None, mana_used
    
    def random_tap_play_card(self, card_uuid, mana_used):
        card = next(card for card in self.active_player.hand if card.instance_id == card_uuid)
        for mana_index in mana_used:
            self.active_player.mana_zone[int(mana_index)].tap()
        self.card_played = True
        for ability in card.get_on_play_abilities():
            if hasattr(ability, 'ability_conditions'):
                    if ability.ability_conditions == 'count':
                        self.stock.append(ability)
                    if ability.ability_conditions == 'select':
                        if not len(ability.zone_cards(self.active_player, self.inactive_player)) == 0:
                            self.stock.append(ability)
            else:
                ability.activate(self.active_player, self.inactive_player)
        if card.card_type == 'creature':
            self.active_player.hand_to_battle_zone(card)
        if card.card_type == 'spell':
            self.active_player.hand_to_graveyard(card)

    def play_shield_trigger(self, hand_index):
        card = next(card for card in self.inactive_player.hand if card.instance_id == hand_index)
        for ability in card.get_on_play_abilities():
            if hasattr(ability, 'ability_conditions'):
                    if ability.ability_conditions == 'count':
                        self.stock.append(ability)
                    if ability.ability_conditions == 'select':
                        if not len(ability.zone_cards(self.inactive_player, self.active_player)) == 0:
                            self.stock.append(ability)
            else:
                ability.activate(self.inactive_player, self.active_player)
        if card.card_type == 'creature':
            self.inactive_player.hand_to_battle_zone(card)
        if card.card_type == 'spell':
            self.inactive_player.hand_to_graveyard(card)

    def can_attack_player(self, card_uuid):
        creature = next(card for card in self.active_player.battle_zone if card.instance_id == card_uuid)
        if 'notAttackPlayer' in creature._static_abilities:
            return False, None, 'このクリーチャーは相手プレイヤーを攻撃できません。'
        if 'notAttack' in creature._static_abilities:
            return False, None, 'このクリーチャーは攻撃できません。'
        if creature.is_tap:
            return False, None, 'このクリーチャーはタップしています。'
        if creature.is_summoning_sickness:
            return False, None, 'このクリーチャーは召喚酔いしています。'
        break_count = 1
        if 'doubleBreaker' in creature._static_abilities:
            break_count = 2
        if 'magumageizaa' in creature._static_abilities:
            break_count = 2
        return True, break_count, None

    def can_break_shield(self, battle_zone_index, break_shield):
        creature = next(card for card in self.active_player.battle_zone if card.instance_id == battle_zone_index)
        break_count = 1
        if 'doubleBreaker' in creature._static_abilities:
            break_count = 2
        if 'magumageizaa' in creature._static_abilities:
            break_count = 2
        if 'notAttack' in creature._static_abilities:
            return False, 'このクリーチャーは攻撃できません。'
        if not break_count == len(break_shield) and not len(self.inactive_player.shield_zone) <= break_count:
            return False, 'ブレイクする枚数が違います。'
        return True, None

    def break_shield(self, battle_zone_index, break_shield):
        creature = next(card for card in self.active_player.battle_zone if card.instance_id == battle_zone_index)
        creature.tap()
        self.attacked = True
        shield_triggers = self.inactive_player.break_shield(break_shield)
        if shield_triggers:
            return shield_triggers

    def direct_attack(self, battle_zone_index):
        creature = next(card for card in self.active_player.battle_zone if card.instance_id == battle_zone_index)
        creature.tap()
        self.attacked = True

    def can_attack_creature(self, battle_zone_index):
        creature = next(card for card in self.active_player.battle_zone if card.instance_id == battle_zone_index)
        if creature.is_tap:
            return False, 'このクリーチャーはタップしています。'
        if creature.is_summoning_sickness:
            return False, 'このクリーチャーは召喚酔いしています。'
        if len(self.inactive_player.battle_zone) == 0:
            return False, '相手のバトルゾーンにクリーチャーがいません。'
        return True, None

    def can_battle(self, battle_zone_index, attack_target_index):
        attack_creature = next(card for card in self.active_player.battle_zone if card.instance_id == battle_zone_index)
        target_creature = next(card for card in self.inactive_player.battle_zone if card.instance_id == attack_target_index)
        if not target_creature.is_tap and not 'unTapKiller' in attack_creature._static_abilities:
            return False, 'そのクリーチャーにはアタックできません。'
        return True, None

    def battle(self, battle_zone_index, attack_target_index):
        attack_creature = next(card for card in self.active_player.battle_zone if card.instance_id == battle_zone_index)
        target_creature = next(card for card in self.inactive_player.battle_zone if card.instance_id == attack_target_index)
        if 'powerAttacker2000' in attack_creature._static_abilities:
            attack_creature.power += 2000
        elif 'magumageizaa' in attack_creature._static_abilities:
            attack_creature.power += 4000
        attack_creature.tap()
        self.attacked = True
        if (attack_creature.power == target_creature.power):
            self.active_player.battle_zone_to_graveyard(attack_creature)
            self.inactive_player.battle_zone_to_graveyard(target_creature)
        elif (attack_creature.power > target_creature.power):
            self.inactive_player.battle_zone_to_graveyard(target_creature)
            if 'winDestroy' in attack_creature._static_abilities:
                self.active_player.battle_zone_to_graveyard(attack_creature)
        elif (attack_creature.power < target_creature.power):
            self.active_player.battle_zone_to_graveyard(attack_creature)
            if 'winDestroy' in target_creature._static_abilities:
                self.active_player.battle_zone_to_graveyard(target_creature)
        if 'powerAttacker2000' in attack_creature._static_abilities:
            attack_creature.power -= 2000
        elif 'magumageizaa' in attack_creature._static_abilities:
            attack_creature.power -= 4000

    def block(self, battle_zone_index, blocker_index):
        attack_creature = next(card for card in self.active_player.battle_zone if card.instance_id == battle_zone_index)
        target_creature = next(card for card in self.inactive_player.battle_zone if card.instance_id == blocker_index)
        if 'powerAttacker2000' in attack_creature._static_abilities:
            attack_creature.power += 2000
        elif 'magumageizaa' in attack_creature._static_abilities:
            attack_creature.power += 4000
        attack_creature.tap()
        target_creature.tap()
        self.attacked = True
        if (attack_creature.power == target_creature.power):
            self.active_player.battle_zone_to_graveyard(battle_zone_index)
            self.inactive_player.battle_zone_to_graveyard(target_creature)
        elif (attack_creature.power > target_creature.power):
            self.inactive_player.battle_zone_to_graveyard(target_creature)
            if 'winDestroy' in attack_creature._static_abilities:
                self.active_player.battle_zone_to_graveyard(attack_creature)
        elif (attack_creature.power < target_creature.power):
            self.active_player.battle_zone_to_graveyard(attack_creature)
            if 'winDestroy' in target_creature._static_abilities:
                self.active_player.battle_zone_to_graveyard(target_creature)
        if 'powerAttacker2000' in attack_creature._static_abilities:
            attack_creature.power -= 2000
        elif 'magumageizaa' in attack_creature._static_abilities:
            attack_creature.power -= 4000

    def ability_execute(self, battle_zone_index):
        ability = self.stock.pop(0)
        ability.activate(self.active_player, self.inactive_player, battle_zone_index)

    def get_blockers(self, card_uuid):
        attacker = next(card for card in self.active_player.battle_zone if card.instance_id == card_uuid)
        if 'unBlockable' in attacker._static_abilities:
            return []
        return [i for i, creature in enumerate(self.inactive_player.battle_zone) if 'blocker' in creature._static_abilities and not creature.is_tap]

    def to_dict(self):
        return {
            'active_player': self.active_player.to_dict(),
            'inactive_player': self.inactive_player.to_dict(),
            'mana_charged': self.mana_charged,
            'card_played': self.card_played,
            'attacked': self.attacked,
        }
