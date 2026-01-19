/**
 * 播放器管理模組 (HLS/Video.js)
 */
export function initHlsPlayers(config) {
    if (typeof videojs === 'undefined') return;

    config.cameras.forEach((camera, index) => {
        if (camera.type === 'hls') {
            const playerId = `hls-player-${index}`;
            const playerElement = document.getElementById(playerId);
            
            if (playerElement) {
                const player = videojs(playerId, {
                    autoplay: true,
                    muted: true,
                    preload: 'auto',
                    fluid: true,
                    liveui: true,
                    html5: {
                        hls: {
                            enableLowInitialPlaylist: true,
                            smoothQualityChange: true,
                            overrideNative: true
                        }
                    }
                });

                player.ready(function() {
                    this.play().catch(err => {
                        console.log('自動播放被攔截:', err);
                    });
                });
            }
        }
    });
}
