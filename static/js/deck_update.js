const decknameInput = document.getElementById('deckname');
const overlay = document.getElementById('overlay');
const menu = document.getElementById('menu');
const menuOkBtn = document.getElementById('menu-ok');
const closeButotn = document.getElementById('menu-close');
menuOkBtn.addEventListener('click', async () => {
    const cards = [];
    document.getElementById('deck-cards').querySelectorAll('img').forEach(img => {
        cards.push(img.dataset.id);
    });

    const deckname = decknameInput.value;
    const deckId = document.getElementById('deck-id').value;
    const formData = new FormData();
    formData.append('cards', cards);
    formData.append('deckname', deckname);
    formData.append('deck-id', deckId);

    const response = await fetch('/save-deck', { method: 'POST', body: formData });
    const data = await response.json();
    if (data.error) {
        alert(data.error);
    } else if (data.redirect_url) {
        window.location.href = data.redirect_url;
    }
});

const deckSaveBtn = document.getElementById('deck-save');
deckSaveBtn.addEventListener('click', openDeckConfirm);

closeButotn.addEventListener('click', closeDeckConfirm);
function closeDeckConfirm() {
    overlay.style.display = 'none';
    menu.style.display = 'none';
}

function openDeckConfirm() {
    overlay.style.display = 'block';
    menu.style.display = 'flex';

    const cards = deck.cards;
    cards.forEach(card => {
        document.getElementById('deck-cards').innerHTML += `<img src="/static/image/cards/${card}.png" class="card">`;
    });
}

const AllCardsImages = document.getElementById('all-cards').querySelectorAll('img');
AllCardsImages.forEach(img => {
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
        const deckRect = document.getElementById('deck-hoge').getBoundingClientRect();

        const deckOverlapX = Math.max(0, Math.min(imgRect.right, deckRect.right) - Math.max(imgRect.left, deckRect.left));
        const deckOverlapY = Math.max(0, Math.min(imgRect.bottom, deckRect.bottom) - Math.max(imgRect.top, deckRect.top));
        const deckArea = deckOverlapX * deckOverlapY;

        document.getElementById('deck-hoge').style.backgroundColor = null;

        if (deckArea) {
            document.getElementById('deck-hoge').style.backgroundColor = 'rgba(55, 65, 81, 0.7)';
        }
    };

    const pointerUp = (e) => {
        if (!isDragging) return;
        isDragging = false;

        const imgRect = img.getBoundingClientRect();
        const deckRect = document.getElementById('deck-hoge').getBoundingClientRect();

        const deckOverlapX = Math.max(0, Math.min(imgRect.right, deckRect.right) - Math.max(imgRect.left, deckRect.left));
        const deckOverlapY = Math.max(0, Math.min(imgRect.bottom, deckRect.bottom) - Math.max(imgRect.top, deckRect.top));
        const deckArea = deckOverlapX * deckOverlapY;

        if (deckArea > 0) {
            document.getElementById('deck-hoge').style.backgroundColor = null;
            const wrapper = document.createElement('div');
            const copyImg = img.cloneNode(true);
            wrapper.classList.add('card-wrapper');
            copyImg.style.left = null;
            copyImg.style.top = null;
            wrapper.appendChild(copyImg);
            document.getElementById('deck-cards').appendChild(wrapper);
            deckAppendEvent(copyImg);
        }

        img.style.left = '0px';
        img.style.top = '0px';
    };

    img.addEventListener('mousedown', pointerDown);
    img.addEventListener('touchstart', pointerDown);
    document.addEventListener('mousemove', pointerMove);
    document.addEventListener('touchmove', pointerMove);
    document.addEventListener('mouseup', pointerUp);
    document.addEventListener('touchend', pointerUp);
});

document.getElementById('deck-cards').querySelectorAll('img').forEach(img => {
    deckAppendEvent(img);
});

function deckAppendEvent(img) {
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
        const deckRect = document.getElementById('hoge').getBoundingClientRect();

        const deckOverlapX = Math.max(0, Math.min(imgRect.right, deckRect.right) - Math.max(imgRect.left, deckRect.left));
        const deckOverlapY = Math.max(0, Math.min(imgRect.bottom, deckRect.bottom) - Math.max(imgRect.top, deckRect.top));
        const deckArea = deckOverlapX * deckOverlapY;

        document.getElementById('hoge').style.backgroundColor = null;

        if (deckArea) {
            document.getElementById('hoge').style.backgroundColor = 'rgba(55, 65, 81, 0.7)';
        }
    };

    const pointerUp = (e) => {
        if (!isDragging) return;
        isDragging = false;

        const imgRect = img.getBoundingClientRect();
        const deckRect = document.getElementById('hoge').getBoundingClientRect();

        const deckOverlapX = Math.max(0, Math.min(imgRect.right, deckRect.right) - Math.max(imgRect.left, deckRect.left));
        const deckOverlapY = Math.max(0, Math.min(imgRect.bottom, deckRect.bottom) - Math.max(imgRect.top, deckRect.top));
        const deckArea = deckOverlapX * deckOverlapY;

        if (deckArea > 0) {
            document.getElementById('hoge').style.backgroundColor = null;
            document.getElementById('deck-cards').removeChild(img.parentNode);
        }

        img.style.left = '0px';
        img.style.top = '0px';
    };

    img.addEventListener('mousedown', pointerDown);
    img.addEventListener('touchstart', pointerDown);
    document.addEventListener('mousemove', pointerMove);
    document.addEventListener('touchmove', pointerMove);
    document.addEventListener('mouseup', pointerUp);
    document.addEventListener('touchend', pointerUp);
}