const select = document.getElementById('deck-select-back');
select.style.backgroundImage = `url("/static/image/cards/${select.dataset.id}.png")`;
if (select.dataset.type == 'creature') {
    select.style.backgroundPosition = '74.5% 35%';
    select.style.backgroundSize = '125.5%';
} else if (select.dataset.type == 'spell') {
    select.style.backgroundPosition = '52% 40.5%';
    select.style.backgroundSize = '135%';
}

for (let i = 1; i <= 3; i++) {
    const compose = document.getElementById('compose-' + i);
    compose.style.backgroundImage = `url("/static/image/cards/${compose.dataset.id}.png")`;
}

const gameStartBtn = document.getElementById('game-start');
gameStartBtn.addEventListener('click', async () => {
    const response = await fetch('/join-game', { method: 'POST' });
    const data = await response.json();
    if (data.alert) {
        alert(data.alert);
    } else {
        window.location.href = `/game?player_id=${data.player_id}`;
    }
});
