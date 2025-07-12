card_list = [
    {
        'id': 'dm01-s03', 'name': 'アクア・スナイパー', 'civilizations': ['water'],
        'cost': 8, 'power': 5000, 'race': ['リキッド・ピープル'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'AllActiveBattleZoneToHandAbility', 'select_count': 2, 'zone_cards': lambda x, y: x.battle_zone + y.battle_zone, 'compulsion': False}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-s04', 'name': 'キング・オリオン', 'civilizations': ['water'],
        'cost': 7, 'power': 6000, 'race': ['リヴァイアサン'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['doubleBreaker', 'unBlockable'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-s07', 'name': 'クリムゾン・ワイバーン', 'civilizations':  ['fire'],
        'cost': 8, 'power': 3000, 'race': ['アーマード・ワイバーン'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'AllDestroyAbility', 'conditions': lambda x: 'blocker' in x._static_abilities}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-001', 'name': '天空の守護者グラン・ギューレ', 'civilizations':  ['light'],
        'cost': 6, 'power': 9000, 'race': ['ガーディアン'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['blocker', 'notAttackPlayer'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-003', 'name': 'キング・ポセイドン', 'civilizations': ['water'],
        'cost': 7, 'power': 5000, 'race': ['リヴァイアサン'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'SelfDrawAbility', 'select_count': 2}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-004', 'name': 'シーマイン', 'civilizations':  ['water'],
        'cost': 6, 'power': 4000, 'race': ['フィッシュ'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['blocker'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-005', 'name': '妖姫シルフィ', 'civilizations': ['darkness'],
        'cost': 8, 'power': 4000, 'race': ['ダークロード'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'AllDestroyAbility', 'conditions': lambda x: x.power <= 3000}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-006', 'name': 'ギガルゴン', 'civilizations': ['darkness'],
        'cost': 8, 'power': 3000, 'race': ['キマイラ'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'SelfActiveGraveyardToHandAbility', 'select_count': 2, 'zone_cards': lambda x, y: [card.set_index(i) for i, card in enumerate(x.graveyard) if card.card_type == 'creature']}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-007', 'name': 'ガトリング・ワイバーン', 'civilizations': ['fire'],
        'cost': 7, 'power': 7000, 'race': ['アーマード・ワイバーン'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['doubleBreaker', 'unTapKiller'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-010', 'name': 'トゲ刺しマンドラ', 'civilizations': ['nature'],
        'cost': 5, 'power': 4000, 'race': ['ツリーフォーク'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'SelfActiveGraveyardToManaZoneAbility', 'select_count': 1, 'zone_cards': lambda x, y: [card.set_index(i) for i, card in enumerate(x.graveyard) if card.card_type == 'creature']}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-011', 'name': '黄昏の守護者シーブス・キーン', 'civilizations': ['light'],
        'cost': 5, 'power': 6000, 'race': ['ガーディアン'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['blocker', 'notAttackPlayer'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-012', 'name': '粛清の伝道師ラー', 'civilizations': ['light'],
        'cost': 5, 'power': 5500, 'race': ['バーサーカー'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-013', 'name': '月光の守護者ディア・ノーク', 'civilizations': ['light'],
        'cost': 4, 'power': 5000, 'race': ['ガーディアン'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['blocker', 'notAttackPlayer'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-014', 'name': '予言者キリアス', 'civilizations': ['light'],
        'cost': 4, 'power': 2500, 'race': ['ライトブリンガー'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['moyashi'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-015', 'name': 'ホーリー・スパーク', 'civilizations': ['light'],
        'cost': 6, 'power': None, 'race': [], 'card_type': 'spell',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'OpponentTapAllAbility'}],
        'static_abilities': ['shieldTrigger'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-018', 'name': 'ソーサーヘッド・シャーク', 'civilizations': ['water'],
        'cost': 5, 'power': 3000, 'race': ['ゲル・フィッシュ'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'AllBattleZoneToHandAbility', 'conditions': lambda x: x.power <= 2000}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-020', 'name': '一角魚', 'civilizations': ['water'],
        'cost': 4, 'power': 1000, 'race': ['フィッシュ'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'AllActiveBattleZoneToHandAbility', 'select_count': 1, 'zone_cards': lambda x, y: x.battle_zone + y.battle_zone, 'compulsion': False}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-021', 'name': 'テレポーテーション', 'civilizations': ['water'],
        'cost': 5, 'power': None, 'race': [], 'card_type': 'spell',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'AllActiveBattleZoneToHandAbility', 'select_count': 2, 'zone_cards': lambda x, y: x.battle_zone + y.battle_zone, 'compulsion': False}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-027', 'name': 'デーモン・ハンド', 'civilizations': ['darkness'],
        'cost': 6, 'power': None, 'race': [], 'card_type': 'spell',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'OpponentActiveDestroyAbility', 'select_count': 1, 'zone_cards': lambda x, y: y.battle_zone}],
        'static_abilities': ['shieldTrigger'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-033', 'name': 'マグマ・ゲイザー', 'civilizations': ['fire'],
        'cost': 3, 'power': None, 'race': [], 'card_type': 'spell',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'magumageizaaAbility', 'select_count': 1, 'zone_cards': lambda x, y: x.battle_zone, 'compulsion': True}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-035', 'name': 'シェル・ストーム', 'civilizations': ['nature'],
        'cost': 7, 'power': 2000, 'race': ['コロニー・ビートル'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'OpponentActiveBattleZoneToManaZoneAbility', 'select_count': 1, 'zone_cards': lambda x, y: y.battle_zone, 'passive': True}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-039', 'name': 'ナチュラル・トラップ', 'civilizations': ['nature'],
        'cost': 6, 'power': None, 'race': [], 'card_type': 'spell',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'OpponentActiveBattleZoneToManaZoneAbility', 'select_count': 1, 'zone_cards': lambda x, y: y.battle_zone}],
        'static_abilities': ['shieldTrigger'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-041', 'name': '希望の使徒トール', 'civilizations': ['light'],
        'cost': 5, 'power': 2000, 'race': ['イニシエート'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnEndSelfTurnAbility', 'name': 'SelfUnTapAllAbility'}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-042', 'name': '追跡の使徒ローク', 'civilizations': ['light'],
        'cost': 4, 'power': 4000, 'race': ['イニシエート'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-048', 'name': 'リボルバー・フィッシュ', 'civilizations': ['water'],
        'cost': 4, 'power': 5000, 'race': ['ゲル・フィッシュ'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['blocker', 'notAttack'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-050', 'name': 'アクア・ソルジャー', 'civilizations': ['water'],
        'cost': 3, 'power': 1000, 'race': ['リキッド・ピープル'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['moyashi'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-052', 'name': 'サイバー・ブレイン', 'civilizations': ['water'],
        'cost': 4, 'power': None, 'race': [], 'card_type': 'spell',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'SelfDrawAbility', 'select_count': 3}],
        'static_abilities': ['shieldTrigger'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-054', 'name': '嘲りの影マスクド・ホラー', 'civilizations': ['darkness'],
        'cost': 5, 'power': 1000, 'race': ['ゴースト'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'OpponentHandToGraveyardAbility'}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-056', 'name': '捕らえる者ボーン・スパイダー', 'civilizations': ['darkness'],
        'cost': 3, 'power': 5000, 'race': ['リビング・デッド'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['winDestroy'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-069', 'name': 'シビレアシダケ', 'civilizations': ['nature'],
        'cost': 2, 'power': 1000, 'race': ['バルーン・マッシュルーム'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'SelfActiveHandToManaZoneAbility', 'select_count': 1, 'zone_cards': lambda x, y: x.hand}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-071', 'name': '翡翠樹', 'civilizations': ['light'],
        'cost': 3, 'power': 4000, 'race': ['スターライト・ツリー'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['blocker', 'notAttackPlayer'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-072', 'name': '弾丸の使徒イーレ', 'civilizations': ['light'],
        'cost': 3, 'power': 3000, 'race': ['イニシエート'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-074', 'name': '碧玉草', 'civilizations': ['light'],
        'cost': 2, 'power': 3000, 'race': ['スターライト・ツリー'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['blocker', 'notAttackPlayer'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-075', 'name': '予言者リュゾル', 'civilizations': ['light'],
        'cost': 2, 'power': 2000, 'race': ['ライトブリンガー'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-079', 'name': 'ファントム・フィッシュ', 'civilizations': ['water'],
        'cost': 3, 'power': 4000, 'race': ['ゲル・フィッシュ'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['blocker', 'notAttack'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-080', 'name': 'アクア・ハルカス', 'civilizations': ['water'],
        'cost': 3, 'power': 2000, 'race': ['リキッド・ピープル'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'SelfDrawAbility', 'select_count': 1}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-083', 'name': 'アクア・ビークル', 'civilizations': ['water'],
        'cost': 2, 'power': 1000, 'race': ['リキッド・ピープル'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-086', 'name': 'スパイラル・ゲート', 'civilizations': ['water'],
        'cost': 2, 'power': None, 'race': [], 'card_type': 'spell',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'AllActiveBattleZoneToHandAbility', 'select_count': 1, 'zone_cards': lambda x, y: x.battle_zone + y.battle_zone, 'compulsion': True}],
        'static_abilities': ['shieldTrigger'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-093', 'name': 'デス・スモーク', 'civilizations': ['darkness'],
        'cost': 4, 'power': None, 'race': [], 'card_type': 'spell',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'OpponentActiveDestroyAbility', 'select_count': 1, 'zone_cards': lambda x, y: [creature.set_index(i) for i, creature in enumerate(y.battle_zone) if not creature.is_tap]}],
        'static_abilities': [''], 'mana_symbol': 1
    },
    {
        'id': 'dm01-094', 'name': 'ゴースト・タッチ', 'civilizations': ['darkness'],
        'cost': 2, 'power': None, 'race': [], 'card_type': 'spell',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'OpponentHandToGraveyardAbility'}],
        'static_abilities': ['shieldTrigger'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-097', 'name': '不死身男爵ボーグ', 'civilizations': ['fire'],
        'cost': 2, 'power': 2000, 'race': ['ヒューマノイド'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-098', 'name': '喧嘩屋タイラー', 'civilizations': ['fire'],
        'cost': 2, 'power': 1000, 'race': ['ヒューマノイド'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['powerAttacker2000'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-100', 'name': '凶戦士ブレイズ・クロー', 'civilizations': ['fire'],
        'cost': 1, 'power': 1000, 'race': ['ドラゴノイド'], 'card_type': 'creature',
        'trigger_abilities': [], 'static_abilities': ['mustAttack'], 'mana_symbol': 1
    },
    {
        'id': 'dm01-106', 'name': '青銅の鎧', 'civilizations': ['nature'],
        'cost': 3, 'power': 1000, 'race': ['ビーストフォーク'], 'card_type': 'creature',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'SelfDeckToManaZoneAbility', 'fixed_count': 1}],
        'static_abilities': [], 'mana_symbol': 1
    },
    {
        'id': 'dm01-109', 'name': 'アルティメット・フォース', 'civilizations': ['nature'],
        'cost': 5, 'power': None, 'race': [], 'card_type': 'spell',
        'trigger_abilities': [{'type': 'OnPlayAbility', 'name': 'SelfDeckToManaZoneAbility', 'fixed_count': 2}],
        'static_abilities': [], 'mana_symbol': 1
    },
]
