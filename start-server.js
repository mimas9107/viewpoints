#!/usr/bin/env node
/**
 * Viewpoints MCP Server + HTTP Server
 * 
 * 1. HTTP Server (Port 8000): 服務靜態網頁
 * 2. MCP Server (Stdio): 提供 AI 工具 (Tools) 來查詢監視器
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { CallToolRequestSchema, ListToolsRequestSchema } = require('@modelcontextprotocol/sdk/types.js');
const { z } = require('zod');

// ==========================================
// HTTP Server Configuration
// ==========================================
const PORT = 8848;
const mimeTypes = {
    '.html': 'text/html',
    '.json': 'application/json',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
};

// ==========================================
// Data Management
// ==========================================
function loadCameras() {
    try {
        const data = fs.readFileSync(path.join(__dirname, 'cameras_database.json'), 'utf8');
        return JSON.parse(data).cameras || [];
    } catch (e) {
        console.error('Failed to load cameras database:', e);
        return [];
    }
}

function loadConfig() {
    try {
        const data = fs.readFileSync(path.join(__dirname, 'viewpoints.json'), 'utf8');
        return JSON.parse(data);
    } catch (e) {
        return null;
    }
}

// ==========================================
// MCP Server Setup
// ==========================================
const mcpServer = new Server(
    {
        name: "viewpoints-server",
        version: "1.0.0",
    },
    {
        capabilities: {
            tools: {},
        },
    }
);

// Define Tools
mcpServer.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: "list_cameras",
                description: "列出所有可用的監視器，支援透過關鍵字或分類篩選",
                inputSchema: zodToJsonSchema(z.object({
                    keyword: z.string().optional().describe("搜尋關鍵字 (例如: 林口, 陽明山)"),
                    category: z.string().optional().describe("分類篩選 (例如: 國道, 景點, 市區)")
                }))
            },
            {
                name: "get_camera_image",
                description: "獲取特定監視器的即時影像 URL，可用於視覺分析",
                inputSchema: zodToJsonSchema(z.object({
                    id: z.string().describe("監視器 ID (從 list_cameras 獲取)"),
                }))
            },
            {
                name: "get_current_config",
                description: "讀取目前監控牆的配置 (viewpoints.json)",
                inputSchema: zodToJsonSchema(z.object({}))
            }
        ],
    };
});

// Handle Tool Calls
mcpServer.setRequestHandler(CallToolRequestSchema, async (request) => {
    const cameras = loadCameras();

    switch (request.params.name) {
        case "list_cameras": {
            const keyword = request.params.arguments?.keyword?.toLowerCase();
            const category = request.params.arguments?.category;

            let filtered = cameras;
            if (keyword) {
                filtered = filtered.filter(c => 
                    c.name.toLowerCase().includes(keyword) || 
                    c.location.toLowerCase().includes(keyword)
                );
            }
            if (category) {
                filtered = filtered.filter(c => c.category === category);
            }

            // 只回傳前 20 筆以避免 token 過多，除非有精確搜尋
            const limit = keyword ? 50 : 20;
            const result = filtered.slice(0, limit).map(c => ({
                id: c.id,
                name: c.name,
                category: c.category,
                type: c.type,
                location: c.location
            }));

            return {
                content: [{
                    type: "text",
                    text: JSON.stringify({
                        total: filtered.length,
                        showing: result.length,
                        cameras: result
                    }, null, 2)
                }]
            };
        }

        case "get_camera_image": {
            const id = request.params.arguments?.id;
            const camera = cameras.find(c => c.id === id);

            if (!camera) {
                return {
                    content: [{ type: "text", text: `Error: Camera ID '${id}' not found.` }],
                    isError: true
                };
            }

            let imageUrl = "";
            if (camera.type === 'image') {
                // 為靜態圖片加上 timestamp 防止快取
                imageUrl = `${camera.imageUrl}${camera.imageUrl.includes('?') ? '&' : '?'}t=${Date.now()}`;
            } else if (camera.type === 'youtube') {
                // YouTube 縮圖
                imageUrl = `https://img.youtube.com/vi/${camera.youtubeId}/maxresdefault.jpg`;
            } else if (camera.type === 'hls') {
                // HLS 通常無法直接獲取靜態圖，這裡嘗試回傳縮圖如果有的話，或提示
                imageUrl = camera.thumbnail || "HLS串流不支援直接截圖，請嘗試訪問串流 URL";
            }

            return {
                content: [{
                    type: "text",
                    text: JSON.stringify({
                        id: camera.id,
                        name: camera.name,
                        type: camera.type,
                        imageUrl: imageUrl,
                        streamUrl: camera.url || camera.hlsUrl || camera.imageUrl
                    }, null, 2)
                }]
            };
        }

        case "get_current_config": {
            const config = loadConfig();
            return {
                content: [{
                    type: "text",
                    text: JSON.stringify(config || { error: "No config found" }, null, 2)
                }]
            };
        }

        default:
            throw new Error("Unknown tool");
    }
});

// Helper: Convert Zod to JSON Schema
function zodToJsonSchema(schema) {
    // 簡單的轉換，實際專案可能需要 zod-to-json-schema 套件
    // 這裡手動實作最基本的部分以減少依賴
    const shape = schema.shape;
    const properties = {};
    const required = [];

    for (const key in shape) {
        const field = shape[key];
        let type = 'string';
        let description = '';
        
        if (field.description) description = field.description;
        if (field.isOptional && field.isOptional()) {
            // optional
        } else {
            required.push(key);
        }

        properties[key] = { type, description };
    }

    return {
        type: "object",
        properties,
        required: required.length > 0 ? required : undefined
    };
}

// ==========================================
// Start Servers
// ==========================================

async function start() {
    // 1. Start HTTP Server
    const httpServer = http.createServer((req, res) => {
        let filePath = '.' + (req.url === '/' ? '/index.html' : req.url);
        
        // 簡單的安全檢查，防止讀取上一層目錄
        if (filePath.includes('..')) {
            res.writeHead(403);
            res.end('Access Denied');
            return;
        }

        const extname = String(path.extname(filePath)).toLowerCase();
        const contentType = mimeTypes[extname] || 'application/octet-stream';

        fs.readFile(filePath, (error, content) => {
            if (error) {
                if (error.code === 'ENOENT') {
                    res.writeHead(404, { 'Content-Type': 'text/html' });
                    res.end('<h1>404 - Not Found</h1>', 'utf-8');
                } else {
                    res.writeHead(500);
                    res.end('Server Error: ' + error.code, 'utf-8');
                }
            } else {
                res.writeHead(200, { 
                    'Content-Type': contentType,
                    'Access-Control-Allow-Origin': '*'
                });
                res.end(content, 'utf-8');
            }
        });
    });

    httpServer.listen(PORT, () => {
        // 只有在不是作為 MCP 運作時才輸出 log，避免干擾 stdio
        // 但為了方便，我們輸出到 stderr，這樣不會影響 MCP (stdout)
        console.error(`HTTP Server running at http://localhost:${PORT}`);
        
        // 自動開啟瀏覽器 (僅在直接執行時，如果是被 MCP Client 呼叫則不開啟)
        // 簡單判斷：如果有父進程，可能是被呼叫的
        if (process.ppid) {
           // Do nothing
        } else {
            // Auto open logic here if needed
        }
    });

    // 2. Start MCP Server
    const transport = new StdioServerTransport();
    await mcpServer.connect(transport);
    console.error("Viewpoints MCP Server running on stdio");
}

start().catch((error) => {
    console.error("Server error:", error);
    process.exit(1);
});
