# 牛牛待办 - 项目状态记忆

## 项目概述
牛牛待办是一个基于 pywebview 的桌面待办应用，采用 Python 后端 + HTML/CSS/JS 前端架构。

## Sprint 5: 成就系统 - 已完成 ✅

### 实现的功能

#### 后端 (services/todo_service.py)
- **成就定义** (行 982-1006): 17 个成就，分为 5 个类别
  - 任务达人系列: task_10, task_50, task_100, task_500
  - 专注大师系列: pomo_10, pomo_50, pomo_100, pomo_500
  - 连续打卡系列: streak_3, streak_7, streak_14, streak_30
  - 早起鸟儿系列: early_5, early_20, early_50
  - 夜猫子系列: night_5, night_20, night_50

- **等级系统** (行 1008-1013): 铜牌、银牌、金牌、钻石

- **核心方法**:
  - `_load_achievements()` / `_save_achievements()`: 数据持久化 (行 1015-1030)
  - `get_achievements()`: 获取所有成就及进度 (行 1032-1056)
  - `_calculate_progress()`: 计算各类成就进度 (行 1058-1086)
  - `_calculate_streak()`: 计算连续打卡天数 (行 1088-1117)
  - `check_achievements()`: 检查并解锁新成就 (行 1119-1143)

#### API 层 (api.py)
- `get_achievements()` (行 265-267)
- `check_achievements()` (行 269-271)

#### 前端 (web/app.js)
- 成就弹窗显示: `showAchievementModal()` (行 1570-1572)
- 成就加载渲染: `loadAchievements()` (行 1575-1615)
- 成就检查触发: `checkAndShowAchievements()` (行 1617-1625)
- 成就 Toast 动画: `showAchievementToast()` (行 1627-1647)
- 任务完成时成就检查: hook `toggleTaskStatus` (行 1650-1663)

#### 前端样式 (web/styles.css)
- 成就统计区域样式 (行 2259-2287)
- 成就卡片样式 (行 2288-2393)
- 成就解锁 Toast 样式 (行 2395-2452)

### 2024-12-14 修复的问题

1. **后端 streak 统计问题** (todo_service.py:1054)
   - 原问题: `get_achievements()` 返回的 streak 来自陈旧的持久化数据 `data["streak_data"]["current"]`
   - 修复: 改为使用实时计算的 `progress.get("streak", 0)`

2. **前端成就检查触发问题** (app.js:1650-1663)
   - 原问题: 代码尝试 hook 不存在的 `window.completeTask`
   - 修复: 改为 hook `toggleTaskStatus`，在任务从未完成变为完成时触发成就检查

3. **番茄钟完成后成就检查** (app.js:844)
   - 原问题: 番茄钟完成后没有检查成就
   - 修复: 在 `completePomodoro()` 末尾添加 `await checkAndShowAchievements()`

4. **成就 Toast z-index** (styles.css:2401)
   - 原问题: 成就 Toast 可能被其他弹窗遮挡 (z-index: 10000)
   - 修复: 将 z-index 提升到 10001

## 项目文件结构

```
todo_app/
├── main.py              # pywebview 主入口
├── api.py               # 前端 API 接口层
├── build.py             # 打包脚本
├── requirements.txt     # Python 依赖
├── services/
│   ├── __init__.py
│   └── todo_service.py  # 核心业务逻辑
├── web/
│   ├── index.html       # 前端页面
│   ├── app.js           # 前端逻辑
│   └── styles.css       # 样式
├── icons/               # 应用图标
└── tests/               # 单元测试
```

## 已实现的完整功能列表

1. **任务管理**: CRUD、状态切换、优先级、四象限
2. **子任务**: 添加、完成、删除、进度显示
3. **分类管理**: 自定义图标和颜色
4. **标签系统**: 多标签支持、按标签筛选
5. **重复任务**: 每日/每周/每月/每年重复
6. **番茄钟**: 计时、统计、图表
7. **多视图**: 列表、看板、日历、四象限
8. **便签悬浮窗**: 今日任务快捷查看
9. **工作总结**: 日报/周报/月报生成
10. **成就系统**: 17个成就、4个等级、解锁动画
11. **多主题**: 9种主题（6浅色+3深色）
12. **数据导入导出**: JSON 格式备份恢复
13. **键盘快捷键**: 全局快捷操作

## 技术栈

- **后端**: Python 3.x, pywebview
- **前端**: 原生 HTML/CSS/JS, uPlot (图表)
- **数据存储**: JSON 文件 (~/.todo_app/)
- **打包**: PyInstaller
