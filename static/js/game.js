/*
グローバル変数
*/

let game_state;
let ClickingTime;
let area1;
let area2;
let onSelectCardOk;
let onRandomSelectCard;

//やむをえず導入
let countAbilityTarget;

const url = new URL(window.location.href);
const params = url.searchParams;
const myNumber = params.get('player_id');

const socket = io({ auth: { 'id': myNumber } });

/*
DOMの取得
*/

const overlay = document.getElementById('overlay');

const menuPopup = document.getElementById('menu');
const fullscreenBtn = document.getElementById('fullscreen');
const gameLeaveBtn = document.getElementById('game-leave');
const menuCloseBtn = document.getElementById('menu-close');

const alertPopup = document.getElementById('alert');
const alertMessage = document.getElementById('alert-message');
const alertOkBtn = document.getElementById('alert-ok');
const alertCloseBtn = document.getElementById('alert-close');

const cardInfoPopup = document.getElementById('card-info');
const cardInfoCard = document.getElementById('card-info-card');
const cardInfoCloseBtn = document.getElementById('card-info-close');

const cardSelectPopup = document.getElementById('card-select');
const cardSelectMessage = document.getElementById('card-select-message');
const cardSelectCards = document.getElementById('card-select-cards');
const cardSelectOkBtn = document.getElementById('card-select-ok');
const cardSelectCloseBtn = document.getElementById('card-select-close');
const randomTapBtn = document.getElementById('random-tap');

const optionalPopup = document.getElementById('optional');
const optionalMessage = document.getElementById('optional-message');
const optionalNo = document.getElementById('no');
const optionalYes = document.getElementById('yes');

const countPopup = document.getElementById('count');
const countMessage = document.getElementById('count-message');
const countNumber = document.getElementById('count-number');
const countOk = document.getElementById('count-ok');

const menuButton = document.getElementById('menu-btn');
const turnEndButton = document.getElementById('turn-end-btn');

/*
イベントリスナーの登録
*/

// if (myNumber == '1') {
//     document.getElementById('playmat1').style.backgroundImage = 'url("/static/image/icon/わため.png")';
//     document.getElementById('playmat2').style.backgroundImage = 'url("/static/image/icon/わため.png")';
// } else {
//     document.getElementById('playmat1').style.backgroundImage = 'url("/static/image/icon/わため.png")';
//     document.getElementById('playmat2').style.backgroundImage = 'url("/static/image/icon/わため.png")';
// }

fullscreenBtn.addEventListener('click', () => {
    if (document.fullscreenElement) {
        document.exitFullscreen();
    } else {
        document.documentElement.requestFullscreen();
    }
});

gameLeaveBtn.addEventListener('click', () => {
    if (window.confirm('本当にゲームを抜けますか？')) {
        window.location.href = '/menu';
    }
});

menuButton.addEventListener('click', openMenu);
menuCloseBtn.addEventListener('click', closeMenu);

alertOkBtn.addEventListener('click', closeAlert);
alertCloseBtn.addEventListener('click', closeAlert);

cardInfoCloseBtn.addEventListener('click', closeCardInfo);
cardSelectCloseBtn.addEventListener('click', closeCardSelect);

optionalNo.addEventListener('click', executeOptionalAbility);
optionalYes.addEventListener('click', executeOptionalAbility);

countOk.addEventListener('click', executeCountAbility);

/*
ユーティリティ関数
*/

function openMenu() {
    overlay.style.display = 'block';
    menuPopup.style.display = 'flex';
}

function closeMenu() {
    overlay.style.display = 'none';
    menuPopup.style.display = 'none';
}

function openAlert(message) {
    overlay.style.display = 'block';
    alertPopup.style.display = 'flex';
    alertMessage.textContent = message;
}

function closeAlert() {
    overlay.style.display = 'none';
    alertPopup.style.display = 'none';
    alertMessage.textContent = null;
}

function openCardInfo(cardId) {
    overlay.style.display = 'block';
    cardInfoPopup.style.display = 'flex';
    cardInfoCard.src = '/static/image/cards/' + cardId + '.png';
}

function closeCardInfo() {
    document.getElementById('overlay').style.display = 'none';
    cardInfoPopup.style.display = 'none';
    cardInfoCard.src = null;
}

function openCardSelect(message, cards, checkMax, executeTarget, playCard) {
    overlay.style.display = 'block';
    cardSelectPopup.style.display = 'flex';
    cardSelectMessage.textContent = message;
    cardSelectCards.innerHTML = null;
    if (executeTarget == 'play-card-execute') {
        randomTapBtn.style.display = 'block';
    }

    for (let i = 0; i < cards.length; i++) {
        if (cards[i].id == 'shield') {
            cardSelectCards.innerHTML += `
                <input type="checkbox" id="targets${i}" name="targets" value="${cards[i].instance_id}" style="display: none;">
                <label class="clickable card" for="targets${i}">
                    <div class="shield-card"></div>
                </label>
            `;
        } else if (cards[i].is_tap) {
            const value = cards[i].instance_id;
            cardSelectCards.innerHTML += `
                <input type="checkbox" id="targets${i}" name="targets" value="${value}" style="display: none;">
                <label class="confused clickable card" for="targets${i}">
                    <img src="/static/image/cards/${cards[i].id}.png" class="card">
                    <img src="/static/image/icon/arrow.png" class="arrow">
                    <div class="card card-overlay"></div>
                </label>
            `;
        } else {
            if (cards[i].id != 'notCard') {
                const value = cards[i].instance_id;
                cardSelectCards.innerHTML += `
                    <input type="checkbox" id="targets${i}" name="targets" value="${value}" style="display: none;">
                    <label class="clickable card" for="targets${i}">
                        <img src="/static/image/cards/${cards[i].id}.png" class="card">
                    </label>
                `;
            }
        }
    }
    if (onSelectCardOk) {
        cardSelectOkBtn.removeEventListener('click', onSelectCardOk);
    }

    if (onRandomSelectCard) {
        randomTapBtn.removeEventListener('click', onRandomSelectCard);
    }

    onSelectCardOk = function () {
        execute(executeTarget, playCard);
    };
    cardSelectOkBtn.addEventListener('click', onSelectCardOk);

    onRandomSelectCard = function () {
        executeRandom(playCard);
    };
    randomTapBtn.addEventListener('click', onRandomSelectCard);

    if (checkMax > 0) {
        cardSelectOkBtn.style.display = 'block';
    } else {
        cardSelectOkBtn.style.display = 'none';
    }

    const checkBoxes = document.getElementsByName('targets');
    checkBoxes.forEach(checkBox => {
        checkBox.addEventListener('change', () => {
            checkCount(checkBox);
        })
    });

    function checkCount(target) {
        let checkCount = 0;
        checkBoxes.forEach(checkBox => {
            if (checkBox.checked) {
                checkCount++;
            }
        });
        if (checkCount > checkMax) {
            target.checked = false;
        }
    }
}

function closeCardSelect() {
    overlay.style.display = 'none';
    cardSelectPopup.style.display = 'none';
    cardSelectMessage.textContent = null;
    cardSelectCards.innerHTML = null;
    cardSelectOkBtn.onclick = null;
    randomTapBtn.style.display = 'none';
}

function openOptional(message) {
    overlay.style.display = 'block';
    optionalPopup.style.display = 'flex';
    optionalMessage.textContent = message;
}

function closeOptional() {
    overlay.style.display = 'none';
    optionalPopup.style.display = 'none';
    optionalMessage.textContent = null;
}

function openCount(message, select_count) {
    overlay.style.display = 'block';
    countPopup.style.display = 'flex';
    countNumber.max = select_count;
    countNumber.value = select_count;
    countMessage.textContent = message;
}

function closeCount() {
    overlay.style.display = 'none';
    countPopup.style.display = 'none';
    countNumber.max = null;
    countNumber.value = null;
    countMessage.textContent = null;
}

/*
サーバー通信
*/

socket.on('game-start', (data) => {
    area1 = new Area(3 - myNumber, 1);
    area2 = new Area(myNumber, 2);

    area1.manaZone.addEventListener('click', () => { checkZone(area1.playerId, 'mana_zone') });
    area2.manaZone.addEventListener('click', () => { checkZone(area2.playerId, 'mana_zone') });
    area1.graveyard.addEventListener('click', () => { checkZone(area1.playerId, 'graveyard') });
    area2.graveyard.addEventListener('click', () => { checkZone(area2.playerId, 'graveyard') });
    turnEndButton.addEventListener('click', endTurn);

    renderUI(data);
});

function rendering() {
    socket.emit('rendering');
}

socket.on('rendering', (data) => {
    renderUI(data);
});

function checkZone(playerNumber, zoneName) {
    const player = game_state[`player${playerNumber}`];
    const zoneMap = {
        'graveyard': '墓地',
        'mana_zone': 'マナゾーン'
    };
    openCardSelect(`${player.name}の${zoneMap[zoneName]}`, player[zoneName], 0, null, null);
}

function chargeMana(cardUuid) {
    socket.emit('charge-mana', {
        'card-uuid': cardUuid
    });
}

function playCardPrepare(cardUuid) {
    socket.emit('play-card-prepare', {
        'card-uuid': cardUuid
    });
}

socket.on('play-card-prepare', (data) => {
    const zoneCards = data.current_turn.active_player.mana_zone;
    const cost = data.cost;
    openCardSelect(`タップするマナを${cost}枚選んでください。`, zoneCards, cost, 'play-card-execute', null);
    renderUI(data);
});

socket.on('optional-ability', (data) => {
    const card_name = data.card_name;
    openOptional(`${card_name}の効果を使いますか？`);
    renderUI(data);
});

socket.on('count-ability', (data) => {
    const select_count = data.select_count;
    openCount(`0から${select_count}の数を選んでください。`, select_count);
    countAbilityTarget = 'count-ability';
    renderUI(data);
});

socket.on('select-ability', (data) => {
    cardSelectCloseBtn.style.display = 'none';
    const zoneCards = data.zone_cards;
    const select_count = data.select_count;
    const compulsion = data.compulsion ? '' : 'まで';
    openCardSelect(`${select_count}枚${compulsion}選んでください。`, zoneCards, select_count, 'select-ability', null);
    renderUI(data);
});

socket.on('count-ability-trigger', (data) => {
    const select_count = data.select_count;
    openCount(`0から${select_count}の数を選んでください。`, select_count);
    countAbilityTarget = 'count-ability-trigger';
    renderUI(data);
});

socket.on('select-ability-trigger', (data) => {
    const zoneCards = data.zone_cards;
    const select_count = data.select_count;
    const compulsion = data.compulsion ? '' : 'まで';
    openCardSelect(`${select_count}枚${compulsion}選んでください。`, zoneCards, select_count, 'select-ability-trigger', null);
    renderUI(data);
    cardSelectCloseBtn.style.display = 'none';
});

socket.on('play-ability-prepare', (data) => {
    const zoneCards = data.zone_cards;
    const checkMax = data.select_count;
    openCardSelect(`${checkMax}枚選んでください。`, zoneCards, checkMax, 'play-ability-execute', null);
    renderUI(data);
});

function attackPlayerPrepare(cardUuid) {
    socket.emit('attack-player-prepare', {
        'card-uuid': cardUuid
    });
}

socket.on('attack-player-prepare', (data) => {
    const zoneCards = [];
    data.current_turn.inactive_player.shield_zone.forEach(card => {
        card.id = 'shield';
        zoneCards.push(card);
    });
    const breakCount = data.break_count;
    const battleZoneIndex = data.battle_zone_index;
    openCardSelect(`ブレイクするシールドを${breakCount}枚選んでください。`, zoneCards, breakCount, 'attack-player-execute', battleZoneIndex);
    renderUI(data);
    cardSelectCloseBtn.style.display = 'none';
});

socket.on('block', (data) => {
    const zoneCards = [];
    const checkMax = 1;
    const blockers = data.blockers;
    const executeTarget = data.execute_target;
    data.current_turn.inactive_player.battle_zone.forEach((card, i) => {
        if (blockers.includes(i)) {
            zoneCards.push(card);
        } else {
            zoneCards.push({ 'id': 'notCard', 'is_tap': false });
        }
    });
    openCardSelect(`ブロックするクリーチャーを選んでください。`, zoneCards, checkMax, executeTarget, data.battle_zone_index);
    rendering();
    cardSelectCloseBtn.style.display = 'none';
});

function attackCreaturePrepare(battleZoneIndex) {
    socket.emit('attack-creature-prepare', {
        'battle-zone-index': battleZoneIndex
    });
}

socket.on('attack-creature-prepare', (data) => {
    const zoneCards = data.current_turn.inactive_player.battle_zone;
    const checkMax = 1;
    openCardSelect(`アタックするクリーチャーを選んでください。`, zoneCards, checkMax, 'attack-creature-execute', null);
    renderUI(data);
});

function execute(executeTarget, playCardUuid) {
    const selectCards = Array.from(document.querySelectorAll('input[name="targets"]:checked')).map(checkbox => checkbox.value);
    socket.emit(executeTarget, {
        'play-card-uuid': playCardUuid,
        'select-cards': selectCards
    });
    closeCardSelect();
    cardSelectCloseBtn.style.display = 'block';
}

function executeRandom(playCardUuid) {
    socket.emit('execute-random', {
        'play-card-uuid': playCardUuid
    });
    closeCardSelect();
    cardSelectCloseBtn.style.display = 'block';
}

function executeOptionalAbility() {    
    socket.emit('optional-ability', {
        'option': this.value == 'yes' ? true : false
    });
    closeOptional();
}

function executeCountAbility() {
    socket.emit(countAbilityTarget, {
        'count': countNumber.value
    });
    closeCount();
}

socket.on('play-shield-triggers-prepare', (data) => {
    const zoneCards = [];
    const checkMax = data.shield_triggers.length;
    const shieldTriggers = data.shield_triggers;
    data.current_turn.inactive_player.hand.forEach((card, i) => {
        if (shieldTriggers.includes(i)) {
            zoneCards.push(card);
        } else {
            zoneCards.push({ 'id': 'notCard', 'is_tap': false });
        }
    });
    openCardSelect(`実行するシールドトリガーを選んでください。`, zoneCards, checkMax, 'play-shield-triggers-execute', null);
    rendering();
    cardSelectCloseBtn.style.display = 'none';
});

function endTurn() {
    socket.emit('end-turn');
}

socket.on('end-game', (data) => {
    alertCloseBtn.style.display = 'block';
    alertOkBtn.style.display = 'block';
    openAlert(data.winner + 'の勝ちです。');
    renderUI(data);
});

socket.on('alert', (data) => {
    alertCloseBtn.style.display = 'block';
    alertOkBtn.style.display = 'block';
    openAlert(data.alert);
    renderUI(data);
});

socket.on('strong-alert', (data) => {
    alertCloseBtn.style.display = 'none';
    alertOkBtn.style.display = 'none';
    openAlert(data.alert);
    renderUI(data);
});

socket.on('strong-alert-close', (data) => {
    closeAlert();
    renderUI(data);
});

/*
UIレンダリング関数
*/

function renderUI(gameState) {
    game_state = gameState;
    area1.renderBattleZone(gameState[`player${area1.playerId}`], gameState.current_turn.active_player.number);
    area2.renderBattleZone(gameState[`player${area2.playerId}`], gameState.current_turn.active_player.number);
    area1.renderShieldZone(gameState[`player${area1.playerId}`]);
    area2.renderShieldZone(gameState[`player${area2.playerId}`]);
    area1.renderDeck(gameState[`player${area1.playerId}`]);
    area2.renderDeck(gameState[`player${area2.playerId}`]);
    area1.renderManaZone(gameState[`player${area1.playerId}`]);
    area2.renderManaZone(gameState[`player${area2.playerId}`]);
    area1.renderGraveyard(gameState[`player${area1.playerId}`]);
    area2.renderGraveyard(gameState[`player${area2.playerId}`]);
    area1.renderHand(gameState[`player${area1.playerId}`], gameState.current_turn.active_player.number);
    area2.renderHand(gameState[`player${area2.playerId}`], gameState.current_turn.active_player.number);

    if (myNumber == gameState.current_turn.active_player.number) {
        turnEndButton.disabled = false;
    } else {
        turnEndButton.disabled = true;
    }

    if (gameState.winner) {
        openAlert(gameState.winner + 'の勝ち！');
    }
}

/*
エリアクラス定義
*/

class Area {
    constructor(playerId, areaId) {
        this.playerId = playerId;
        this.opponentId = 3 - playerId;
        this.areaId = areaId;
        this.opponentAreaId = 3 - areaId;
        this.battleZone = document.getElementById('battle-zone' + areaId);
        this.shieldZone = document.getElementById('shield-zone' + areaId);
        this.deck = document.getElementById('deck' + areaId);
        this.deckCount = document.getElementById('deck-count' + areaId);
        this.graveyard = document.getElementById('graveyard' + areaId);
        this.graveyardCount = document.getElementById('graveyard-count' + areaId);
        this.manaZone = document.getElementById('mana-zone' + areaId);
        this.manaZoneCount = document.getElementById('mana-zone-count' + areaId);
        this.availableManaCount = document.getElementById('available-mana-count' + areaId);
        this.hand = document.getElementById('hand' + areaId);
        this.playMat = document.getElementById('player' + areaId);
    }

    renderBattleZone(playerData, activePlayerNumber) {
        if (activePlayerNumber == this.playerId) {
            document.getElementById('area' + this.areaId).classList.add('active-player');
        } else {
            document.getElementById('area' + this.areaId).classList.remove('active-player');
        }
        this.battleZone.innerHTML = null;
        if (playerData.battle_zone.length > 0) {
            const zoneWidth = parseFloat(window.getComputedStyle(this.battleZone).width);
            const zoneGap = parseFloat(window.getComputedStyle(this.battleZone).gap);

            for (let i = 0; i < playerData.battle_zone.length; i++) {
                let addText;
                const onclickText = (this.playerId != myNumber || activePlayerNumber != myNumber) ? `onclick="openCardInfo('${playerData.battle_zone[i].id}')"` : '';
                addText = `
                    <div class="battle-zone-wrapper">
                        <div class="confused clickable" data-player="${this.playerNumber}" ${onclickText}
                        data-zone="battle-zone" data-uuid="${playerData.battle_zone[i].instance_id}" data-cardid="${playerData.battle_zone[i].id}">
                            <img src="/static/image/cards/${playerData.battle_zone[i].id}.png" class="card">`;
                if (playerData.battle_zone[i].is_tap) {
                    addText += `
                        <img src="/static/image/icon/arrow.png" class="arrow">
                        <div class="card card-overlay"></div>`;
                }
                if (playerData.battle_zone[i].is_summoning_sickness) {
                    addText += `
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 110 110" class="line line1">
                            <circle cx="55" cy="55" r="50" class="" />
                        </svg>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 110 110" class="line line2">
                            <circle cx="55" cy="55" r="50" class="" />
                        </svg>
                        <div class="orbit">
                            <img src="/static/image/icon/star.png" class="star star1" alt="星">
                            <img src="/static/image/icon/star.png" class="star star2" alt="星">
                        </div>`;
                }

                addText += `
                        </div>
                    </div>`;

                this.battleZone.innerHTML += addText;
            }

            if (this.playerId == myNumber && myNumber == activePlayerNumber) {
                const images = this.battleZone.querySelectorAll('.confused');
                images.forEach(img => {
                    let offsetX, offsetY;
                    let isDragging = false;

                    const pointerDown = (e) => {
                        ClickingTime = new Date().getTime();
                        isDragging = true;
                        offsetX = e.type.startsWith('touch') ? e.touches[0].clientX - img.getBoundingClientRect().left : e.offsetX;
                        offsetY = e.type.startsWith('touch') ? e.touches[0].clientY - img.getBoundingClientRect().top : e.offsetY;
                    };

                    const pointerMove = (e) => {
                        if (!isDragging) return;
                        const clientX = e.type.startsWith('touch') ? e.touches[0].clientX : e.clientX;
                        const clientY = e.type.startsWith('touch') ? e.touches[0].clientY : e.clientY;

                        const containerRect = img.parentNode.getBoundingClientRect();
                        let x = clientX - containerRect.left - offsetX;
                        let y = clientY - containerRect.top - offsetY;
                        img.style.left = x + 'px';
                        img.style.top = y + 'px';
                        img.style.zIndex = 1;

                        const imgRect = img.getBoundingClientRect();
                        const battleZoneRect = document.getElementById('battle-zone' + this.opponentAreaId).getBoundingClientRect();
                        const shieldZoneRect = document.getElementById('shield-zone' + this.opponentAreaId).getBoundingClientRect();

                        const battleZoneOverlapX = Math.max(0, Math.min(imgRect.right, battleZoneRect.right) - Math.max(imgRect.left, battleZoneRect.left));
                        const battleZoneOverlapY = Math.max(0, Math.min(imgRect.bottom, battleZoneRect.bottom) - Math.max(imgRect.top, battleZoneRect.top));
                        const battleZoneArea = battleZoneOverlapX * battleZoneOverlapY;

                        const shieldZoneOverlapX = Math.max(0, Math.min(imgRect.right, shieldZoneRect.right) - Math.max(imgRect.left, shieldZoneRect.left));
                        const shieldZoneOverlapY = Math.max(0, Math.min(imgRect.bottom, shieldZoneRect.bottom) - Math.max(imgRect.top, shieldZoneRect.top));
                        const shieldZoneArea = shieldZoneOverlapX * shieldZoneOverlapY;

                        document.getElementById('battle-zone' + this.opponentAreaId).style.backgroundColor = null;
                        document.getElementById('shield-zone' + this.opponentAreaId).style.backgroundColor = null;

                        if (battleZoneArea > 0 || shieldZoneArea > 0) {
                            if (battleZoneArea >= shieldZoneArea) {
                                document.getElementById('battle-zone' + this.opponentAreaId).style.backgroundColor = 'rgba(55, 65, 81, 0.7)';
                            } else {
                                document.getElementById('shield-zone' + this.opponentAreaId).style.backgroundColor = 'rgba(55, 65, 81, 0.7)';
                            }
                        }
                    };

                    const pointerUp = (e) => {
                        if (!isDragging) return;
                        isDragging = false;
                        const imgRect = img.getBoundingClientRect();
                        const battleZoneRect = document.getElementById('battle-zone' + this.opponentAreaId).getBoundingClientRect();
                        const shieldZoneRect = document.getElementById('shield-zone' + this.opponentAreaId).getBoundingClientRect();

                        const battleZoneOverlapX = Math.max(0, Math.min(imgRect.right, battleZoneRect.right) - Math.max(imgRect.left, battleZoneRect.left));
                        const battleZoneOverlapY = Math.max(0, Math.min(imgRect.bottom, battleZoneRect.bottom) - Math.max(imgRect.top, battleZoneRect.top));
                        const battleZoneArea = battleZoneOverlapX * battleZoneOverlapY;

                        const shieldZoneOverlapX = Math.max(0, Math.min(imgRect.right, shieldZoneRect.right) - Math.max(imgRect.left, shieldZoneRect.left));
                        const shieldZoneOverlapY = Math.max(0, Math.min(imgRect.bottom, shieldZoneRect.bottom) - Math.max(imgRect.top, shieldZoneRect.top));
                        const shieldZoneArea = shieldZoneOverlapX * shieldZoneOverlapY;

                        document.getElementById('battle-zone' + this.opponentAreaId).style.backgroundColor = null;
                        document.getElementById('shield-zone' + this.opponentAreaId).style.backgroundColor = null;

                        if (battleZoneArea > 0 || shieldZoneArea > 0) {
                            if (battleZoneArea >= shieldZoneArea) {
                                attackCreaturePrepare(img.dataset.uuid);
                            } else {
                                attackPlayerPrepare(img.dataset.uuid);
                            }
                        } else {
                            img.style.left = '0px';
                            img.style.top = '0px';
                            img.style.zIndex = null;
                            if (new Date().getTime() - ClickingTime < 300) {
                                openCardInfo(img.dataset.cardid);
                            }
                        }
                    };

                    img.addEventListener('mousedown', pointerDown);
                    img.addEventListener('touchstart', pointerDown);
                    document.addEventListener('mousemove', pointerMove);
                    document.addEventListener('touchmove', pointerMove);
                    document.addEventListener('mouseup', pointerUp);
                    document.addEventListener('touchend', pointerUp);
                });
            }
            adjustImageOverlap(this.battleZone.querySelectorAll('.battle-zone-wrapper'), zoneWidth, zoneGap);
        }
    }

    renderShieldZone(playerData) {
        this.shieldZone.innerHTML = null;
        if (playerData.shield_zone.length > 0) {
            const zoneWidth = parseFloat(window.getComputedStyle(this.shieldZone).width);
            const zoneGap = parseFloat(window.getComputedStyle(this.shieldZone).gap);
            for (let i = 0; i < playerData.shield_zone.length; i++) {
                this.shieldZone.innerHTML += '<div class="shield-card"></div>';
            }
            adjustImageOverlap(this.shieldZone.querySelectorAll('.shield-card'), zoneWidth, zoneGap);
        }
    }

    renderDeck(playerData) {
        this.deckCount.textContent = playerData.deck.length;
    }

    renderManaZone(playerData) {
        this.manaZoneCount.textContent = playerData.mana_zone.length;
        this.availableManaCount.textContent = playerData.available_mana;
    }

    renderGraveyard(playerData) {
        this.graveyardCount.innerHTML = playerData.graveyard.length;
    }

    renderHand(playerData, activePlayerNumber) {
        this.hand.innerHTML = null;
        if (playerData.hand.length > 0) {
            const zoneWidth = parseFloat(window.getComputedStyle(this.hand).width);
            const zoneGap = parseFloat(window.getComputedStyle(this.hand).gap);
            for (let i = 0; i < playerData.hand.length; i++) {
                if (myNumber == playerData.number) {
                    const onclickText = myNumber != activePlayerNumber ? `onclick="openCardInfo('${playerData.hand[i].id}')"` : '';
                    this.hand.innerHTML += `
                        <div class="hand-wrapper">
                            <img src="/static/image/cards/${playerData.hand[i].id}.png" class="card clickable" ${onclickText}
                            data-player="${this.playerNumber}" data-zone="hand" data-uuid="${playerData.hand[i].instance_id}" data-cardid="${playerData.hand[i].id}">
                        </div>`;
                } else {
                    this.hand.innerHTML += `
                        <div class="hand-wrapper">
                            <img src="/static/image/cards/card.png" class="card">
                        </div>`;
                }
            }

            if (this.playerId == myNumber && myNumber == activePlayerNumber) {
                const images = this.hand.querySelectorAll('img');
                images.forEach(img => {
                    let offsetX, offsetY;
                    let isDragging = false;

                    const pointerDown = (e) => {
                        ClickingTime = new Date().getTime();
                        isDragging = true;
                        offsetX = e.type.startsWith('touch') ? e.touches[0].clientX - img.getBoundingClientRect().left : e.offsetX;
                        offsetY = e.type.startsWith('touch') ? e.touches[0].clientY - img.getBoundingClientRect().top : e.offsetY;
                    };

                    const pointerMove = (e) => {
                        if (!isDragging) return;
                        const clientX = e.type.startsWith('touch') ? e.touches[0].clientX : e.clientX;
                        const clientY = e.type.startsWith('touch') ? e.touches[0].clientY : e.clientY;

                        const containerRect = img.parentNode.getBoundingClientRect();
                        let x = clientX - containerRect.left - offsetX;
                        let y = clientY - containerRect.top - offsetY;
                        img.style.left = x + 'px';
                        img.style.top = y + 'px';

                        const imgRect = img.getBoundingClientRect();
                        const manaRect = this.manaZone.getBoundingClientRect();
                        const battleZoneRect = this.battleZone.getBoundingClientRect();

                        const manaOverlapX = Math.max(0, Math.min(imgRect.right, manaRect.right) - Math.max(imgRect.left, manaRect.left));
                        const manaOverlapY = Math.max(0, Math.min(imgRect.bottom, manaRect.bottom) - Math.max(imgRect.top, manaRect.top));
                        const manaArea = manaOverlapX * manaOverlapY;

                        const battleZoneOverlapX = Math.max(0, Math.min(imgRect.right, battleZoneRect.right) - Math.max(imgRect.left, battleZoneRect.left));
                        const battleZoneOverlapY = Math.max(0, Math.min(imgRect.bottom, battleZoneRect.bottom) - Math.max(imgRect.top, battleZoneRect.top));
                        const battleZoneArea = battleZoneOverlapX * battleZoneOverlapY;

                        this.manaZone.style.backgroundColor = null;
                        this.battleZone.style.backgroundColor = null;

                        if (manaArea > 0 || battleZoneArea > 0) {
                            if (manaArea >= battleZoneArea) {
                                this.manaZone.style.backgroundColor = 'rgba(55, 65, 81, 0.7)';
                            } else {
                                this.battleZone.style.backgroundColor = 'rgba(55, 65, 81, 0.7)';
                            }
                        }
                    };

                    const pointerUp = (e) => {
                        if (!isDragging) return;
                        isDragging = false;

                        const imgRect = img.getBoundingClientRect();
                        const manaRect = this.manaZone.getBoundingClientRect();
                        const battleZoneRect = this.battleZone.getBoundingClientRect();

                        const manaOverlapX = Math.max(0, Math.min(imgRect.right, manaRect.right) - Math.max(imgRect.left, manaRect.left));
                        const manaOverlapY = Math.max(0, Math.min(imgRect.bottom, manaRect.bottom) - Math.max(imgRect.top, manaRect.top));
                        const manaArea = manaOverlapX * manaOverlapY;

                        const battleZoneOverlapX = Math.max(0, Math.min(imgRect.right, battleZoneRect.right) - Math.max(imgRect.left, battleZoneRect.left));
                        const battleZoneOverlapY = Math.max(0, Math.min(imgRect.bottom, battleZoneRect.bottom) - Math.max(imgRect.top, battleZoneRect.top));
                        const battleZoneArea = battleZoneOverlapX * battleZoneOverlapY;

                        if (manaArea > 0 || battleZoneArea > 0) {
                            this.manaZone.style.backgroundColor = null;
                            this.battleZone.style.backgroundColor = null;
                            if (manaArea >= battleZoneArea) {
                                chargeMana(img.dataset.uuid);
                            } else {
                                playCardPrepare(img.dataset.uuid);
                            }
                        } else {
                            img.style.left = '0px';
                            img.style.top = '0px';
                            if (new Date().getTime() - ClickingTime < 300) {
                                openCardInfo(img.dataset.cardid);
                            }
                        }
                    };

                    img.addEventListener('mousedown', pointerDown);
                    img.addEventListener('touchstart', pointerDown);
                    document.addEventListener('mousemove', pointerMove);
                    document.addEventListener('touchmove', pointerMove);
                    document.addEventListener('mouseup', pointerUp);
                    document.addEventListener('touchend', pointerUp);
                });
            }
            adjustImageOverlap(this.hand.querySelectorAll('.hand-wrapper'), zoneWidth, zoneGap);
        }
    }
}

/*
ヘルパー関数
*/

function adjustImageOverlap(cards, zoneWidth, zoneGap) {
    const cardWidth = parseFloat(window.getComputedStyle(cards[0]).width);
    const totalCardsWidth = (cardWidth + zoneGap) * cards.length - zoneGap;

    if (zoneWidth < totalCardsWidth) {
        const hoge = (totalCardsWidth - zoneWidth) / (cards.length - 1);

        cards.forEach((card, index) => {
            if (index != 0) {
                card.style.marginLeft = `-${hoge}px`;
            }
        });
    }
}
