const playerNameInput = document.getElementById('player-name');
const gameStartBtn = document.getElementById('game-join');
gameStartBtn.addEventListener('click', async () => {
    const playerName = playerNameInput.value;
    if (!playerName) {
        alert('プレイヤー名を入力してください。');
        return;
    }

    const formData = new FormData();
    formData.append('player-name', playerName);
    const response = await fetch('/join-game', { method: 'POST', body: formData });
    const data = await response.json();
    if (data.alert) {
        alert(data.alert);
    } else {
        window.location.href = `/game?player_id=${data.player_id}`;
    }
});
