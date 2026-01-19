/**
 * 圖片載入模組 (具備完整性檢查與自動重試)
 */
export function loadImage(img, index, retryCount = 0) {
    const container = img.closest('.camera-image-container');
    const loading = container.querySelector('.loading');
    const lastUpdateEl = document.getElementById(`lastUpdate${index}`);
    
    // 加入時間戳記以避免快取
    const timestamp = new Date().getTime();
    const baseUrl = img.dataset.src;
    const imageUrl = baseUrl + (baseUrl.includes('?') ? '&' : '?') + 't=' + timestamp;
    
    const tempImg = new Image();
    
    tempImg.onload = () => {
        // 檢查圖片完整性
        if (tempImg.naturalWidth > 0 && tempImg.naturalHeight > 0) {
            img.src = tempImg.src;
            img.style.display = 'block';
            if (loading) loading.style.display = 'none';
            
            // 更新時間戳記
            if (lastUpdateEl) {
                const now = new Date();
                lastUpdateEl.textContent = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
            }
        } else {
            handleImageError(img, index, retryCount, "圖片損毀");
        }
    };

    tempImg.onerror = () => {
        handleImageError(img, index, retryCount, "載入失敗");
    };

    tempImg.src = imageUrl;
}

function handleImageError(img, index, retryCount, reason) {
    if (retryCount < 3) {
        console.warn(`圖片載入異常 (${reason})，正在進行第 ${retryCount + 1} 次重試...`);
        setTimeout(() => {
            loadImage(img, index, retryCount + 1);
        }, 500);
    } else {
        const container = img.closest('.camera-image-container');
        const loading = container.querySelector('.loading');
        if (loading) {
            loading.innerHTML = `<div class="error">載入失敗<br>點擊重新整理重試</div>`;
            loading.style.cursor = 'pointer';
            loading.onclick = () => loadImage(img, index, 0);
        }
    }
}

export function loadAllImages() {
    const images = document.querySelectorAll('.camera-image');
    images.forEach((img, index) => {
        loadImage(img, index);
    });
}
