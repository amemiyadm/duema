const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');

registerBtn.addEventListener('click', () => registerOrLogin('/register-user'));
loginBtn.addEventListener('click', () => registerOrLogin('/login'));

async function registerOrLogin(action) {
    const username = usernameInput.value;
    const password = passwordInput.value;

    if (!username || !password) {
        alert('ユーザー名とパスワードを入力してください。');
        return;
    }

    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    try {
        const response = await fetch(action, { method: 'POST', body: formData });

        if (!response.ok) {
            alert(`エラーが発生しました: ${response.statusText}`);
            return;
        }

        const data = await response.json();
        if (data.error) {
            alert(data.error);
        } else if (data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    } catch (error) {
        alert('サーバーに接続できませんでした。ネットワーク接続を確認してください。');
    }
}
