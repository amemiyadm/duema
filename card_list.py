from card import *

card_list = [
    [
        'dm01-s03', 'アクア・スナイパー', ['water'], 8, 5000, ['リキッド・ピープル'], 'creature',
        [{'type': 'OnPlayAbility', 'name': 'AllActiveBattleZoneToHandAbility', 'select_count': 2,
            'zone_cards': lambda x, y: x.battle_zone + y.battle_zone, 'compulsion': False}],
        [], 1
    ],
    [
        'dm01-s04', 'キング・オリオン', ['water'], 7, 6000,
        ['リヴァイアサン'], 'creature', [], ['doubleBreaker', 'unBlockable'], 1
    ],
    [
        'dm01-s07', 'クリムゾン・ワイバーン', ['fire'], 8, 3000,
        ['アーマード・ワイバーン'], 'creature',
        [{'type': 'OnPlayAbility', 'name': 'AllDestroyAbility', 'conditions': lambda x: 'blocker' in x._static_abilities}], [], 1
    ],
    [
        'dm01-001', '天空の守護者グラン・ギューレ', ['light'], 6, 9000,
        ['ガーディアン'], 'creature', [], ['blocker', 'notAttackPlayer'], 1
    ],
    [
        'dm01-003', 'キング・ポセイドン', ['water'], 7, 5000,
        ['リヴァイアサン'], 'creature', [{'type': 'OnPlayAbility', 'name': 'SelfDrawAbility', 'select_count': 2}], [], 1
    ],
    [
        'dm01-005', '妖姫シルフィ', ['darkness'], 8, 4000,
        ['ダークロード'], 'creature',
        [{'type': 'OnPlayAbility', 'name': 'AllDestroyAbility', 'conditions': lambda x: x.power <= 3000}],
        [], 1
    ],
    [
        'dm01-006', 'ギガルゴン', ['darkness'], 8, 3000,
        ['キマイラ'], 'creature',
        [{'type': 'OnPlayAbility', 'name': 'SelfActiveGraveyardToHandAbility', 'select_count': 2, 'zone_cards': lambda x,
            y: [card.set_index(i) for i, card in enumerate(x.graveyard) if card.card_type == 'creature']}],
        [], 1
    ],
    [
        'dm01-007', 'ガトリング・ワイバーン', ['fire'], 7, 7000,
        ['アーマード・ワイバーン'], 'creature', [], ['doubleBreaker', 'unTapKiller'], 1
    ],
    [
        'dm01-010', 'トゲ刺しマンドラ', ['nature'], 5, 4000,
        ['ツリーフォーク'], 'creature',
        [{'type': 'OnPlayAbility', 'name': 'SelfActiveGraveyardToManaZoneAbility', 'select_count': 1, 'zone_cards': lambda x,
            y: [card.set_index(i) for i, card in enumerate(x.graveyard) if card.card_type == 'creature']}],
        [], 1
    ],
    [
        'dm01-011', '黄昏の守護者シーブス・キーン', ['light'], 5, 6000,
        ['ガーディアン'], 'creature', [], ['blocker', 'notAttackPlayer'], 1
    ],
    [
        'dm01-012', '粛清の伝道師ラー', ['light'], 5, 5500,
        ['バーサーカー'], 'creature', [], [], 1
    ],
    [
        'dm01-013', '月光の守護者ディア・ノーク', ['light'], 4, 5000,
        ['ガーディアン'], 'creature', [], ['blocker', 'notAttackPlayer'], 1
    ],
    [
        'dm01-015', 'ホーリー・スパーク', ['light'], 6, None,
        [], 'spell', [{'type': 'OnPlayAbility', 'name': 'OpponentTapAllAbility'}], ['shieldTrigger'], 1
    ],
    [
        'dm01-018', 'ソーサーヘッド・シャーク', ['water'], 5, 3000,
        ['ゲル・フィッシュ'], 'creature',
        [{'type': 'OnPlayAbility', 'name': 'AllBattleZoneToHandAbility', 'conditions': lambda x: x.power <= 2000}],
        [], 1
    ],
    [
        'dm01-020', '一角魚', ['water'], 4, 1000, ['フィッシュ'], 'creature',
        [{'type': 'OnPlayAbility', 'name': 'AllActiveBattleZoneToHandAbility', 'select_count': 1,
            'zone_cards': lambda x, y: x.battle_zone + y.battle_zone, 'compulsion': False}],
        [], 1
    ],
    [
        'dm01-027', 'デーモン・ハンド', ['darkness'], 6, None,
        [], 'spell', [{'type': 'OnPlayAbility', 'name': 'OpponentActiveDestroyAbility', 'select_count': 1, 'zone_cards': lambda x, y: y.battle_zone}],
        ['shieldTrigger'], 1
    ],
    [
        'dm01-035', 'シェル・ストーム', ['nature'], 7, 2000, ['コロニー・ビートル'], 'creature',
        [{'type': 'OnPlayAbility', 'name': 'OpponentActiveBattleZoneToManaZoneAbility', 'select_count': 1, 'zone_cards': lambda x, y: y.battle_zone, 'passive': True}],
        [], 1
    ],
    [
        'dm01-039', 'ナチュラル・トラップ', ['nature'], 6, None, [], 'spell',
        [{'type': 'OnPlayAbility', 'name': 'OpponentActiveBattleZoneToManaZoneAbility', 'select_count': 1, 'zone_cards': lambda x, y: y.battle_zone}],
        ['shieldTrigger'], 1
    ],
    [
        'dm01-041', '希望の使徒トール', ['light'], 5, 2000,
        ['イニシエート'], 'creature', [{'type': 'OnEndSelfTurnAbility', 'name': 'SelfUnTapAllAbility'}], [], 1
    ],
    [
        'dm01-042', '追跡の使徒ローク', ['light'], 4, 4000,
        ['イニシエート'], 'creature', [], [], 1
    ],
    [
        'dm01-052', 'サイバー・ブレイン', ['water'], 4, None,
        [''], 'spell', [{'type': 'OnPlayAbility', 'name': 'SelfDrawAbility', 'select_count': 3}], ['shieldTrigger'], 1
    ],
    [
        'dm01-056', '捕らえる者ボーン・スパイダー', ['darkness'], 3, 5000,
        ['リビング・デッド'], 'creature', [], ['winDestroy'], 1
    ],
    [
        'dm01-069', 'シビレアシダケ', ['nature'], 2, 1000,
        ['バルーン・マッシュルーム'], 'creature',
        [{'type': 'OnPlayAbility', 'name': 'SelfActiveHandToManaZoneAbility', 'select_count': 1, 'zone_cards': lambda x, y: x.hand}], [], 1
    ],
    [
        'dm01-071', '翡翠樹', ['light'], 3, 4000,
        ['スターライト・ツリー'], 'creature', [], ['blocker', 'notAttackPlayer'], 1
    ],
    [
        'dm01-072', '弾丸の使徒イーレ', ['light'], 3, 3000,
        ['イニシエート'], 'creature', [], [], 1
    ],
    [
        'dm01-074', '碧玉草', ['light'], 2, 3000,
        ['スターライト・ツリー'], 'creature', [], ['blocker', 'notAttackPlayer'], 1
    ],
    [
        'dm01-075', '預言者リュゾル', ['light'], 2, 2000,
        ['ライトブリンガー'], 'creature', [], [], 1
    ],
    [
        'dm01-080', 'アクア・ハルカス', ['water'], 3, 2000,
        ['リキッド・ピープル'], 'creature', [{'type': 'OnPlayAbility', 'name': 'SelfDrawAbility', 'select_count': 1}], [], 1
    ],
    [
        'dm01-083', 'アクア・ビークル', ['water'], 2, 1000,
        ['リキッド・ピープル'], 'creature', [], [], 1
    ],
    [
        'dm01-086', 'スパイラル・ゲート', ['water'], 2, None, [''], 'spell',
        [{'type': 'OnPlayAbility', 'name': 'AllActiveBattleZoneToHandAbility', 'select_count': 1,
            'zone_cards': lambda x, y: x.battle_zone + y.battle_zone, 'compulsion': True}],
        ['shieldTrigger'], 1
    ],
    [
        'dm01-093', 'デス・スモーク', ['darkness'], 4, None, [''], 'spell',
        [{'type': 'OnPlayAbility', 'name': 'OpponentActiveDestroyAbility', 'select_count': 1,
          'zone_cards': lambda x, y: [creature.set_index(i) for i, creature in enumerate(y.battle_zone) if not creature.is_tap]}],
        [''], 1
    ],
    [
        'dm01-094', 'ゴースト・タッチ', ['darkness'], 2, None,
        [''], 'spell', [{'type': 'OnPlayAbility', 'name': 'OpponentHandToGraveyardAbility'}], ['shieldTrigger'], 1
    ],
    [
        'dm01-106', '青銅の鎧', ['nature'], 3, 1000,
        [''], 'creature', [{'type': 'OnPlayAbility', 'name': 'SelfDeckToManaZoneAbility', 'fixed_count': 1}], [], 1
    ],
    [
        'dm01-109', 'アルティメット・フォース', ['nature'], 5, None,
        [''], 'spell', [{'type': 'OnPlayAbility', 'name': 'SelfDeckToManaZoneAbility', 'fixed_count': 2}], [], 1
    ]
]
