/**
 * 主程式邏輯
 */
import { fetchConfig } from './config.js';
import { setupUI, setupFullscreen, updateRefreshStatus } from './ui.js';
import { loadAllImages, loadImage } from './image-loader.js';
import { initHlsPlayers } from './player.js';

let config = null;
let autoRefreshInterval = null;
let autoRefreshEnabled = false;
let showFullscreen = null;

async function init() {
    config = await fetchConfig();
    if (!config) return;

    // 1. 初始化介面
    setupUI(config);
    showFullscreen = setupFullscreen();

    // 2. 渲染監視器
    renderCameras();

    // 3. 設定事件監聽
    setupEventListeners();

    // 4. 設定自動重新整理
    if (config.autoRefresh) {
        toggleAutoRefresh();
    }
}

function renderCameras() {
    const grid = document.getElementById('cameraGrid');
    grid.innerHTML = '';
    
    config.cameras.forEach((camera, index) => {
        const cameraItem = document.createElement('div');
        cameraItem.className = 'camera-item';
        
        const isYoutube = camera.type === 'youtube';
        const isHls = camera.type === 'hls';
        
        if (isYoutube) {
            cameraItem.innerHTML = `
                <div class="camera-header">
                    <div class="camera-name">${camera.name}</div>
                    <div class="camera-info">
                        <span class="camera-location">${camera.location || ''}</span>
                        <span class="camera-category">${camera.category || ''}</span>
                    </div>
                </div>
                <div class="camera-image-container">
                    <div class="youtube-badge">LIVE</div>
                    <iframe class="camera-iframe"
                        src="https://www.youtube-nocookie.com/embed/${camera.youtubeId}?mute=1&autoplay=1&playsinline=1&rel=0&modestbranding=1&controls=1"
                        title="${camera.name}"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen
                        loading="lazy">
                    </iframe>
                </div>
            `;
        } else if (isHls) {
            cameraItem.innerHTML = `
                <div class="camera-header">
                    <div class="camera-name">${camera.name}</div>
                    <div class="camera-info">
                        <span class="camera-location">${camera.location || ''}</span>
                        <span class="camera-category">${camera.category || ''}</span>
                    </div>
                </div>
                <div class="camera-image-container">
                    <div class="hls-badge">HLS LIVE</div>
                    <video-js id="hls-player-${index}" 
                              class="video-js vjs-default-skin vjs-big-play-centered"
                              controls
                              autoplay
                              muted
                              playsinline
                              preload="auto">
                        <source src="${camera.hlsUrl}" type="application/x-mpegURL">
                    </video-js>
                </div>
            `;
        } else {
            cameraItem.innerHTML = `
                <div class="camera-header">
                    <div class="camera-name">${camera.name}</div>
                    <div class="camera-info">
                        <span class="camera-location">${camera.location || ''}</span>
                        <span class="camera-category">${camera.category || ''}</span>
                    </div>
                </div>
                <div class="camera-image-container">
                    <div class="loading">載入中...</div>
                    <img class="camera-image" 
                         data-camera-id="${camera.id}"
                         data-src="${camera.imageUrl}"
                         alt="${camera.name}"
                         style="display: none;">
                    <div class="last-update" id="lastUpdate${index}"></div>
                </div>
            `;
        }
        
        grid.appendChild(cameraItem);
    });
    
    initHlsPlayers(config);
    loadAllImages();

    // 點擊全螢幕事件
    document.querySelectorAll('.camera-image').forEach(img => {
        img.onclick = () => showFullscreen(img.src, img.alt);
    });
}

function setupEventListeners() {
    document.getElementById('refreshBtn').onclick = loadAllImages;
    document.getElementById('toggleAutoRefresh').onclick = toggleAutoRefresh;
}

function toggleAutoRefresh() {
    autoRefreshEnabled = !autoRefreshEnabled;
    const interval = (config?.refreshInterval || 60) * 1000;
    
    if (autoRefreshEnabled) {
        autoRefreshInterval = setInterval(loadAllImages, interval);
    } else {
        if (autoRefreshInterval) {
            clearInterval(autoRefreshInterval);
            autoRefreshInterval = null;
        }
    }
    
    updateRefreshStatus(autoRefreshEnabled, config?.refreshInterval || 60);
}

// 啟動 App
init();
