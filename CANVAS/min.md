明白了！你需要一个可以作为浏览器插件开发起点的项目模板，用于构建你的手写标记工具。下面是基于 Chrome 插件（Manifest V3）的最小初始化模板，支持：
	•	插件图标 & 描述
	•	可注入网页的绘图层（和你之前的需求一致）
	•	简洁目录结构，方便后续扩展图层/存储/Markdown 等功能

⸻

🗂 项目结构

web-ink-plugin/
├── manifest.json
├── content.js
├── assets/
│   └── icon.png
├── popup/
│   ├── popup.html
│   └── popup.js
└── styles/
    └── ink.css



⸻

📄 manifest.json

{
  "manifest_version": 3,
  "name": "Web Ink Layer",
  "description": "Draw on any webpage like using a plastic sheet overlay.",
  "version": "1.0",
  "permissions": ["scripting", "storage"],
  "host_permissions": ["<all_urls>"],
  "action": {
    "default_popup": "popup/popup.html",
    "default_icon": "assets/icon.png"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "css": ["styles/ink.css"]
    }
  ]
}



⸻

📄 content.js

if (window.hasRunInkPlugin) return;
window.hasRunInkPlugin = true;

// Create canvas overlay
const canvas = document.createElement('canvas');
canvas.id = 'inkCanvas';
document.body.appendChild(canvas);

const ctx = canvas.getContext('2d');
let drawing = false;

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Drawing logic
canvas.addEventListener('pointerdown', e => {
  drawing = true;
  ctx.beginPath();
  ctx.moveTo(e.clientX, e.clientY);
});
canvas.addEventListener('pointermove', e => {
  if (!drawing) return;
  ctx.lineTo(e.clientX, e.clientY);
  ctx.stroke();
});
canvas.addEventListener('pointerup', () => {
  drawing = false;
});



⸻

📄 styles/ink.css

#inkCanvas {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9999;
  pointer-events: auto;
  width: 100vw;
  height: 100vh;
}



⸻

📄 popup/popup.html

<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: sans-serif; padding: 10px; width: 150px; }
    button { margin-top: 5px; width: 100%; }
  </style>
</head>
<body>
  <h4>🖋️ Web Ink</h4>
  <button id="clear">Clear</button>
  <script src="popup.js"></script>
</body>
</html>



⸻

📄 popup/popup.js

chrome.scripting.executeScript({
  target: {tabId: chrome.devtools.inspectedWindow.tabId},
  func: () => {
    const canvas = document.getElementById('inkCanvas');
    if (canvas) {
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
  }
});



⸻

✅ 使用方法
	1.	在 Chrome 浏览器打开 chrome://extensions
	2.	打开开发者模式
	3.	点击“加载已解压的扩展程序”
	4.	选择 web-ink-plugin 目录
	5.	打开任意网页，在插件弹窗中点击按钮试试！

⸻

需要我帮你打包成 .zip 或者补全哪些细节（图层、保存、Markdown 支持等）？