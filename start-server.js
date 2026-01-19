#!/usr/bin/env node
/**
 * 监视器墙本地服务器启动脚本
 * 使用 Node.js 内置的 HTTP 服务器
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PORT = 8000;

// MIME 类型映射
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

const server = http.createServer((req, res) => {
    // 处理请求路径
    let filePath = '.' + (req.url === '/' ? '/index.html' : req.url);
    const extname = String(path.extname(filePath)).toLowerCase();
    const contentType = mimeTypes[extname] || 'application/octet-stream';

    // 读取文件
    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code === 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/html' });
                res.end('<h1>404 - 文件未找到</h1>', 'utf-8');
            } else {
                res.writeHead(500);
                res.end('服务器错误: ' + error.code, 'utf-8');
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

// 启动服务器
server.listen(PORT, () => {
    const url = `http://localhost:${PORT}`;
    console.log('='.repeat(60));
    console.log('监视器墙服务器已启动！');
    console.log('='.repeat(60));
    console.log('');
    console.log(`访问地址: ${url}`);
    console.log('');
    console.log('按 Ctrl+C 停止服务器');
    console.log('='.repeat(60));

    // 自动在浏览器中打开
    const platform = process.platform;
    const command = platform === 'darwin' ? 'open' : 
                   platform === 'win32' ? 'start' : 'xdg-open';
    
    try {
        execSync(`${command} ${url}`, { stdio: 'ignore' });
    } catch (e) {
        // 忽略错误
    }
});

// 处理退出
process.on('SIGINT', () => {
    console.log('\n');
    console.log('='.repeat(60));
    console.log('服务器已停止');
    console.log('='.repeat(60));
    process.exit(0);
});

// 错误处理
server.on('error', (e) => {
    if (e.code === 'EADDRINUSE') {
        console.error(`错误: 端口 ${PORT} 已被占用`);
        console.error('请关闭占用该端口的程序，或修改脚本中的 PORT 变量');
    } else {
        console.error('错误:', e);
    }
    process.exit(1);
});
