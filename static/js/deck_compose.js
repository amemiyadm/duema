const decks = document.getElementById('decks');

decks.addEventListener('click', async (e) => {
    if (e.target.classList.contains('btn-confirm')) {
        const deckId = e.target.dataset.id;

        const formData = new FormData();
        formData.append('deck-id', deckId);

        const response = await fetch('/confirm-deck', { method: 'POST', body: formData });
        const data = await response.json();
        if (data.error) {
            alert(data.error);
        } else {
            openDeckConfirm(data.deck);
        }
    }
});

document.querySelectorAll('.key-card').forEach(keyCard => {
    keyCard.style.backgroundImage = `url('/static/image/cards/${keyCard.dataset.key}.png')`;
});

const overlay = document.getElementById('overlay');
const menu = document.getElementById('menu');
const closeButotn = document.getElementById('menu-close');

closeButotn.addEventListener('click', closeDeckConfirm);

function openDeckConfirm(deck) {
    overlay.style.display = 'block';
    menu.style.display = 'flex';

    const cards = deck.cards;
    cards.forEach(card => {
        document.getElementById('deck-cards').innerHTML += `<img src="/static/image/cards/${card}.png" class="card">`;
    });
}

function closeDeckConfirm() {
    overlay.style.display = 'none';
    menu.style.display = 'none';
    document.getElementById('deck-cards').innerHTML = null;
}
