// FastAPI 深度专题 - 导航交互脚本

(function() {
    'use strict';

    // DOM 元素
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const darkModeToggle = document.getElementById('darkModeToggle');
    const content = document.getElementById('content');
    const breadcrumbCurrent = document.getElementById('breadcrumbCurrent');
    const previewPanel = document.getElementById('previewPanel');
    const previewBody = document.getElementById('previewBody');
    const previewClose = document.getElementById('previewClose');
    const progressText = document.querySelector('.progress-text');
    const progressFill = document.querySelector('.progress-fill');

    // 暗色模式切换
    function toggleDarkMode() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        // 更新按钮图标
        darkModeToggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
    }

    // 初始化暗色模式
    function initDarkMode() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        darkModeToggle.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
    }

    // 侧边栏切换（移动端）
    function toggleSidebar() {
        sidebar.classList.toggle('active');
    }

    // 加载章节内容
    async function loadChapter(chapterNum) {
        try {
            const chapterTitles = {
                '02': '02_路由与依赖注入进阶',
                '03': '03_数据模型与校验_Pydantic2',
                '04': '04_数据库与事务',
                '05': '05_认证与授权',
                '06': '06_中间件与跨切面',
                '07': '07_异步与背景任务',
                '08': '08_WebSocket与实时推送',
                '09': '09_测试与Mock'
            };

            const chapterPaths = {
                '02': '../../02.开发环境及框架介绍/04_FastAPI_深度专题/02_路由与依赖注入进阶.md',
                '03': '../../02.开发环境及框架介绍/04_FastAPI_深度专题/03_数据模型与校验_Pydantic2.md',
                '04': '../../02.开发环境及框架介绍/04_FastAPI_深度专题/04_数据库与事务.md',
                '05': '../../02.开发环境及框架介绍/04_FastAPI_深度专题/05_认证与授权.md',
                '06': '../../02.开发环境及框架介绍/04_FastAPI_深度专题/06_中间件与跨切面.md',
                '07': '../../02.开发环境及框架介绍/04_FastAPI_深度专题/07_异步与背景任务.md',
                '08': '../../02.开发环境及框架介绍/04_FastAPI_深度专题/08_WebSocket与实时推送.md',
                '09': '../../02.开发环境及框架介绍/04_FastAPI_深度专题/09_测试与Mock.md'
            };

            const title = chapterTitles[chapterNum] || `第 ${chapterNum} 章`;
            const path = chapterPaths[chapterNum] || '';

            await renderMarkdown(path, title);
            renderLeftSummary(title, path, false);

            // 更新面包屑
            breadcrumbCurrent.innerHTML = ` <span>/</span> ${title}`;

            // 语法高亮
            if (window.Prism) {
                Prism.highlightAll();
            }
        } catch (error) {
            console.error('加载章节失败:', error);
            content.innerHTML = '<p>加载内容失败，请检查文件路径。</p>';
        }
    }

    // 加载实验室内容
    async function loadLab(labName) {
        try {
            const labTitles = {
                'lab01': 'lab01_router_splitting - 路由拆分练习',
                'lab02': 'lab02_dep_chain_override - 依赖链覆盖',
                'lab03': 'lab03_async_sqlalchemy - 异步 SQLAlchemy',
                'lab04': 'lab04_websocket_chat - WebSocket 聊天/通知',
                'lab05': 'lab05_jwt_rbac - JWT + RBAC 实验'
            };

            const title = labTitles[labName] || labName;
            const labPath = `../../02.开发环境及框架介绍/04_FastAPI_深度专题/labs/${labName}/README.md`;

            const ok = await renderMarkdown(labPath, title, true);
            if (!ok) {
                // 若无 README，给出操作指南
                previewBody.innerHTML = `
                    <h2 style="margin-top:0;">${title}</h2>
                    <div class="info-box">
                        <p>未找到实验文档，按以下步骤操作：</p>
                        <ol>
                            <li>进入目录：<code>02.开发环境及框架介绍/04_FastAPI_深度专题/labs/${labName}/</code></li>
                            <li>阅读代码注释，完成 TODO</li>
                            <li>安装依赖：<code>pip install fastapi uvicorn pytest</code></li>
                            <li>运行：<code>uvicorn app.main:app --reload</code>，访问 <code>http://127.0.0.1:8000/docs</code></li>
                            <li>执行测试（若提供）：<code>pytest</code></li>
                        </ol>
                    </div>
                `;
            }
            renderLeftSummary(title, ok ? labPath : null, true);

            // 更新面包屑
            breadcrumbCurrent.innerHTML = ` <span>/</span> ${title}`;

            // 语法高亮
            if (window.Prism) {
                Prism.highlightAll();
            }
        } catch (error) {
            console.error('加载实验失败:', error);
            content.innerHTML = '<p>加载内容失败，请检查文件路径。</p>';
        }
    }

    // 初始化事件监听器
    function init() {
        // 暗色模式
        initDarkMode();
        darkModeToggle.addEventListener('click', toggleDarkMode);

        // 侧边栏切换
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', toggleSidebar);
        }

        // 章节链接点击
        document.querySelectorAll('[data-chapter]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const chapterNum = e.target.dataset.chapter;
                setActiveItem(e.target.closest('.nav-item'));
                loadChapter(chapterNum);
            });
        });

        // 实验室链接点击
        document.querySelectorAll('[data-lab]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const labName = e.target.dataset.lab;
                setActiveItem(e.target.closest('.nav-item'));
                loadLab(labName);
            });
        });

        // 关闭移动端侧边栏（点击内容区域时）
        content.addEventListener('click', () => {
            if (window.innerWidth <= 768 && sidebar.classList.contains('active')) {
                sidebar.classList.remove('active');
            }
        });

        // 关闭预览
        if (previewClose) {
            previewClose.addEventListener('click', () => {
                previewBody.innerHTML = `<p style="color: var(--text-secondary);">右侧空间将显示所选章节/实验的 Markdown 内容。</p>`;
            });
        }

        // 默认加载第一章
        previewBody.innerHTML = `<p style="color: var(--text-secondary);">右侧空间将显示所选章节/实验的 Markdown 内容。</p>`;
        updateProgress(0);
    }

    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ========== Markdown 渲染工具 ==========
    async function renderMarkdown(path, title, silent=false) {
        if (!path) {
            if (!silent) {
                previewBody.innerHTML = `<p>未找到对应文档路径，请检查课程配置。</p>`;
            }
            return false;
        }
        try {
            const resp = await fetch(encodeURI(path));
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const md = await resp.text();
            const html = window.marked ? marked.parse(md) : md.replace(/\n/g, '<br>');

            previewBody.innerHTML = `
                <h2 style="margin-top:0;">${title}</h2>
                <div class="md-body">${html}</div>
                <div class="info-box" style="margin-top:12px;">
                    <p style="margin:0;">来源：${path}</p>
                    <p style="margin:4px 0 0;">提示：若无法加载，请从仓库根目录启动静态服务，例如：
                    <code>python -m http.server 5500</code> （确保能访问该 Markdown 路径）</p>
                </div>
            `;

            if (window.Prism) {
                Prism.highlightAll();
            }
            return true;
        } catch (err) {
            console.error('渲染 Markdown 失败', err);
            if (!silent) {
                previewBody.innerHTML = `
                    <h2 style="margin-top:0;">${title}</h2>
                    <p>文档加载失败，可能原因：未从仓库根目录启动静态服务器或路径不存在。</p>
                    <code>${path}</code>
                `;
            }
            return false;
        }
    }

    function setActiveItem(item) {
        if (!item) return;
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');

        // 状态圆点更新：全部设为 ○，当前设为 ✓
        document.querySelectorAll('.nav-item .status').forEach(s => {
            s.textContent = '○';
            s.style.color = 'var(--text-secondary)';
        });
        const statusEl = item.querySelector('.status');
        if (statusEl) {
            statusEl.textContent = '✓';
            statusEl.style.color = 'var(--success-color, #22c55e)';
        }

        const text = item.innerText.trim();
        if (progressText) {
            progressText.textContent = `当前：${text}`;
        }

        updateProgress(calcProgress(item));
    }

    // 左侧内容区同步概览
    function renderLeftSummary(title, path, isLab=false) {
        const typeLabel = isLab ? '实验室' : '章节';
        const pathInfo = path ? `<code>${path}</code>` : '<span style="color: var(--text-secondary);">未找到文档路径，查看右侧指引</span>';
        content.innerHTML = `
            <h1>${title}</h1>
            <div class="info-box">
                <h4 style="margin:0 0 6px 0;">${typeLabel}概览</h4>
                <p style="margin:0;">来源路径：${pathInfo}</p>
            </div>
            <h2>如何学习</h2>
            <ol>
                <li>右侧预览阅读完整内容</li>
                <li>${isLab ? '按步骤运行代码并完成 TODO/测试' : '结合右侧文档示例在本地实践'}</li>
                <li>若预览失败，可在本地直接打开上述路径的 Markdown</li>
            </ol>
            <div class="info-box">
                <p style="margin:0;">小贴士：启动静态服务时建议在仓库根目录运行 <code>python -m http.server 5500</code>，以确保相对路径可访问。</p>
            </div>
        `;
    }

    // 计算进度：当前项在可点击列表中的顺序位置
    function calcProgress(currentItem) {
        const clickable = Array.from(document.querySelectorAll('.nav-item a[data-chapter], .nav-item a[data-lab]'))
            .map(a => a.closest('.nav-item'))
            .filter(Boolean);
        if (clickable.length === 0 || !currentItem) return 0;
        const idx = clickable.indexOf(currentItem);
        if (idx === -1) return 0;
        return (idx + 1) / clickable.length;
    }

    function updateProgress(ratio) {
        if (!progressFill) return;
        const pct = Math.max(0, Math.min(1, ratio));
        progressFill.style.width = `${Math.round(pct * 100)}%`;
    }
})();
