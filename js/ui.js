/**
 * UI 互動與全螢幕模組
 */
export function setupUI(config) {
    // 更新頁面標題
    document.title = config.title || '我的監視器牆';
    document.getElementById('pageTitle').textContent = config.title || '我的監視器牆';

    // 設定網格佈局
    const grid = document.getElementById('cameraGrid');
    grid.className = `camera-grid grid-${config.layout.columns}x${config.layout.rows}`;
}

export function setupFullscreen() {
    const overlay = document.getElementById('fullscreenOverlay');
    const img = document.getElementById('fullscreenImage');
    const closeBtn = document.getElementById('closeFullscreen');

    const close = () => overlay.classList.remove('active');

    closeBtn.onclick = close;
    overlay.onclick = (e) => {
        if (e.target.id === 'fullscreenOverlay') close();
    };

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') close();
    });

    return (src, alt) => {
        img.src = src;
        img.alt = alt;
        overlay.classList.add('active');
    };
}

export function updateRefreshStatus(enabled, interval) {
    const statusEl = document.getElementById('autoRefreshStatus');
    const btnEl = document.getElementById('toggleAutoRefresh');
    
    if (enabled) {
        statusEl.textContent = `自動重新整理: 開啟 (${interval}秒)`;
        statusEl.classList.add('live');
        btnEl.textContent = '停止自動重新整理';
        btnEl.classList.add('active');
    } else {
        statusEl.textContent = '自動重新整理: 關閉';
        statusEl.classList.remove('live');
        btnEl.textContent = '啟用自動重新整理';
        btnEl.classList.remove('active');
    }
}
