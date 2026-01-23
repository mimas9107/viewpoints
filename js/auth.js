/**
 * Viewpoints 前端認證模組
 */

const TOKEN_KEY = 'viewpoints_token';
const USERNAME_KEY = 'viewpoints_username';

export function saveToken(token, username) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USERNAME_KEY, username);
}

export function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

export function getUsername() {
    return localStorage.getItem(USERNAME_KEY);
}

export function logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USERNAME_KEY);
    window.location.href = 'login.html';
}

export function isAuthenticated() {
    return !!getToken();
}

/**
 * 檢查是否已登入，若未登入則導向登入頁
 */
export function checkAuth() {
    if (!isAuthenticated() && !window.location.pathname.endsWith('login.html')) {
        window.location.href = 'login.html';
    }
}

/**
 * 封裝 fetch，自動加入 Authorization Header 並處理 401 錯誤
 */
export async function fetchWithAuth(url, options = {}) {
    const token = getToken();
    const headers = {
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, { ...options, headers });

    if (response.status === 401) {
        console.warn('認證失效，重新導向至登入頁');
        logout();
        throw new Error('Unauthorized');
    }

    return response;
}

export async function login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || '登入失敗');
    }

    const data = await response.json();
    saveToken(data.access_token, data.username);
    return data;
}

export async function register(username, password) {
    const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || '註冊失敗');
    }

    return await response.json();
}
