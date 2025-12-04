// FastAPI 深度专题 - 导航交互脚本

(function() {
    'use strict';

    // DOM 元素
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const darkModeToggle = document.getElementById('darkModeToggle');
    const content = document.getElementById('content');
    const breadcrumbCurrent = document.getElementById('breadcrumbCurrent');

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
            // 这里应该从 Markdown 文件加载内容
            // 当前简化版本，直接显示提示信息
            const chapterTitles = {
                '02': '02_路由与依赖注入进阶'
            };

            const title = chapterTitles[chapterNum] || `第 ${chapterNum} 章`;

            content.innerHTML = `
                <h1>${title}</h1>
                <div class="info-box">
                    <h4>📖 学习指引</h4>
                    <p>请前往项目目录查看完整的 Markdown 文档：</p>
                    <code>02.开发环境及框架介绍/04_FastAPI_深度专题/${title}.md</code>
                </div>
                <h2>如何学习这一章</h2>
                <ol>
                    <li>阅读 Markdown 文档中的理论部分</li>
                    <li>运行文档中的代码示例</li>
                    <li>完成对应的实验室练习</li>
                    <li>标记本章节为已完成</li>
                </ol>
            `;

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
                'lab01': 'lab01_router_splitting - 路由拆分练习'
            };

            const title = labTitles[labName] || labName;

            content.innerHTML = `
                <h1>${title}</h1>
                <div class="info-box">
                    <h4>🛠️ 实验指引</h4>
                    <p>请前往实验目录查看 README 和代码：</p>
                    <code>02.开发环境及框架介绍/04_FastAPI_深度专题/labs/${labName}/</code>
                </div>
                <h2>实验步骤</h2>
                <ol>
                    <li>进入实验目录</li>
                    <li>阅读 README.md 了解实验目标</li>
                    <li>安装必要的依赖</li>
                    <li>运行代码并测试</li>
                    <li>完成验收清单</li>
                </ol>
                <h2>快速开始</h2>
                <pre><code class="language-bash">cd "02.开发环境及框架介绍/04_FastAPI_深度专题/labs/${labName}"
pip install fastapi uvicorn pytest
uvicorn app.main:app --reload
# 访问 http://127.0.0.1:8000/docs</code></pre>
            `;

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
                loadChapter(chapterNum);

                // 移除所有active类
                document.querySelectorAll('.nav-item').forEach(item => {
                    item.classList.remove('active');
                });
                // 添加active类到当前项
                e.target.closest('.nav-item').classList.add('active');
            });
        });

        // 实验室链接点击
        document.querySelectorAll('[data-lab]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const labName = e.target.dataset.lab;
                loadLab(labName);

                // 移除所有active类
                document.querySelectorAll('.nav-item').forEach(item => {
                    item.classList.remove('active');
                });
                // 添加active类到当前项
                e.target.closest('.nav-item').classList.add('active');
            });
        });

        // 关闭移动端侧边栏（点击内容区域时）
        content.addEventListener('click', () => {
            if (window.innerWidth <= 768 && sidebar.classList.contains('active')) {
                sidebar.classList.remove('active');
            }
        });
    }

    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
