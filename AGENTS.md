# Agent Instructions for Viewpoints

This document provides guidelines for AI coding agents working on the Viewpoints project - a customizable CCTV monitoring wall system.

## Project Overview

**Type:** Static web application with local server scripts  
**Tech Stack:** HTML5, vanilla JavaScript, CSS3, Python 3, Node.js  
**Dependencies:** Video.js (CDN), no local npm/pip packages  
**Structure:** Single-page application with JSON configuration

## Repository Structure

```
viewpoints/
├── index.html              # Main application (HTML/CSS/JS in one file)
├── picker.html             # Camera picker UI for selecting cameras
├── viewpoints.json         # Configuration with camera definitions
├── viewpoints.json.template # Empty template for new configurations
├── cameras_database.json   # Database of all available cameras (600+ cameras)
├── start-server.py         # Python HTTP server launcher
├── start-server.js         # Node.js HTTP + MCP server launcher
├── MCP_GUIDE.md            # MCP Server setup guide for AI integration
├── README.md               # User documentation
├── QUICKSTART.md           # Quick start guide
├── AGENTS.md               # This file - guidelines for AI agents
├── LICENSE                 # MIT license
└── .gitignore              # Git ignore rules
```

## Build/Test/Run Commands

### Running the Application

**Start Python server (recommended):**
```bash
python3 start-server.py
```

**Start Node.js server:**
```bash
node start-server.js
```

**Alternative methods:**
```bash
# Python built-in server
python3 -m http.server 8000

# Node http-server (if installed)
npx http-server -p 8000
```

The application will open at `http://localhost:8000`.

### Testing

**No formal test suite exists.** Manual testing checklist:

1. Start server and verify page loads
2. Test static image cameras (image loading, refresh)
3. Test YouTube cameras (iframe embedding, autoplay)
4. Test HLS cameras (Video.js player, streaming)
5. Test manual refresh button
6. Test auto-refresh toggle
7. Test fullscreen functionality (click image, ESC key)
8. Test responsive layout on mobile
9. Verify JSON configuration changes take effect on reload

### Linting

**No linters configured.** For manual code quality checks:
- Use browser DevTools console (F12) to check for errors
- Validate JSON: `python3 -m json.tool viewpoints.json`
- HTML validation: Use W3C validator if needed

## MCP Server

The `start-server.js` file includes a dual-mode server that provides both HTTP and MCP (Model Context Protocol) interfaces:

### Features

- **HTTP Server (Port 8000):** Serves static files (index.html, picker.html)
- **MCP Server (Stdio):** Provides tools for AI assistants to query camera data

### Available Tools

| Tool | Description |
|------|-------------|
| `list_cameras` | List all cameras with optional keyword/category filters |
| `get_camera_image` | Get the image URL for a specific camera (supports static images, YouTube thumbnails) |
| `get_current_config` | Read the current viewpoints.json configuration |

### Usage for AI Agents

When working as an AI agent with access to this MCP server, you can:
1. Use `list_cameras` to find cameras by location or category
2. Use `get_camera_image` to get the image URL
3. Analyze the returned URL to provide visual insights about traffic or weather

Example workflow:
```
User: "Is there traffic congestion on National Highway 1 at Linkou?"
Agent: 
1. Call list_cameras(keyword="林口", category="國道")
2. Call get_camera_image(id="1030-N-14.7-M") 
3. Analyze the returned image URL and provide a response
```

## Code Style Guidelines

### HTML

- **Indentation:** 4 spaces
- **Language:** `lang="zh-Hant-TW"` (Traditional Chinese)
- **Meta tags:** Include charset UTF-8 and viewport for mobile
- **Structure:** Semantic HTML5 elements where appropriate
- **Classes:** Use kebab-case (e.g., `camera-grid`, `camera-item`)

### CSS

- **Embedded:** All CSS is in `<style>` tag in index.html
- **Reset:** Universal box-sizing and margin/padding reset
- **Color scheme:** Dark theme (#1a1a1b background, #2d2d2e panels)
- **Layout:** CSS Grid for camera grid, Flexbox for header/controls
- **Responsive:** Mobile-first with `@media (max-width: 768px)`
- **Naming:** BEM-like conventions (e.g., `camera-item`, `camera-header`, `camera-image-container`)
- **Units:** 
  - px for borders, shadows, small fixed sizes
  - rem/em for font sizes when appropriate
  - % or vh/vw for responsive layouts
  - Padding/margin in px

### JavaScript

- **Style:** ES6+ modern JavaScript (no build step, browser-native)
- **Variables:** `let` for mutable, `const` for immutable
- **Functions:** Use arrow functions for callbacks, regular functions for top-level
- **Async:** `async/await` for asynchronous operations
- **Naming conventions:**
  - Functions: camelCase (e.g., `loadConfig`, `renderCameras`)
  - Variables: camelCase (e.g., `autoRefreshInterval`, `config`)
  - Constants: UPPER_SNAKE_CASE if truly constant (e.g., PORT in servers)
  - DOM IDs: camelCase (e.g., `cameraGrid`, `pageTitle`)
  - CSS classes: kebab-case (e.g., `camera-item`)

**Example:**
```javascript
async function loadConfig() {
    try {
        const response = await fetch('./viewpoints.json');
        config = await response.json();
        renderCameras();
    } catch (error) {
        console.error('Failed to load config:', error);
        alert('无法加载配置文件');
    }
}
```

### Error Handling

- **Always use try-catch for async operations**
- **Console logging:** `console.error()` for errors, `console.log()` for debugging
- **User feedback:** Alert or inline error messages for critical failures
- **Graceful degradation:** Show error message in UI, allow retry (see loadImage function)

**Example:**
```javascript
tempImg.onerror = () => {
    loading.innerHTML = '<div class="error">加载失败<br>点击刷新重试</div>';
    loading.style.cursor = 'pointer';
    loading.onclick = () => loadImage(img, index);
};
```

### Python (start-server.py)

- **Style:** PEP 8 compliant
- **Docstrings:** Triple-quoted strings for module/function docs
- **Imports:** Standard library only (http.server, socketserver, os, webbrowser, sys)
- **Error handling:** Try-except with specific exception types
- **Constants:** UPPER_CASE (e.g., `PORT = 8000`)
- **Indentation:** 4 spaces

### Node.js (start-server.js)

- **Style:** CommonJS modules (`require`/`module.exports`)
- **Conventions:** camelCase for variables/functions
- **Error handling:** Error-first callbacks, try-catch where appropriate
- **Constants:** const for immutable values
- **Indentation:** 4 spaces

### JSON (viewpoints.json)

- **Indentation:** 2 spaces
- **Structure:** Must include `title`, `autoRefresh`, `refreshInterval`, `layout`, `cameras`
- **Camera types:**
  - Static image: `type` omitted or `"image"`, requires `imageUrl`
  - YouTube: `type: "youtube"`, requires `youtubeId`
  - HLS: `type: "hls"`, requires `hlsUrl`
- **Required fields per camera:** `id`, `name`, `location`, `category`
- **Validation:** Ensure layout columns × rows ≥ camera count

## Making Changes

### Adding New Features

1. **HTML changes:** Edit `index.html` structure section
2. **CSS changes:** Edit `<style>` section in index.html
3. **JavaScript changes:** Edit `<script>` section in index.html
4. **Configuration:** Modify `viewpoints.json` for data changes
5. **Documentation:** Update README.md with user-facing changes

### Camera Types Implementation

When adding support for new camera types:

1. Add type check in `renderCameras()` function
2. Create appropriate HTML structure (iframe, video, img)
3. Initialize player/loader if needed (like `initHlsPlayers()`)
4. Add distinctive badge styling
5. Update viewpoints.json.template with example
6. Document in README.md

### Common Tasks

**Add a new camera to default configuration:**
```json
{
  "id": "unique-id",
  "name": "Display Name",
  "description": "Detailed description",
  "imageUrl": "https://example.com/image.jpg",
  "location": "City, Region",
  "category": "国道/省道/市区/景点"
}
```

**Change grid layout:**
Modify `layout` in viewpoints.json and ensure CSS class exists in index.html (grid-2x2, grid-3x2, grid-3x3, grid-4x3).

**Modify refresh interval:**
Edit `refreshInterval` in viewpoints.json (value in seconds).

## Important Notes

- **CORS:** Application must run through HTTP server, not file:// protocol
- **No build process:** All code is browser-ready, no transpilation/bundling
- **External dependencies:** Only Video.js via CDN (for HLS playback)
- **Browser support:** Modern browsers (Chrome, Firefox, Edge, Safari)
- **Language:** UI text is in Traditional Chinese (zh-Hant-TW)
- **Timestamps:** Images include cache-busting timestamp parameter
- **Security:** Basic CORS headers in server scripts for local development

## Git Workflow

- Commit messages in English or Chinese are acceptable
- Keep commits atomic and descriptive
- No force push to main branch
- Test manually before committing

## Debugging Tips

1. Open browser DevTools (F12) → Console tab for JavaScript errors
2. Network tab to inspect image/stream loading
3. Check server console for HTTP errors
4. Validate viewpoints.json with `python3 -m json.tool viewpoints.json`
5. Test different camera types independently

## Resources

- Main documentation: README.md
- Quick start: QUICKSTART.md
- Video.js docs: https://videojs.com/
- Camera sources: https://tw.live/
