// 全局状态
let allCredentials = [];
let allCommands = [];
let allTabs = [];
let currentTabId = null;
let convertedNodes = [];
let expandedCredentialIds = new Set(); // 凭证附加信息展开状态

// 初始化
document.addEventListener('DOMContentLoaded', async () => {
    await waitForPywebview();
    initNavigation();
    initTheme();
    loadCredentials();
    await loadTabs();
    loadCommands();
    loadNodes();
});

function waitForPywebview() {
    return new Promise(resolve => {
        if (window.pywebview && window.pywebview.api) {
            resolve();
        } else {
            window.addEventListener('pywebviewready', resolve);
        }
    });
}

// 导航
function initNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            item.classList.add('active');
            document.getElementById(`page-${item.dataset.page}`).classList.add('active');
        });
    });
}

// 主题切换
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const icon = document.querySelector('.theme-icon');
    if (icon) {
        icon.textContent = theme === 'dark' ? '🌙' : '☀️';
    }
}

// ==================== 凭证管理 ====================
async function loadCredentials() {
    allCredentials = await pywebview.api.get_credentials();
    renderCredentials(allCredentials);
}

function renderCredentials(credentials) {
    const container = document.getElementById('credentials-list');
    if (!credentials.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔐</div>
                <div class="empty-state-text">暂无记录，点击右上角添加</div>
            </div>`;
        return;
    }

    container.innerHTML = credentials.map(cred => `
        <div class="credential-card" data-cred-id="${cred.id}" draggable="true"
             ondragstart="onCredentialDragStart(event)"
             ondragover="onCredentialDragOver(event)"
             ondrop="onCredentialDrop(event)"
             ondragend="onCredentialDragEnd(event)">
            <div class="credential-header">
                <div class="credential-title-area">
                    <div class="credential-service">${escapeHtml(cred.service)}</div>
                    ${cred.url ? `<div class="credential-url"><a href="${escapeHtml(cred.url)}" target="_blank">${escapeHtml(cred.url)}</a></div>` : ''}
                </div>
                <div class="credential-actions">
                    <button class="btn btn-sm btn-ghost" onclick="editCredential('${cred.id}')">编辑</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteCredential('${cred.id}')">删除</button>
                </div>
            </div>
            <div class="credential-body">
                ${cred.account ? `
                <div class="credential-field">
                    <span class="credential-label">账号</span>
                    <span class="credential-value">${escapeHtml(cred.account)}</span>
                    <button class="copy-btn" onclick="copyField(this, '${escapeAttr(cred.account)}')" title="复制">📋</button>
                </div>` : ''}
                ${cred.password ? `
                <div class="credential-field">
                    <span class="credential-label">密码</span>
                    <span class="credential-value">${escapeHtml(cred.password)}</span>
                    <button class="copy-btn" onclick="copyField(this, '${escapeAttr(cred.password)}')" title="复制">📋</button>
                </div>` : ''}
            </div>
            ${cred.extra && cred.extra.length ? `
            <div class="credential-extra-toggle">
                <button class="btn btn-sm btn-ghost" onclick="toggleCredentialExtra('${cred.id}', event)">
                    ${expandedCredentialIds.has(cred.id) ? '收起附加信息' : '展开附加信息'}
                </button>
            </div>
            <div class="credential-extra ${expandedCredentialIds.has(cred.id) ? 'expanded' : ''}">
                ${cred.extra.map(e => `<div class="credential-extra-item">${escapeHtml(e)}</div>`).join('')}
            </div>` : ''}
        </div>
    `).join('');
}

function filterCredentials() {
    const keyword = document.getElementById('credential-search').value.toLowerCase();
    const filtered = allCredentials.filter(c =>
        c.service.toLowerCase().includes(keyword) ||
        c.account.toLowerCase().includes(keyword) ||
        c.url.toLowerCase().includes(keyword)
    );
    renderCredentials(filtered);
}

function showCredentialModal(cred = null) {
    document.getElementById('credential-modal-title').textContent = cred ? '编辑记录' : '添加记录';
    document.getElementById('credential-id').value = cred?.id || '';
    document.getElementById('credential-service').value = cred?.service || '';
    document.getElementById('credential-url').value = cred?.url || '';
    document.getElementById('credential-account').value = cred?.account || '';
    document.getElementById('credential-password').value = cred?.password || '';
    document.getElementById('credential-extra').value = cred?.extra?.join('\n') || '';
    openModal('credential-modal');
}

async function editCredential(id) {
    const cred = allCredentials.find(c => c.id === id);
    if (cred) showCredentialModal(cred);
}

async function saveCredential() {
    const id = document.getElementById('credential-id').value;
    const service = document.getElementById('credential-service').value.trim();
    const url = document.getElementById('credential-url').value.trim();
    const account = document.getElementById('credential-account').value.trim();
    const password = document.getElementById('credential-password').value.trim();
    const extra = document.getElementById('credential-extra').value.split('\n').filter(l => l.trim());

    if (!service) {
        alert('请填写服务名称');
        return;
    }

    if (id) {
        await pywebview.api.update_credential(id, service, url, account, password, extra);
    } else {
        await pywebview.api.add_credential(service, url, account, password, extra);
    }
    closeModal('credential-modal');
    loadCredentials();
}

async function deleteCredential(id) {
    if (confirm('确定删除此记录？')) {
        await pywebview.api.delete_credential(id);
        loadCredentials();
    }
}

function toggleCredentialExtra(id, e) {
    if (e) e.stopPropagation();
    if (expandedCredentialIds.has(id)) {
        expandedCredentialIds.delete(id);
    } else {
        expandedCredentialIds.add(id);
    }
    // 重新渲染以更新展开状态与按钮文案
    const keyword = document.getElementById('credential-search').value.toLowerCase();
    const filtered = allCredentials.filter(c =>
        c.service.toLowerCase().includes(keyword) ||
        c.account.toLowerCase().includes(keyword) ||
        c.url.toLowerCase().includes(keyword)
    );
    renderCredentials(keyword ? filtered : allCredentials);
}

// 凭证拖拽排序
let draggedCredentialId = null;

function onCredentialDragStart(e) {
    const card = e.target.closest('.credential-card');
    if (!card) return;
    draggedCredentialId = card.dataset.credId;
    card.classList.add('dragging');
    if (e.dataTransfer) {
        e.dataTransfer.effectAllowed = 'move';
    }
}

function onCredentialDragOver(e) {
    e.preventDefault();
    const target = e.target.closest('.credential-card');
    if (target && target.dataset.credId !== draggedCredentialId) {
        target.classList.add('drag-over');
    }
}

async function onCredentialDrop(e) {
    e.preventDefault();
    const target = e.target.closest('.credential-card');
    if (target && draggedCredentialId && target.dataset.credId !== draggedCredentialId) {
        await reorderCredentials(draggedCredentialId, target.dataset.credId);
    }
    document.querySelectorAll('.credential-card').forEach(el => el.classList.remove('drag-over'));
}

function onCredentialDragEnd() {
    draggedCredentialId = null;
    document.querySelectorAll('.credential-card').forEach(el => {
        el.classList.remove('dragging', 'drag-over');
    });
}

async function reorderCredentials(draggedId, targetId) {
    const draggedIdx = allCredentials.findIndex(c => c.id === draggedId);
    const targetIdx = allCredentials.findIndex(c => c.id === targetId);
    if (draggedIdx === -1 || targetIdx === -1) return;

    const [dragged] = allCredentials.splice(draggedIdx, 1);
    allCredentials.splice(targetIdx, 0, dragged);

    const keyword = document.getElementById('credential-search').value.toLowerCase();
    const displayList = keyword
        ? allCredentials.filter(c =>
            c.service.toLowerCase().includes(keyword) ||
            c.account.toLowerCase().includes(keyword) ||
            c.url.toLowerCase().includes(keyword)
        )
        : allCredentials;

    renderCredentials(displayList);
    await pywebview.api.reorder_credentials(allCredentials.map(c => c.id));
}

// ==================== 页签管理 ====================
async function loadTabs() {
    allTabs = await pywebview.api.get_tabs();
    if (!currentTabId && allTabs.length) {
        currentTabId = allTabs[0].id;
    }
    renderTabs();
}

function renderTabs() {
    const container = document.getElementById('command-tabs');
    container.innerHTML = allTabs.map(tab => {
        const count = allCommands.filter(c => c.tab_id === tab.id).length;
        return `
            <div class="tab-item ${tab.id === currentTabId ? 'active' : ''}"
                 data-tab-id="${tab.id}"
                 draggable="true"
                 onclick="selectTab('${tab.id}')"
                 ondragstart="onTabDragStart(event)"
                 ondragover="onTabDragOver(event)"
                 ondrop="onTabDrop(event)"
                 ondragend="onTabDragEnd(event)">
                <span>${escapeHtml(tab.name)}</span>
                <span class="tab-count">${count}</span>
            </div>
        `;
    }).join('');
}

function selectTab(tabId) {
    currentTabId = tabId;
    renderTabs();
    renderCommandsByTab();
}

function getTabCommandCount(tabId) {
    return allCommands.filter(c => c.tab_id === tabId).length;
}

// 页签拖拽排序
let draggedTabId = null;

function onTabDragStart(e) {
    draggedTabId = e.target.dataset.tabId;
    e.target.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
}

function onTabDragOver(e) {
    e.preventDefault();
    const target = e.target.closest('.tab-item');
    if (target && target.dataset.tabId !== draggedTabId) {
        target.classList.add('drag-over');
    }
}

function onTabDrop(e) {
    e.preventDefault();
    const target = e.target.closest('.tab-item');
    if (target && draggedTabId && target.dataset.tabId !== draggedTabId) {
        const targetId = target.dataset.tabId;
        reorderTabs(draggedTabId, targetId);
    }
    document.querySelectorAll('.tab-item').forEach(el => el.classList.remove('drag-over'));
}

function onTabDragEnd(e) {
    draggedTabId = null;
    document.querySelectorAll('.tab-item').forEach(el => {
        el.classList.remove('dragging', 'drag-over');
    });
}

async function reorderTabs(draggedId, targetId) {
    const draggedIdx = allTabs.findIndex(t => t.id === draggedId);
    const targetIdx = allTabs.findIndex(t => t.id === targetId);

    const [dragged] = allTabs.splice(draggedIdx, 1);
    allTabs.splice(targetIdx, 0, dragged);

    const newOrder = allTabs.map(t => t.id);
    await pywebview.api.reorder_tabs(newOrder);
    renderTabs();
}

// 页签管理弹窗
function showTabModal() {
    renderTabManageList();
    openModal('tab-modal');
}

function renderTabManageList() {
    const container = document.getElementById('tabs-manage-list');
    container.innerHTML = allTabs.map(tab => `
        <div class="tab-manage-item" data-tab-id="${tab.id}" draggable="true"
             ondragstart="onManageTabDragStart(event)"
             ondragover="onManageTabDragOver(event)"
             ondrop="onManageTabDrop(event)"
             ondragend="onManageTabDragEnd(event)">
            <span class="tab-drag-handle">☰</span>
            <div class="tab-manage-name">${escapeHtml(tab.name)}</div>
            <div class="tab-manage-actions">
                <button class="tab-manage-btn" onclick="editTabName('${tab.id}')" title="编辑">✏️</button>
                ${tab.id !== '0' ? `<button class="tab-manage-btn delete" onclick="deleteTab('${tab.id}')" title="删除">🗑</button>` : ''}
            </div>
        </div>
    `).join('');
}

// 管理列表拖拽
let draggedManageTabId = null;

function onManageTabDragStart(e) {
    draggedManageTabId = e.target.closest('.tab-manage-item').dataset.tabId;
    e.target.closest('.tab-manage-item').classList.add('dragging');
}

function onManageTabDragOver(e) {
    e.preventDefault();
    const target = e.target.closest('.tab-manage-item');
    if (target && target.dataset.tabId !== draggedManageTabId) {
        target.classList.add('drag-over');
    }
}

function onManageTabDrop(e) {
    e.preventDefault();
    const target = e.target.closest('.tab-manage-item');
    if (target && draggedManageTabId && target.dataset.tabId !== draggedManageTabId) {
        reorderTabs(draggedManageTabId, target.dataset.tabId);
        renderTabManageList();
    }
    document.querySelectorAll('.tab-manage-item').forEach(el => el.classList.remove('drag-over'));
}

function onManageTabDragEnd(e) {
    draggedManageTabId = null;
    document.querySelectorAll('.tab-manage-item').forEach(el => {
        el.classList.remove('dragging', 'drag-over');
    });
}

async function addTab() {
    const nameInput = document.getElementById('new-tab-name');
    const name = nameInput.value.trim();
    if (!name) {
        alert('请输入页签名称');
        return;
    }
    await pywebview.api.add_tab(name);
    nameInput.value = '';
    await loadTabs();
    renderTabManageList();
}

async function editTabName(tabId) {
    const tab = allTabs.find(t => t.id === tabId);
    if (!tab) return;

    const newName = prompt('输入新名称', tab.name);
    if (newName && newName.trim() && newName !== tab.name) {
        await pywebview.api.update_tab(tabId, newName.trim());
        await loadTabs();
        renderTabManageList();
    }
}

async function deleteTab(tabId) {
    if (confirm('删除页签后，其中的命令将移至"未分类"。确定删除？')) {
        await pywebview.api.delete_tab(tabId);
        if (currentTabId === tabId) {
            currentTabId = '0';
        }
        await loadTabs();
        await loadCommands();
        renderTabManageList();
    }
}

// ==================== 命令块管理 ====================
async function loadCommands() {
    allCommands = await pywebview.api.get_commands();
    renderTabs(); // 更新计数
    renderCommandsByTab();
}

function renderCommandsByTab() {
    const commands = currentTabId
        ? allCommands.filter(c => c.tab_id === currentTabId)
        : allCommands;
    renderCommands(commands);
}

function renderCommands(commands) {
    const container = document.getElementById('commands-list');
    if (!commands.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">⌨️</div>
                <div class="empty-state-text">当前页签暂无命令</div>
            </div>`;
        return;
    }

    container.innerHTML = commands.map(cmd => `
        <div class="command-card" data-cmd-id="${cmd.id}" draggable="true"
             ondragstart="onCommandDragStart(event)"
             ondragover="onCommandDragOver(event)"
             ondrop="onCommandDrop(event)"
             ondragend="onCommandDragEnd(event)">
            <div class="command-header">
                <div class="command-info">
                    <div class="command-title">${escapeHtml(cmd.title)}</div>
                    ${cmd.description ? `<div class="command-description">${escapeHtml(cmd.description)}</div>` : ''}
                </div>
                <div class="command-actions">
                    <button class="btn btn-sm btn-ghost" onclick="showMoveCommandModal('${cmd.id}')" title="移动">📁</button>
                    <button class="btn btn-sm btn-ghost" onclick="editCommand('${cmd.id}')">编辑</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteCommand('${cmd.id}')">删除</button>
                </div>
            </div>
            <div class="command-body">
                <pre>${escapeHtml(cmd.commands.join('\n'))}</pre>
                <button class="command-copy-btn" onclick="copyCommand(this, \`${escapeAttr(cmd.commands.join('\n'))}\`)" title="复制命令">📋</button>
            </div>
        </div>
    `).join('');
}

// 命令拖拽排序
let draggedCommandId = null;

function onCommandDragStart(e) {
    draggedCommandId = e.target.closest('.command-card').dataset.cmdId;
    e.target.closest('.command-card').classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
}

function onCommandDragOver(e) {
    e.preventDefault();
    const target = e.target.closest('.command-card');
    if (target && target.dataset.cmdId !== draggedCommandId) {
        target.classList.add('drag-over');
    }
}

async function onCommandDrop(e) {
    e.preventDefault();
    const target = e.target.closest('.command-card');
    if (target && draggedCommandId && target.dataset.cmdId !== draggedCommandId) {
        await reorderCommands(draggedCommandId, target.dataset.cmdId);
    }
    document.querySelectorAll('.command-card').forEach(el => el.classList.remove('drag-over'));
}

function onCommandDragEnd(e) {
    draggedCommandId = null;
    document.querySelectorAll('.command-card').forEach(el => {
        el.classList.remove('dragging', 'drag-over');
    });
}

async function reorderCommands(draggedId, targetId) {
    const currentCmds = allCommands.filter(c => c.tab_id === currentTabId);
    const draggedIdx = currentCmds.findIndex(c => c.id === draggedId);
    const targetIdx = currentCmds.findIndex(c => c.id === targetId);
    if (draggedIdx === -1 || targetIdx === -1) return;

    const [dragged] = currentCmds.splice(draggedIdx, 1);
    currentCmds.splice(targetIdx, 0, dragged);

    currentCmds.forEach((cmd, idx) => {
        cmd.order = idx;
    });

    allCommands.sort((a, b) => {
        if (a.tab_id === b.tab_id) {
            return (a.order || 0) - (b.order || 0);
        }
        return a.tab_id < b.tab_id ? -1 : 1;
    });

    renderCommands(currentCmds);
    await pywebview.api.reorder_commands(currentTabId, currentCmds.map(c => c.id));
}

function filterCommands() {
    const keyword = document.getElementById('command-search').value.toLowerCase();
    let commands = currentTabId
        ? allCommands.filter(c => c.tab_id === currentTabId)
        : allCommands;

    if (keyword) {
        commands = commands.filter(c =>
            c.title.toLowerCase().includes(keyword) ||
            c.description.toLowerCase().includes(keyword) ||
            c.commands.some(cmd => cmd.toLowerCase().includes(keyword))
        );
    }
    renderCommands(commands);
}

function showCommandModal(cmd = null) {
    document.getElementById('command-modal-title').textContent = cmd ? '编辑命令' : '添加命令';
    document.getElementById('command-id').value = cmd?.id || '';
    document.getElementById('command-tab-id').value = cmd?.tab_id || currentTabId || '0';
    document.getElementById('command-title').value = cmd?.title || '';
    document.getElementById('command-description').value = cmd?.description || '';
    document.getElementById('command-content').value = cmd?.commands?.join('\n') || '';

    // 填充页签选择
    const select = document.getElementById('command-tab-select');
    select.innerHTML = allTabs.map(tab =>
        `<option value="${tab.id}" ${tab.id === (cmd?.tab_id || currentTabId || '0') ? 'selected' : ''}>${escapeHtml(tab.name)}</option>`
    ).join('');

    openModal('command-modal');
}

async function editCommand(id) {
    const cmd = allCommands.find(c => c.id === id);
    if (cmd) showCommandModal(cmd);
}

async function saveCommand() {
    const id = document.getElementById('command-id').value;
    const title = document.getElementById('command-title').value.trim();
    const description = document.getElementById('command-description').value.trim();
    const tabId = document.getElementById('command-tab-select').value;
    const commands = document.getElementById('command-content').value.split('\n').filter(l => l.trim());

    if (!title || !commands.length) {
        alert('请填写标题和命令');
        return;
    }

    if (id) {
        await pywebview.api.update_command(id, title, description, commands, tabId, []);
    } else {
        await pywebview.api.add_command(title, description, commands, tabId, []);
    }
    closeModal('command-modal');
    await loadCommands();
}

async function deleteCommand(id) {
    if (confirm('确定删除此命令？')) {
        await pywebview.api.delete_command(id);
        await loadCommands();
    }
}

// 移动命令到页签
function showMoveCommandModal(cmdId) {
    const cmd = allCommands.find(c => c.id === cmdId);
    if (!cmd) return;

    document.getElementById('move-command-id').value = cmdId;
    const container = document.getElementById('move-tab-options');

    container.innerHTML = allTabs.map(tab => `
        <div class="move-tab-option ${tab.id === cmd.tab_id ? 'current' : ''}" onclick="moveCommandToTab('${cmdId}', '${tab.id}')">
            <span class="move-tab-icon">📁</span>
            <span class="move-tab-name">${escapeHtml(tab.name)}</span>
            ${tab.id === cmd.tab_id ? '<span class="move-tab-current">当前</span>' : ''}
        </div>
    `).join('');

    openModal('move-command-modal');
}

async function moveCommandToTab(cmdId, tabId) {
    await pywebview.api.move_command_to_tab(cmdId, tabId);
    closeModal('move-command-modal');
    await loadCommands();
}

// ==================== 批量导入 ====================
function showImportModal(type) {
    document.getElementById('import-type').value = type;
    document.getElementById('import-content').value = '';

    if (type === 'credentials') {
        document.getElementById('import-modal-title').textContent = '批量导入凭证';
        document.getElementById('import-hint').innerHTML = `
            支持格式：<br>
            1. <code>服务名 URL || 账号 || 密码</code><br>
            2. 多行格式（空行分隔）：<br>
            <code>服务名<br>账号：xxx<br>密码：xxx</code>
        `;
    } else {
        document.getElementById('import-modal-title').textContent = '批量导入命令块';
        document.getElementById('import-hint').innerHTML = `
            格式：以 <code># 注释</code> 或 <code>标题：</code> 开头作为块标题，<br>
            后续行作为命令，空行分隔不同命令块<br>
            <small>导入的命令将添加到当前页签</small>
        `;
    }
    openModal('import-modal');
}

async function doImport() {
    const type = document.getElementById('import-type').value;
    const content = document.getElementById('import-content').value.trim();

    if (!content) {
        alert('请粘贴要导入的内容');
        return;
    }

    let result;
    if (type === 'credentials') {
        result = await pywebview.api.import_credentials(content);
        loadCredentials();
    } else {
        result = await pywebview.api.import_commands(content);
        await loadCommands();
    }

    closeModal('import-modal');
    alert(`成功导入 ${result.imported} 条记录`);
}

// ==================== 节点转换 ====================
async function convertLinks() {
    const linksText = document.getElementById('links-input').value.trim();
    if (!linksText) {
        alert('请输入节点链接');
        return;
    }

    const result = await pywebview.api.convert_links(linksText);
    convertedNodes = result.nodes;

    const jsonOutput = JSON.stringify(result.nodes, null, 2);
    document.getElementById('yaml-output').value = jsonOutput;
    showErrors(result.errors);
}

async function fetchSubscription() {
    const url = document.getElementById('subscription-url').value.trim();
    if (!url) {
        alert('请输入订阅URL');
        return;
    }

    const result = await pywebview.api.fetch_subscription(url);
    convertedNodes = result.nodes;

    const jsonOutput = JSON.stringify(result.nodes, null, 2);
    document.getElementById('yaml-output').value = jsonOutput;
    showErrors(result.errors);
}

function showErrors(errors) {
    const container = document.getElementById('convert-errors');
    container.innerHTML = errors.map(e => `<div>⚠ ${escapeHtml(e)}</div>`).join('');
}

function copyYaml() {
    const content = document.getElementById('yaml-output').value;
    if (content) {
        navigator.clipboard.writeText(content);
        alert('已复制到剪贴板');
    }
}

async function saveConvertedNodes() {
    if (!convertedNodes.length) {
        alert('没有可保存的节点');
        return;
    }

    for (const node of convertedNodes) {
        await pywebview.api.save_node(
            node.name,
            node.type,
            node.server,
            node.port,
            '',
            JSON.stringify(node, null, 2)
        );
    }
    alert(`已保存 ${convertedNodes.length} 个节点`);
    loadNodes();
}

// ==================== 节点管理 ====================
async function loadNodes() {
    const nodes = await pywebview.api.get_nodes();
    const container = document.getElementById('nodes-list');

    if (!nodes.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🌐</div>
                <div class="empty-state-text">暂无保存的节点</div>
            </div>`;
        return;
    }

    container.innerHTML = nodes.map(node => `
        <div class="node-card">
            <div class="node-header">
                <span class="node-name">${escapeHtml(node.name)}</span>
                <div style="display:flex;gap:8px;align-items:center">
                    <span class="node-type">${escapeHtml(node.type)}</span>
                    <button class="btn btn-sm btn-danger" onclick="deleteNode('${node.id}')">删除</button>
                </div>
            </div>
            <div class="node-info">
                <span>🖥 ${escapeHtml(node.server)}</span>
                <span>🔌 ${node.port}</span>
            </div>
        </div>
    `).join('');
}

async function deleteNode(id) {
    if (confirm('确定删除此节点？')) {
        await pywebview.api.delete_node(id);
        loadNodes();
    }
}

// ==================== 工具函数 ====================
function openModal(id) {
    document.getElementById(id).classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}

function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}

function escapeAttr(text) {
    if (text === null || text === undefined) return '';
    return String(text).replace(/'/g, "\\'").replace(/"/g, '\\"').replace(/`/g, '\\`');
}

function copyField(btn, text) {
    navigator.clipboard.writeText(text);
    btn.classList.add('copied');
    setTimeout(() => btn.classList.remove('copied'), 1000);
}

function copyCommand(btn, text) {
    navigator.clipboard.writeText(text);
    btn.classList.add('copied');
    setTimeout(() => btn.classList.remove('copied'), 1000);
}
