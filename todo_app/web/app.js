// ===== 状态管理 =====
const state = {
    tasks: [],
    categories: [],
    currentView: 'list',
    currentCategory: '',
    calendarDate: new Date(),
    editingTaskId: null,
    pomodoroTaskId: null,
    pomodoroRunning: false,
    pomodoroTime: 25 * 60,
    pomodoroInterval: null,
    // 便签状态
    stickyVisible: false,
    stickyMinimized: false,
    stickyOpacity: 1,
    stickyPosition: { x: 30, y: null }, // y=null 表示使用 bottom
    // 键盘导航
    selectedTaskIndex: -1,
    keyboardNavTasks: []
};

// ===== 工具函数 =====
function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function escapeAttr(text) {
    return escapeHtml(text).replace(/`/g, '&#096;');
}

// ===== 日期辅助函数 =====
function getLocalDateStr() {
    const now = new Date();
    const offset = now.getTimezoneOffset() * 60000;
    return new Date(now.getTime() - offset).toISOString().split('T')[0];
}

// ===== 初始化 =====
document.addEventListener('DOMContentLoaded', async () => {
    await waitForApi();
    initTheme();
    initViewSwitcher();
    await loadCategories();
    await loadTasks();
    updateStats();
    initDragDrop();
    initKeyboardShortcuts();
    initStickyNotes();
});

async function waitForApi() {
    while (!window.pywebview?.api) {
        await new Promise(r => setTimeout(r, 50));
    }
}

// ===== 主题系统 =====
const THEME_ICONS = {
    'light': '☀️', 'cute': '🐮', 'office': '📊',
    'neon-light': '🌊', 'forest': '🌲', 'sunset': '🌅',
    'dark': '🌙', 'neon': '🌃', 'cyberpunk': '🤖'
};

async function initTheme() {
    let savedTheme = 'cute';
    try {
        savedTheme = await pywebview.api.get_theme();
    } catch (e) {
        savedTheme = localStorage.getItem('theme') || 'cute';
    }
    setTheme(savedTheme, false);

    window.addEventListener('click', (e) => {
        const menu = document.getElementById('themeMenu');
        const btn = document.getElementById('themeToggleBtn');
        if (menu && btn && menu.classList.contains('active')) {
            if (!menu.contains(e.target) && !btn.contains(e.target)) {
                menu.classList.remove('active');
            }
        }
    });
}

function toggleThemeMenu() {
    document.getElementById('themeMenu').classList.toggle('active');
}

function selectTheme(theme) {
    setTheme(theme);
    document.getElementById('themeMenu').classList.remove('active');
}

function setTheme(theme, save = true) {
    document.documentElement.setAttribute('data-theme', theme);
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateThemeIcon(theme);
    updateThemeSelector(theme);
    if (save) {
        pywebview.api.save_theme(theme).catch(() => {});
    }
}

function updateThemeIcon(theme) {
    const iconEl = document.getElementById('currentThemeIcon');
    if (iconEl && THEME_ICONS[theme]) {
        iconEl.textContent = THEME_ICONS[theme];
    }
}

function updateThemeSelector(activeTheme) {
    document.querySelectorAll('.theme-item').forEach(opt => {
        opt.classList.toggle('active', opt.dataset.theme === activeTheme);
    });
}

// ===== 视图切换 =====
function initViewSwitcher() {
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const view = btn.dataset.view;
            switchView(view);
        });
    });
}

function switchView(view) {
    state.currentView = view;

    document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.view-btn[data-view="${view}"]`)?.classList.add('active');

    document.querySelectorAll('.view-container').forEach(v => v.classList.remove('active'));
    document.getElementById(`view-${view}`)?.classList.add('active');

    renderCurrentView();
}

function renderCurrentView() {
    switch (state.currentView) {
        case 'list': renderListView(); break;
        case 'kanban': renderKanbanView(); break;
        case 'calendar': renderCalendarView(); break;
        case 'quadrant': renderQuadrantView(); break;
    }
}

// ===== 数据加载 =====
async function loadCategories() {
    state.categories = await pywebview.api.get_categories();
    renderCategoriesList();
    renderCategorySelects();
}

async function loadTasks() {
    const status = document.getElementById('filter-status')?.value || '';
    const priority = document.getElementById('filter-priority')?.value || '';
    const category = document.getElementById('filter-category')?.value || '';
    const search = document.getElementById('search-input')?.value || '';

    state.tasks = await pywebview.api.get_tasks(status, category, priority, '', '', search);
    renderCurrentView();
    updateStats();
}

function handleSearch() {
    loadTasks();
}

async function updateStats() {
    const todayTasks = await pywebview.api.get_today_tasks();
    const completed = todayTasks.filter(t => t.status === 'completed').length;
    const pomodoroCount = await pywebview.api.get_today_pomodoro_count();

    document.getElementById('stat-today-completed').textContent = completed;
    document.getElementById('stat-today-pomodoro').textContent = pomodoroCount;
}

// ===== 分类渲染 =====
function renderCategoriesList() {
    const container = document.getElementById('categories-list');
    const taskCounts = {};
    state.tasks.forEach(t => {
        taskCounts[t.category_id] = (taskCounts[t.category_id] || 0) + 1;
    });

    container.innerHTML = `
        <div class="category-item ${!state.currentCategory ? 'active' : ''}"
             onclick="selectCategory('')">
            <div class="category-icon" style="background:#eee">📋</div>
            <span class="category-name">全部</span>
            <span class="category-count">${state.tasks.length}</span>
        </div>
    ` + state.categories.map(c => `
        <div class="category-item ${state.currentCategory === c.id ? 'active' : ''}"
             onclick="selectCategory('${escapeAttr(c.id)}')">
            <div class="category-icon" style="background:${escapeAttr(c.color)}">${escapeHtml(c.icon)}</div>
            <span class="category-name">${escapeHtml(c.name)}</span>
            <span class="category-count">${taskCounts[c.id] || 0}</span>
        </div>
    `).join('');
}

function renderCategorySelects() {
    const options = '<option value="">无分类</option>' +
        state.categories.map(c =>
            `<option value="${escapeAttr(c.id)}">${escapeHtml(c.icon)} ${escapeHtml(c.name)}</option>`
        ).join('');

    document.getElementById('task-category').innerHTML = options;
    document.getElementById('filter-category').innerHTML =
        '<option value="">全部分类</option>' +
        state.categories.map(c =>
            `<option value="${escapeAttr(c.id)}">${escapeHtml(c.icon)} ${escapeHtml(c.name)}</option>`
        ).join('');
}

function selectCategory(categoryId) {
    state.currentCategory = categoryId;
    document.getElementById('filter-category').value = categoryId;
    loadTasks();
}

// ===== 列表视图 =====
function renderListView() {
    const container = document.getElementById('task-groups');

    const groups = {
        'not_started': { title: '📝 未开始', tasks: [] },
        'in_progress': { title: '🚀 进行中', tasks: [] },
        'completed': { title: '✅ 已完成', tasks: [] }
    };

    state.tasks.forEach(t => {
        if (groups[t.status]) {
            groups[t.status].tasks.push(t);
        }
    });

    if (state.tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🐮</div>
                <p>还没有任务哞～</p>
                <button class="btn btn-primary" onclick="showTaskModal()">创建第一个任务</button>
            </div>
        `;
        return;
    }

    container.innerHTML = Object.entries(groups)
        .filter(([_, g]) => g.tasks.length > 0)
        .map(([status, group]) => `
            <div class="task-group">
                <div class="group-header">${group.title} (${group.tasks.length})</div>
                <div class="task-list">
                    ${group.tasks.map(t => renderTaskCard(t)).join('')}
                </div>
            </div>
        `).join('');
}

function renderTaskCard(task) {
    const category = state.categories.find(c => c.id === task.category_id);
    const isOverdue = task.due_date && task.due_date < getLocalDateStr() && task.status !== 'completed';

    return `
        <div class="task-card ${task.status === 'completed' ? 'completed' : ''}"
             data-id="${escapeAttr(task.id)}"
             data-priority="${escapeAttr(task.priority)}"
             onclick="showEditTaskModal('${escapeAttr(task.id)}')">
            <div class="task-checkbox" onclick="event.stopPropagation(); toggleTaskStatus('${escapeAttr(task.id)}')">
                ${task.status === 'completed' ? '✓' : ''}
            </div>
            <div class="task-content">
                <div class="task-title">${escapeHtml(task.title)}</div>
                <div class="task-meta">
                    ${category ? `<span style="color:${escapeAttr(category.color)}">${escapeHtml(category.icon)} ${escapeHtml(category.name)}</span>` : ''}
                    ${task.due_date ? `<span class="task-due ${isOverdue ? 'overdue' : ''}">📅 ${task.due_date}</span>` : ''}
                    ${task.pomodoro_count > 0 ? `<span>🍅 ${task.pomodoro_count}</span>` : ''}
                </div>
            </div>
            <div class="task-actions">
                <button class="btn-pomodoro" onclick="event.stopPropagation(); startPomodoro('${escapeAttr(task.id)}')" title="开始番茄钟">🍅</button>
            </div>
        </div>
    `;
}

async function toggleTaskStatus(taskId) {
    const task = state.tasks.find(t => t.id === taskId);
    if (!task) return;

    const newStatus = task.status === 'completed' ? 'not_started' : 'completed';
    await pywebview.api.update_task_status(taskId, newStatus);
    await loadTasks();
    showToast(newStatus === 'completed' ? '任务完成哞！' : '任务已恢复');
}

// ===== 看板视图 =====
function renderKanbanView() {
    const columns = {
        'not_started': document.getElementById('kanban-not-started'),
        'in_progress': document.getElementById('kanban-in-progress'),
        'completed': document.getElementById('kanban-completed')
    };

    const counts = { 'not_started': 0, 'in_progress': 0, 'completed': 0 };

    Object.values(columns).forEach(col => col.innerHTML = '');

    state.tasks.forEach(task => {
        if (columns[task.status]) {
            columns[task.status].innerHTML += renderKanbanTask(task);
            counts[task.status]++;
        }
    });

    document.getElementById('count-not-started').textContent = counts['not_started'];
    document.getElementById('count-in-progress').textContent = counts['in_progress'];
    document.getElementById('count-completed').textContent = counts['completed'];
}

function renderKanbanTask(task) {
    return `
        <div class="kanban-task"
             data-id="${escapeAttr(task.id)}"
             data-priority="${escapeAttr(task.priority)}"
             draggable="true"
             onclick="showEditTaskModal('${escapeAttr(task.id)}')">
            <div class="task-title">${escapeHtml(task.title)}</div>
            ${task.due_date ? `<div class="task-meta"><span class="task-due">📅 ${task.due_date}</span></div>` : ''}
        </div>
    `;
}

// ===== 日历视图 =====
function renderCalendarView() {
    const year = state.calendarDate.getFullYear();
    const month = state.calendarDate.getMonth();

    document.getElementById('calendar-title').textContent = `${year}年${month + 1}月`;

    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDay = firstDay.getDay();
    const daysInMonth = lastDay.getDate();

    const today = getLocalDateStr();

    // 获取本月任务
    const startDate = `${year}-${String(month + 1).padStart(2, '0')}-01`;
    const endDate = `${year}-${String(month + 1).padStart(2, '0')}-${daysInMonth}`;
    const tasksByDate = {};
    state.tasks.forEach(t => {
        if (t.due_date && t.due_date >= startDate && t.due_date <= endDate) {
            if (!tasksByDate[t.due_date]) tasksByDate[t.due_date] = [];
            tasksByDate[t.due_date].push(t);
        }
    });

    const days = ['日', '一', '二', '三', '四', '五', '六'];
    let html = days.map(d => `<div class="calendar-day-header">${d}</div>`).join('');

    // 上月填充
    const prevMonthDays = new Date(year, month, 0).getDate();
    for (let i = startDay - 1; i >= 0; i--) {
        html += `<div class="calendar-day other-month"><div class="day-number">${prevMonthDays - i}</div></div>`;
    }

    // 本月
    for (let day = 1; day <= daysInMonth; day++) {
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const isToday = dateStr === today;
        const dayTasks = tasksByDate[dateStr] || [];

        html += `
            <div class="calendar-day ${isToday ? 'today' : ''}"
                 onclick="showDayTasks('${dateStr}')">
                <div class="day-number">${day}</div>
                <div class="task-dots">
                    ${dayTasks.slice(0, 4).map(t => `<div class="task-dot ${t.priority}"></div>`).join('')}
                </div>
            </div>
        `;
    }

    // 下月填充
    const remaining = 42 - (startDay + daysInMonth);
    for (let i = 1; i <= remaining; i++) {
        html += `<div class="calendar-day other-month"><div class="day-number">${i}</div></div>`;
    }

    document.getElementById('calendar-grid').innerHTML = html;
}

function prevMonth() {
    state.calendarDate.setMonth(state.calendarDate.getMonth() - 1);
    renderCalendarView();
}

function nextMonth() {
    state.calendarDate.setMonth(state.calendarDate.getMonth() + 1);
    renderCalendarView();
}

function showDayTasks(dateStr) {
    // 简化：筛选该日期任务
    document.getElementById('filter-status').value = '';
    state.tasks = state.tasks.filter(t => t.due_date === dateStr);
    switchView('list');
    loadTasks(); // 重新加载以显示筛选结果
}

// ===== 四象限视图 =====
function renderQuadrantView() {
    const quadrants = {
        'q1': document.getElementById('quadrant-q1'),
        'q2': document.getElementById('quadrant-q2'),
        'q3': document.getElementById('quadrant-q3'),
        'q4': document.getElementById('quadrant-q4')
    };

    Object.values(quadrants).forEach(q => q.innerHTML = '');

    state.tasks.forEach(task => {
        if (task.quadrant && quadrants[task.quadrant]) {
            quadrants[task.quadrant].innerHTML += `
                <div class="quadrant-task"
                     onclick="showEditTaskModal('${escapeAttr(task.id)}')">
                    ${escapeHtml(task.title)}
                </div>
            `;
        }
    });

    // 显示未分配的任务提示
    const unassigned = state.tasks.filter(t => !t.quadrant).length;
    if (unassigned > 0) {
        showToast(`有 ${unassigned} 个任务未分配象限`, true);
    }
}

// ===== 拖拽功能 =====
function initDragDrop() {
    document.addEventListener('dragstart', (e) => {
        if (e.target.classList.contains('kanban-task')) {
            e.target.classList.add('dragging');
            e.dataTransfer.setData('text/plain', e.target.dataset.id);
        }
    });

    document.addEventListener('dragend', (e) => {
        if (e.target.classList.contains('kanban-task')) {
            e.target.classList.remove('dragging');
        }
    });

    document.querySelectorAll('.column-tasks').forEach(column => {
        column.addEventListener('dragover', (e) => {
            e.preventDefault();
            column.classList.add('drag-over');
        });

        column.addEventListener('dragleave', () => {
            column.classList.remove('drag-over');
        });

        column.addEventListener('drop', async (e) => {
            e.preventDefault();
            column.classList.remove('drag-over');

            const taskId = e.dataTransfer.getData('text/plain');
            const newStatus = column.parentElement.dataset.status;

            await pywebview.api.update_task_status(taskId, newStatus);
            await loadTasks();
            showToast('任务状态已更新哞！');
        });
    });
}

// ===== 任务弹窗 =====
function showTaskModal() {
    state.editingTaskId = null;
    document.getElementById('task-modal-title').textContent = '新建任务';
    document.getElementById('task-id').value = '';
    document.getElementById('task-title').value = '';
    document.getElementById('task-description').value = '';
    document.getElementById('task-priority').value = 'medium';
    document.getElementById('task-due-date').value = '';
    document.getElementById('task-category').value = '';
    document.getElementById('task-quadrant').value = '';
    document.getElementById('btn-delete-task').style.display = 'none';
    openModal('task-modal');
    document.getElementById('task-title').focus();
}

function showEditTaskModal(taskId) {
    const task = state.tasks.find(t => t.id === taskId);
    if (!task) return;

    state.editingTaskId = taskId;
    document.getElementById('task-modal-title').textContent = '编辑任务';
    document.getElementById('task-id').value = task.id;
    document.getElementById('task-title').value = task.title;
    document.getElementById('task-description').value = task.description || '';
    document.getElementById('task-priority').value = task.priority;
    document.getElementById('task-due-date').value = task.due_date || '';
    document.getElementById('task-category').value = task.category_id || '';
    document.getElementById('task-quadrant').value = task.quadrant || '';
    document.getElementById('btn-delete-task').style.display = 'block';
    openModal('task-modal');
}

async function saveTask() {
    const title = document.getElementById('task-title').value.trim();
    const description = document.getElementById('task-description').value.trim();
    const priority = document.getElementById('task-priority').value;
    const dueDate = document.getElementById('task-due-date').value;
    const categoryId = document.getElementById('task-category').value;
    const quadrant = document.getElementById('task-quadrant').value;

    if (!title) {
        showToast('请输入任务标题哞～', true);
        return;
    }

    try {
        if (state.editingTaskId) {
            await pywebview.api.update_task(state.editingTaskId, {
                title, description, priority, due_date: dueDate,
                category_id: categoryId, quadrant
            });
            showToast('任务已更新哞！');
        } else {
            await pywebview.api.add_task(title, description, priority, categoryId, dueDate, [], quadrant);
            showToast('任务创建成功哞！');
        }

        closeModal('task-modal');
        await loadTasks();
    } catch (e) {
        showToast('保存失败：' + e, true);
    }
}

async function deleteCurrentTask() {
    if (!state.editingTaskId) return;
    if (!confirm('确定要删除这个任务吗？')) return;

    await pywebview.api.delete_task(state.editingTaskId);
    closeModal('task-modal');
    await loadTasks();
    showToast('任务已删除');
}

// ===== 分类弹窗 =====
const EMOJI_OPTIONS = ['💼', '📚', '🏠', '🎮', '🏃', '🛒', '💡', '🎯', '📌', '⭐'];
const COLOR_OPTIONS = ['#FFB347', '#87CEEB', '#B5EAD7', '#C7CEEA', '#E0BBE4', '#FFD93D', '#F59E0B', '#3B82F6', '#10B981', '#6B7280'];

let selectedCategoryEmoji = EMOJI_OPTIONS[0];
let selectedCategoryColor = COLOR_OPTIONS[0];

function showCategoryModal() {
    document.getElementById('category-name').value = '';
    selectedCategoryEmoji = EMOJI_OPTIONS[0];
    selectedCategoryColor = COLOR_OPTIONS[0];

    document.getElementById('category-emoji-picker').innerHTML = EMOJI_OPTIONS.map(e =>
        `<span class="emoji-item ${e === selectedCategoryEmoji ? 'selected' : ''}"
               data-emoji="${e}" onclick="selectCategoryEmoji('${e}')">${e}</span>`
    ).join('');

    document.getElementById('category-color-picker').innerHTML = COLOR_OPTIONS.map(c =>
        `<span class="color-item ${c === selectedCategoryColor ? 'selected' : ''}"
               style="background:${c}" data-color="${c}" onclick="selectCategoryColor('${c}')"></span>`
    ).join('');

    openModal('category-modal');
}

function selectCategoryEmoji(emoji) {
    selectedCategoryEmoji = emoji;
    document.querySelectorAll('#category-emoji-picker .emoji-item').forEach(el => {
        el.classList.toggle('selected', el.dataset.emoji === emoji);
    });
}

function selectCategoryColor(color) {
    selectedCategoryColor = color;
    document.querySelectorAll('#category-color-picker .color-item').forEach(el => {
        el.classList.toggle('selected', el.dataset.color === color);
    });
}

async function saveCategory() {
    const name = document.getElementById('category-name').value.trim();
    if (!name) {
        showToast('请输入分类名称哞～', true);
        return;
    }

    await pywebview.api.add_category(name, selectedCategoryEmoji, selectedCategoryColor);
    closeModal('category-modal');
    await loadCategories();
    showToast('分类创建成功哞！');
}

// ===== 番茄钟 =====
function startPomodoro(taskId) {
    const task = state.tasks.find(t => t.id === taskId);
    if (!task) return;

    // 清除可能正在运行的旧定时器
    if (state.pomodoroInterval) clearInterval(state.pomodoroInterval);
    state.pomodoroTaskId = taskId;
    state.pomodoroTime = 25 * 60;
    state.pomodoroRunning = false;

    document.getElementById('pomodoro-task-title').textContent = task.title;
    updatePomodoroDisplay();
    document.getElementById('pomodoro-widget').classList.remove('hidden');

    pywebview.api.start_pomodoro(taskId, 25);
}

function togglePomodoro() {
    if (state.pomodoroRunning) {
        clearInterval(state.pomodoroInterval);
        state.pomodoroRunning = false;
        document.getElementById('btn-pomodoro-toggle').textContent = '继续';
    } else {
        state.pomodoroRunning = true;
        document.getElementById('btn-pomodoro-toggle').textContent = '暂停';
        state.pomodoroInterval = setInterval(() => {
            state.pomodoroTime--;
            updatePomodoroDisplay();

            if (state.pomodoroTime <= 0) {
                completePomodoro();
            }
        }, 1000);
    }
}

function resetPomodoro() {
    clearInterval(state.pomodoroInterval);
    state.pomodoroTime = 25 * 60;
    state.pomodoroRunning = false;
    document.getElementById('btn-pomodoro-toggle').textContent = '开始';
    updatePomodoroDisplay();
}

async function completePomodoro() {
    clearInterval(state.pomodoroInterval);
    state.pomodoroRunning = false;

    // 这里简化处理，实际应该调用 complete_pomodoro API
    showToast('🍅 番茄钟完成！休息一下吧哞～');
    closePomodoroWidget();
    await updateStats();
}

function closePomodoroWidget() {
    clearInterval(state.pomodoroInterval);
    document.getElementById('pomodoro-widget').classList.add('hidden');
    state.pomodoroRunning = false;
}

function updatePomodoroDisplay() {
    const minutes = Math.floor(state.pomodoroTime / 60);
    const seconds = state.pomodoroTime % 60;
    document.getElementById('pomodoro-time').textContent =
        `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    // 更新进度环
    const progress = document.getElementById('pomodoro-progress');
    const total = 25 * 60;
    const offset = 283 * (1 - state.pomodoroTime / total);
    progress.style.strokeDashoffset = offset;
}

// ===== 键盘快捷键 =====
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // 忽略输入框中的按键
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') {
            return;
        }

        // 如果有弹窗打开，只处理 Escape
        if (document.querySelector('.modal.show')) {
            if (e.key === 'Escape') {
                document.querySelectorAll('.modal.show').forEach(m => m.classList.remove('show'));
            }
            return;
        }

        switch (e.key.toLowerCase()) {
            case 'n':
                e.preventDefault();
                showTaskModal();
                break;
            case 'e':
                e.preventDefault();
                editSelectedTask();
                break;
            case 'p':
                e.preventDefault();
                startPomodoroForSelected();
                break;
            case 's':
                e.preventDefault();
                toggleStickyNotes();
                break;
            case '1':
                e.preventDefault();
                switchView('list');
                break;
            case '2':
                e.preventDefault();
                switchView('kanban');
                break;
            case '3':
                e.preventDefault();
                switchView('calendar');
                break;
            case '4':
                e.preventDefault();
                switchView('quadrant');
                break;
            case '/':
                e.preventDefault();
                document.getElementById('search-input').focus();
                break;
            case 'arrowup':
                e.preventDefault();
                navigateTask(-1);
                break;
            case 'arrowdown':
                e.preventDefault();
                navigateTask(1);
                break;
            case ' ':
                e.preventDefault();
                toggleSelectedTaskStatus();
                break;
            case 'escape':
                clearTaskSelection();
                break;
        }
    });
}

// 键盘导航：选择任务
function navigateTask(direction) {
    updateKeyboardNavTasks();
    if (state.keyboardNavTasks.length === 0) return;

    state.selectedTaskIndex += direction;
    if (state.selectedTaskIndex < 0) state.selectedTaskIndex = state.keyboardNavTasks.length - 1;
    if (state.selectedTaskIndex >= state.keyboardNavTasks.length) state.selectedTaskIndex = 0;

    highlightSelectedTask();
}

function updateKeyboardNavTasks() {
    if (state.currentView === 'list') {
        state.keyboardNavTasks = Array.from(document.querySelectorAll('.task-card'));
    } else if (state.currentView === 'kanban') {
        state.keyboardNavTasks = Array.from(document.querySelectorAll('.kanban-task'));
    } else {
        state.keyboardNavTasks = [];
    }
}

function highlightSelectedTask() {
    document.querySelectorAll('.keyboard-selected').forEach(el => el.classList.remove('keyboard-selected'));
    if (state.selectedTaskIndex >= 0 && state.selectedTaskIndex < state.keyboardNavTasks.length) {
        const el = state.keyboardNavTasks[state.selectedTaskIndex];
        el.classList.add('keyboard-selected');
        el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

function getSelectedTaskId() {
    if (state.selectedTaskIndex < 0 || state.selectedTaskIndex >= state.keyboardNavTasks.length) return null;
    return state.keyboardNavTasks[state.selectedTaskIndex]?.dataset?.id;
}

function clearTaskSelection() {
    state.selectedTaskIndex = -1;
    document.querySelectorAll('.keyboard-selected').forEach(el => el.classList.remove('keyboard-selected'));
}

function editSelectedTask() {
    const taskId = getSelectedTaskId();
    if (taskId) {
        showEditTaskModal(taskId);
    }
}

function startPomodoroForSelected() {
    const taskId = getSelectedTaskId();
    if (taskId) {
        startPomodoro(taskId);
    }
}

async function toggleSelectedTaskStatus() {
    const taskId = getSelectedTaskId();
    if (taskId) {
        await toggleTaskStatus(taskId);
        updateKeyboardNavTasks();
        highlightSelectedTask();
    }
}

// ===== 便签悬浮窗 =====
function initStickyNotes() {
    const sticky = document.getElementById('sticky-notes');
    const handle = document.getElementById('sticky-drag-handle');

    // 加载保存的便签设置
    loadStickySettings();

    let isDragging = false;
    let startX, startY, startLeft, startBottom;

    handle.addEventListener('mousedown', (e) => {
        if (e.target.classList.contains('sticky-btn')) return;
        isDragging = true;
        sticky.classList.add('dragging');

        const rect = sticky.getBoundingClientRect();
        startX = e.clientX;
        startY = e.clientY;
        startLeft = rect.left;
        startBottom = window.innerHeight - rect.bottom;

        e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;

        const dx = e.clientX - startX;
        const dy = e.clientY - startY;

        let newLeft = startLeft + dx;
        let newBottom = startBottom - dy;

        // 边界限制
        newLeft = Math.max(0, Math.min(newLeft, window.innerWidth - sticky.offsetWidth));
        newBottom = Math.max(0, Math.min(newBottom, window.innerHeight - sticky.offsetHeight));

        sticky.style.left = newLeft + 'px';
        sticky.style.bottom = newBottom + 'px';
        sticky.style.right = 'auto';
        sticky.style.top = 'auto';

        state.stickyPosition = { x: newLeft, y: newBottom };
    });

    document.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
            sticky.classList.remove('dragging');
            saveStickySettings();
        }
    });
}

async function loadStickySettings() {
    try {
        const settings = await pywebview.api.get_settings();
        state.stickyVisible = settings.sticky_visible || false;
        state.stickyOpacity = settings.sticky_opacity || 1;
        state.stickyPosition = {
            x: settings.sticky_position_x || 30,
            y: settings.sticky_position_y || 30
        };

        const sticky = document.getElementById('sticky-notes');
        if (state.stickyVisible) {
            sticky.classList.remove('hidden');
            sticky.style.opacity = state.stickyOpacity;
            sticky.style.left = state.stickyPosition.x + 'px';
            sticky.style.bottom = state.stickyPosition.y + 'px';
            renderStickyTasks();
        }
    } catch (e) {
        // 默认值已在 state 中设置
    }
}

async function saveStickySettings() {
    try {
        await pywebview.api.update_settings({
            sticky_visible: state.stickyVisible,
            sticky_opacity: state.stickyOpacity,
            sticky_position_x: Math.round(state.stickyPosition.x),
            sticky_position_y: Math.round(state.stickyPosition.y)
        });
    } catch (e) {
        // 忽略保存错误
    }
}

function toggleStickyNotes() {
    const sticky = document.getElementById('sticky-notes');
    state.stickyVisible = !state.stickyVisible;

    if (state.stickyVisible) {
        sticky.classList.remove('hidden');
        sticky.style.opacity = state.stickyOpacity;
        renderStickyTasks();
    } else {
        sticky.classList.add('hidden');
    }
    saveStickySettings();
}

function closeStickyNotes() {
    state.stickyVisible = false;
    document.getElementById('sticky-notes').classList.add('hidden');
    saveStickySettings();
}

function toggleStickyMinimize() {
    const sticky = document.getElementById('sticky-notes');
    state.stickyMinimized = !state.stickyMinimized;
    sticky.classList.toggle('minimized', state.stickyMinimized);
}

function adjustStickyOpacity(delta) {
    state.stickyOpacity = Math.max(0.3, Math.min(1, state.stickyOpacity + delta));
    document.getElementById('sticky-notes').style.opacity = state.stickyOpacity;
}

async function renderStickyTasks() {
    const container = document.getElementById('sticky-tasks');
    let todayTasks = [];

    try {
        todayTasks = await pywebview.api.get_today_tasks();
    } catch (e) {
        todayTasks = state.tasks.filter(t => {
            const today = getLocalDateStr();
            return t.due_date === today || t.status === 'in_progress';
        });
    }

    if (todayTasks.length === 0) {
        container.innerHTML = `
            <div class="sticky-empty">
                <div class="sticky-empty-icon">🐄</div>
                <div>今天没有任务哞～</div>
            </div>
        `;
        document.getElementById('sticky-stat-done').textContent = '0';
        document.getElementById('sticky-stat-total').textContent = '0';
        return;
    }

    const completed = todayTasks.filter(t => t.status === 'completed').length;
    document.getElementById('sticky-stat-done').textContent = completed;
    document.getElementById('sticky-stat-total').textContent = todayTasks.length;

    container.innerHTML = todayTasks.map(task => `
        <div class="sticky-task ${task.status === 'completed' ? 'completed' : ''}"
             data-id="${escapeAttr(task.id)}"
             data-priority="${escapeAttr(task.priority)}"
             onclick="toggleTaskFromSticky('${escapeAttr(task.id)}')">
            <div class="sticky-task-checkbox">${task.status === 'completed' ? '✓' : ''}</div>
            <span class="sticky-task-title">${escapeHtml(task.title)}</span>
        </div>
    `).join('');
}

async function toggleTaskFromSticky(taskId) {
    await toggleTaskStatus(taskId);
    renderStickyTasks();
}

// ===== 工作总结 =====
let currentSummaryPeriod = 'day';

function showSummaryModal() {
    openModal('summary-modal');
    switchSummaryTab('day');
}

function switchSummaryTab(period) {
    currentSummaryPeriod = period;
    document.querySelectorAll('.summary-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.period === period);
    });
    loadSummaryData(period);
}

async function loadSummaryData(period) {
    const { startDate, endDate, periodName } = getDateRange(period);

    try {
        const stats = await pywebview.api.get_stats(startDate, endDate);
        const tasks = await pywebview.api.get_tasks_by_date_range(startDate, endDate);

        // 更新统计卡片
        document.getElementById('summary-completed').textContent = stats.completed_tasks || 0;
        document.getElementById('summary-pomodoros').textContent = stats.total_pomodoros || 0;
        document.getElementById('summary-hours').textContent = ((stats.total_pomodoros || 0) * 25 / 60).toFixed(1);

        const total = stats.total_tasks || 0;
        const completed = stats.completed_tasks || 0;
        const rate = total > 0 ? Math.round(completed / total * 100) : 0;
        document.getElementById('summary-rate').textContent = rate + '%';

        // 渲染任务列表
        renderSummaryTasks(tasks);

        // 生成文字总结
        generateSummaryText(periodName, stats, tasks);
    } catch (e) {
        console.error('加载总结数据失败:', e);
    }
}

function getDateRange(period) {
    const now = new Date();
    const today = getLocalDateStr();
    let startDate, endDate, periodName;

    if (period === 'day') {
        startDate = endDate = today;
        periodName = '今日';
    } else if (period === 'week') {
        const dayOfWeek = now.getDay();
        const monday = new Date(now);
        monday.setDate(now.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1));
        startDate = monday.toISOString().split('T')[0];
        endDate = today;
        periodName = '本周';
    } else {
        const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
        startDate = firstDay.toISOString().split('T')[0];
        endDate = today;
        periodName = '本月';
    }

    return { startDate, endDate, periodName };
}

function renderSummaryTasks(tasks) {
    const container = document.getElementById('summary-task-list');

    if (tasks.length === 0) {
        container.innerHTML = '<div class="summary-empty">暂无任务数据</div>';
        return;
    }

    container.innerHTML = tasks.map(task => `
        <div class="summary-task-item">
            <div class="task-status ${task.status === 'completed' ? 'completed' : 'incomplete'}">
                ${task.status === 'completed' ? '✓' : ''}
            </div>
            <span class="task-title">${escapeHtml(task.title)}</span>
            ${task.pomodoro_count > 0 ? `<span class="task-pomodoro">🍅 ${task.pomodoro_count}</span>` : ''}
        </div>
    `).join('');
}

function generateSummaryText(periodName, stats, tasks) {
    const completed = stats.completed_tasks || 0;
    const total = stats.total_tasks || 0;
    const pomodoros = stats.total_pomodoros || 0;
    const hours = (pomodoros * 25 / 60).toFixed(1);

    const completedTasks = tasks.filter(t => t.status === 'completed');
    const inProgressTasks = tasks.filter(t => t.status === 'in_progress');

    let text = `📊 ${periodName}工作总结\n`;
    text += `━━━━━━━━━━━━━━━━━━\n\n`;

    text += `📈 数据概览\n`;
    text += `• 完成任务: ${completed}/${total} 项\n`;
    text += `• 番茄数量: ${pomodoros} 个\n`;
    text += `• 专注时长: ${hours} 小时\n\n`;

    if (completedTasks.length > 0) {
        text += `✅ 已完成任务\n`;
        completedTasks.forEach(t => {
            text += `• ${t.title}`;
            if (t.pomodoro_count > 0) text += ` (🍅${t.pomodoro_count})`;
            text += '\n';
        });
        text += '\n';
    }

    if (inProgressTasks.length > 0) {
        text += `🚀 进行中任务\n`;
        inProgressTasks.forEach(t => {
            text += `• ${t.title}\n`;
        });
        text += '\n';
    }

    text += `━━━━━━━━━━━━━━━━━━\n`;
    text += `牛牛待办 · ${new Date().toLocaleDateString('zh-CN')}`;

    document.getElementById('summary-text').value = text;
}

async function copySummary() {
    const text = document.getElementById('summary-text').value;
    try {
        await navigator.clipboard.writeText(text);
        showToast('总结已复制到剪贴板哞！');
    } catch (e) {
        // 降级方案
        const textarea = document.getElementById('summary-text');
        textarea.select();
        document.execCommand('copy');
        showToast('总结已复制哞！');
    }
}

// ===== 设置 =====
async function showSettingsModal() {
    await loadSettingsData();
    openModal('settings-modal');
}

async function loadSettingsData() {
    try {
        const settings = await pywebview.api.get_settings();
        document.getElementById('settings-pomodoro-work').value = settings.pomodoro_work || 25;
        document.getElementById('settings-pomodoro-break').value = settings.pomodoro_break || 5;
        document.getElementById('settings-pomodoro-long-break').value = settings.pomodoro_long_break || 15;

        const dataStats = await pywebview.api.get_data_stats();
        document.getElementById('data-stat-tasks').textContent = dataStats.tasks || 0;
        document.getElementById('data-stat-categories').textContent = dataStats.categories || 0;
        document.getElementById('data-stat-pomodoros').textContent = dataStats.pomodoros || 0;
    } catch (e) {
        console.error('加载设置失败:', e);
    }
}

async function saveSettings() {
    const pomodoroWork = parseInt(document.getElementById('settings-pomodoro-work').value) || 25;
    const pomodoroBreak = parseInt(document.getElementById('settings-pomodoro-break').value) || 5;
    const pomodoroLongBreak = parseInt(document.getElementById('settings-pomodoro-long-break').value) || 15;

    try {
        await pywebview.api.update_settings({
            pomodoro_work: pomodoroWork,
            pomodoro_break: pomodoroBreak,
            pomodoro_long_break: pomodoroLongBreak
        });
        closeModal('settings-modal');
        showToast('设置已保存哞！');
    } catch (e) {
        showToast('保存失败：' + e, true);
    }
}

async function exportData() {
    try {
        const data = await pywebview.api.export_data();
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `牛牛待办_备份_${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
        showToast('数据已导出哞！');
    } catch (e) {
        showToast('导出失败：' + e, true);
    }
}

function handleImportFile(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
        try {
            const data = JSON.parse(e.target.result);
            if (!confirm('导入数据将覆盖现有数据，确定继续吗？')) {
                return;
            }
            const result = await pywebview.api.import_data(data);
            if (result.success) {
                showToast('数据导入成功哞！正在刷新...');
                setTimeout(() => location.reload(), 1000);
            } else {
                showToast('导入失败：' + (result.error || '未知错误'), true);
            }
        } catch (e) {
            showToast('文件格式错误：' + e, true);
        }
    };
    reader.readAsText(file);
    event.target.value = '';
}

// ===== 弹窗 =====
function openModal(id) {
    document.getElementById(id).classList.add('show');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('show');
}

// ===== Toast =====
function showToast(msg, isError = false) {
    const toast = document.getElementById('toast');
    const msgEl = document.getElementById('toast-message');
    const iconEl = toast.querySelector('.toast-icon');

    msgEl.textContent = msg;
    iconEl.textContent = isError ? '🐮' : '🐄';
    toast.className = 'toast' + (isError ? ' error' : '');

    setTimeout(() => toast.classList.add('hidden'), 2500);
}
