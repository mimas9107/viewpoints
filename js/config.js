/**
 * 配置管理模組
 */
export async function fetchConfig() {
    try {
        const response = await fetch('./viewpoints.json');
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error('無法載入組態檔:', error);
        alert('無法載入組態檔 viewpoints.json，請確保檔案存在。');
        return null;
    }
}
