import { fetchWithAuth, checkAuth } from './auth.js';

/**
 * 配置管理模組
 * 優先順序：
 * 1. URL 參數 ?configUrl=... (外部 URL)
 * 2. API 端點 /api/config (start-server-fastapi.py)
 * 3. 本地檔案 ./viewpoints.json (fallback)
 */
const CONFIG_API = '/api/config';

export async function fetchConfig() {
    const urlParams = new URLSearchParams(window.location.search);
    const externalConfigUrl = urlParams.get('configUrl');

    if (externalConfigUrl) {
        console.log('[Config] 使用外部 URL 載入配置:', externalConfigUrl);
        return await fetchExternalConfig(externalConfigUrl);
    }

    try {
        // 檢查認證狀態（除了載入外部配置外）
        checkAuth();

        const apiResponse = await fetchWithAuth(CONFIG_API);
        if (apiResponse.ok) {
            console.log('[Config] 使用 API 端點載入配置');
            return await apiResponse.json();
        }
    } catch (apiError) {
        if (apiError.message === 'Unauthorized') return null;
        console.log('[Config] API 不可用，嘗試本地檔案');
    }

    console.log('[Config] 使用本地檔案載入配置');
    return await fetchLocalConfig();
}

async function fetchExternalConfig(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error('無法載入外部配置:', error);
        alert(`無法載入外部配置: ${url}`);
        return null;
    }
}

async function fetchLocalConfig() {
    try {
        const response = await fetch('./viewpoints.json');
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error('無法載入本地配置:', error);
        alert('無法載入組態檔 viewpoints.json，請確保檔案存在。');
        return null;
    }
}

export { CONFIG_API };
