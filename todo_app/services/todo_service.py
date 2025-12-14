"""
Todo Service - 待办任务核心业务逻辑
"""
import json
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any


def generate_unique_id(prefix: str = "") -> str:
    """生成唯一ID（使用UUID避免碰撞）"""
    uid = uuid.uuid4().hex[:16]
    return f"{prefix}_{uid}" if prefix else uid


@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    status: str = "not_started"  # not_started | in_progress | completed
    priority: str = "medium"     # urgent | high | medium | low
    quadrant: str = ""           # q1 | q2 | q3 | q4 (四象限)
    category_id: str = ""
    due_date: str = ""           # YYYY-MM-DD
    tags: List[str] = field(default_factory=list)
    created_at: str = ""
    completed_at: str = ""
    pomodoro_count: int = 0
    order: int = 0


@dataclass
class Category:
    id: str
    name: str
    icon: str = "📁"
    color: str = "#C7CEEA"
    order: int = 0


@dataclass
class PomodoroRecord:
    id: str
    task_id: str
    started_at: str
    ended_at: str = ""
    duration: int = 25
    completed: bool = False


@dataclass
class Settings:
    pomodoro_work: int = 25
    pomodoro_break: int = 5
    pomodoro_long_break: int = 15
    theme: str = "cute"
    default_view: str = "list"  # list | kanban | calendar | quadrant
    # 便签设置
    sticky_visible: bool = False
    sticky_opacity: float = 1.0
    sticky_position_x: int = 30
    sticky_position_y: int = 30


# 常量
VALID_STATUSES = {"not_started", "in_progress", "completed"}
VALID_PRIORITIES = {"urgent", "high", "medium", "low"}
VALID_QUADRANTS = {"", "q1", "q2", "q3", "q4"}
PRIORITY_COLORS = {
    "urgent": "#E07A5F",  # 红色
    "high": "#3B82F6",    # 蓝色
    "medium": "#F59E0B",  # 橙色
    "low": "#9CA3AF"      # 灰色
}


class TodoService:
    def __init__(self, data_dir: str = ""):
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = Path.home() / ".todo_app"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.tasks_file = self.data_dir / "tasks.json"
        self.categories_file = self.data_dir / "categories.json"
        self.pomodoros_file = self.data_dir / "pomodoros.json"
        self.settings_file = self.data_dir / "settings.json"

        self.tasks: List[Task] = []
        self.categories: List[Category] = []
        self.pomodoros: List[PomodoroRecord] = []
        self.settings: Settings = Settings()

        self._load_all()

    # ===== 文件操作 =====
    def _load_json(self, file: Path) -> List[Dict]:
        if not file.exists():
            return []
        try:
            return json.loads(file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            return []

    def _save_json(self, file: Path, data: List):
        payload = json.dumps(
            [asdict(d) if hasattr(d, '__dataclass_fields__') else d for d in data],
            ensure_ascii=False, indent=2
        )
        tmp_file = file.with_suffix(file.suffix + ".tmp")
        tmp_file.write_text(payload, encoding="utf-8")
        tmp_file.replace(file)

    def _load_all(self):
        # 加载任务
        tasks_data = self._load_json(self.tasks_file)
        self.tasks = [Task(**t) for t in tasks_data]

        # 加载分类
        categories_data = self._load_json(self.categories_file)
        if categories_data:
            self.categories = [Category(**c) for c in categories_data]
        else:
            self._init_default_categories()

        # 加载番茄记录
        pomodoros_data = self._load_json(self.pomodoros_file)
        self.pomodoros = [PomodoroRecord(**p) for p in pomodoros_data]

        # 加载设置
        if self.settings_file.exists():
            try:
                settings_data = json.loads(self.settings_file.read_text(encoding="utf-8"))
                self.settings = Settings(**settings_data)
            except (json.JSONDecodeError, IOError):
                self.settings = Settings()

    def _init_default_categories(self):
        defaults = [
            Category(id=generate_unique_id("cat"), name="工作", icon="💼", color="#3B82F6", order=0),
            Category(id=generate_unique_id("cat"), name="学习", icon="📚", color="#8B5CF6", order=1),
            Category(id=generate_unique_id("cat"), name="生活", icon="🏠", color="#10B981", order=2),
            Category(id=generate_unique_id("cat"), name="其他", icon="📌", color="#6B7280", order=3),
        ]
        self.categories = defaults
        self._save_json(self.categories_file, self.categories)

    def _save_tasks(self):
        self._save_json(self.tasks_file, self.tasks)

    def _save_categories(self):
        self._save_json(self.categories_file, self.categories)

    def _save_pomodoros(self):
        self._save_json(self.pomodoros_file, self.pomodoros)

    def _save_settings(self):
        payload = json.dumps(asdict(self.settings), ensure_ascii=False, indent=2)
        self.settings_file.write_text(payload, encoding="utf-8")

    # ===== Task CRUD =====
    def add_task(self, title: str, description: str = "", priority: str = "medium",
                 category_id: str = "", due_date: str = "", tags: List[str] = None,
                 quadrant: str = "") -> Task:
        if not title or not title.strip():
            raise ValueError("任务标题不能为空")
        if priority not in VALID_PRIORITIES:
            priority = "medium"
        if quadrant not in VALID_QUADRANTS:
            quadrant = ""

        max_order = max((t.order for t in self.tasks), default=-1)
        task = Task(
            id=generate_unique_id("task"),
            title=title.strip(),
            description=description.strip(),
            status="not_started",
            priority=priority,
            quadrant=quadrant,
            category_id=category_id,
            due_date=due_date,
            tags=tags or [],
            created_at=datetime.now().isoformat(),
            completed_at="",
            pomodoro_count=0,
            order=max_order + 1
        )
        self.tasks.append(task)
        self._save_tasks()
        return task

    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        task = self.get_task(task_id)
        if not task:
            return None

        for key, value in kwargs.items():
            if hasattr(task, key):
                if key == "status" and value not in VALID_STATUSES:
                    continue
                if key == "priority" and value not in VALID_PRIORITIES:
                    continue
                if key == "quadrant" and value not in VALID_QUADRANTS:
                    continue
                if key == "title" and (not value or not str(value).strip()):
                    continue
                setattr(task, key, value)

        # 自动设置完成时间
        if task.status == "completed" and not task.completed_at:
            task.completed_at = datetime.now().isoformat()
        elif task.status != "completed":
            task.completed_at = ""

        self._save_tasks()
        return task

    def delete_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        self.tasks.remove(task)
        # 删除关联的番茄记录
        self.pomodoros = [p for p in self.pomodoros if p.task_id != task_id]
        self._save_tasks()
        self._save_pomodoros()
        return True

    def get_task(self, task_id: str) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_tasks(self, status: str = "", category_id: str = "",
                  priority: str = "", quadrant: str = "",
                  due_date: str = "", search: str = "") -> List[Task]:
        result = self.tasks.copy()

        if status:
            result = [t for t in result if t.status == status]
        if category_id:
            result = [t for t in result if t.category_id == category_id]
        if priority:
            result = [t for t in result if t.priority == priority]
        if quadrant:
            result = [t for t in result if t.quadrant == quadrant]
        if due_date:
            result = [t for t in result if t.due_date == due_date]
        if search:
            search_lower = search.lower()
            result = [t for t in result if search_lower in t.title.lower()
                      or search_lower in t.description.lower()]

        return sorted(result, key=lambda t: t.order)

    def get_tasks_by_date_range(self, start_date: str, end_date: str) -> List[Task]:
        return [t for t in self.tasks
                if t.due_date and start_date <= t.due_date <= end_date]

    def get_today_tasks(self) -> List[Task]:
        today = datetime.now().strftime("%Y-%m-%d")
        return self.get_tasks(due_date=today)

    def reorder_tasks(self, task_ids: List[str]) -> bool:
        task_map = {t.id: t for t in self.tasks}
        for i, tid in enumerate(task_ids):
            if tid in task_map:
                task_map[tid].order = i
        self._save_tasks()
        return True

    def update_task_status(self, task_id: str, status: str) -> Optional[Task]:
        if status not in VALID_STATUSES:
            return None
        return self.update_task(task_id, status=status)

    def update_task_priority(self, task_id: str, priority: str) -> Optional[Task]:
        if priority not in VALID_PRIORITIES:
            return None
        return self.update_task(task_id, priority=priority)

    def update_task_quadrant(self, task_id: str, quadrant: str) -> Optional[Task]:
        if quadrant not in VALID_QUADRANTS:
            return None
        return self.update_task(task_id, quadrant=quadrant)

    # ===== Category CRUD =====
    def add_category(self, name: str, icon: str = "📁", color: str = "#C7CEEA") -> Category:
        if not name or not name.strip():
            raise ValueError("分类名称不能为空")
        max_order = max((c.order for c in self.categories), default=-1)
        category = Category(
            id=generate_unique_id("cat"),
            name=name.strip(),
            icon=icon,
            color=color,
            order=max_order + 1
        )
        self.categories.append(category)
        self._save_categories()
        return category

    def update_category(self, category_id: str, **kwargs) -> Optional[Category]:
        category = self.get_category(category_id)
        if not category:
            return None
        for key, value in kwargs.items():
            if hasattr(category, key):
                setattr(category, key, value)
        self._save_categories()
        return category

    def delete_category(self, category_id: str) -> bool:
        category = self.get_category(category_id)
        if not category:
            return False
        self.categories.remove(category)
        # 清除任务的分类关联
        for task in self.tasks:
            if task.category_id == category_id:
                task.category_id = ""
        self._save_categories()
        self._save_tasks()
        return True

    def get_category(self, category_id: str) -> Optional[Category]:
        for cat in self.categories:
            if cat.id == category_id:
                return cat
        return None

    def get_categories(self) -> List[Category]:
        return sorted(self.categories, key=lambda c: c.order)

    # ===== Pomodoro 番茄钟 =====
    def start_pomodoro(self, task_id: str, duration: int = 25) -> PomodoroRecord:
        task = self.get_task(task_id)
        if not task:
            raise ValueError("任务不存在")

        record = PomodoroRecord(
            id=generate_unique_id("pomo"),
            task_id=task_id,
            started_at=datetime.now().isoformat(),
            duration=duration,
            completed=False
        )
        self.pomodoros.append(record)
        self._save_pomodoros()
        return record

    def complete_pomodoro(self, pomodoro_id: str) -> Optional[PomodoroRecord]:
        for record in self.pomodoros:
            if record.id == pomodoro_id:
                record.ended_at = datetime.now().isoformat()
                record.completed = True
                # 更新任务的番茄计数
                task = self.get_task(record.task_id)
                if task:
                    task.pomodoro_count += 1
                    self._save_tasks()
                self._save_pomodoros()
                return record
        return None

    def cancel_pomodoro(self, pomodoro_id: str) -> bool:
        for record in self.pomodoros:
            if record.id == pomodoro_id:
                record.ended_at = datetime.now().isoformat()
                record.completed = False
                self._save_pomodoros()
                return True
        return False

    def get_pomodoros_by_task(self, task_id: str) -> List[PomodoroRecord]:
        return [p for p in self.pomodoros if p.task_id == task_id]

    def get_pomodoros_by_date(self, date: str) -> List[PomodoroRecord]:
        return [p for p in self.pomodoros if p.started_at.startswith(date)]

    def get_today_pomodoro_count(self) -> int:
        today = datetime.now().strftime("%Y-%m-%d")
        return sum(1 for p in self.pomodoros
                   if p.started_at.startswith(today) and p.completed)

    # ===== 统计 =====
    def get_stats(self, start_date: str = "", end_date: str = "") -> Dict[str, Any]:
        tasks = self.tasks
        if start_date and end_date:
            tasks = [t for t in tasks if start_date <= t.created_at[:10] <= end_date]

        total = len(tasks)
        completed = sum(1 for t in tasks if t.status == "completed")
        in_progress = sum(1 for t in tasks if t.status == "in_progress")
        not_started = sum(1 for t in tasks if t.status == "not_started")

        pomodoros = self.pomodoros
        if start_date and end_date:
            pomodoros = [p for p in pomodoros
                        if start_date <= p.started_at[:10] <= end_date]
        pomodoro_completed = sum(1 for p in pomodoros if p.completed)
        pomodoro_minutes = sum(p.duration for p in pomodoros if p.completed)

        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "in_progress_tasks": in_progress,
            "not_started_tasks": not_started,
            "completion_rate": round(completed / total * 100, 1) if total > 0 else 0,
            "pomodoro_count": pomodoro_completed,
            "pomodoro_minutes": pomodoro_minutes,
            "pomodoro_hours": round(pomodoro_minutes / 60, 1)
        }

    def get_daily_stats(self, date: str) -> Dict[str, Any]:
        tasks_created = sum(1 for t in self.tasks if t.created_at.startswith(date))
        tasks_completed = sum(1 for t in self.tasks
                             if t.completed_at and t.completed_at.startswith(date))
        pomodoros = sum(1 for p in self.pomodoros
                       if p.started_at.startswith(date) and p.completed)
        return {
            "date": date,
            "tasks_created": tasks_created,
            "tasks_completed": tasks_completed,
            "pomodoros": pomodoros
        }

    # ===== 设置 =====
    def get_settings(self) -> Settings:
        return self.settings

    def update_settings(self, **kwargs) -> Settings:
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
        self._save_settings()
        return self.settings

    def get_theme(self) -> str:
        return self.settings.theme

    def save_theme(self, theme: str):
        self.settings.theme = theme
        self._save_settings()

    # ===== 数据导出/导入 =====
    def export_data(self) -> Dict[str, Any]:
        return {
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "data": {
                "tasks": [asdict(t) for t in self.tasks],
                "categories": [asdict(c) for c in self.categories],
                "pomodoros": [asdict(p) for p in self.pomodoros],
                "settings": asdict(self.settings)
            }
        }

    def import_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            imported = {"tasks": 0, "categories": 0, "pomodoros": 0}

            if "data" in data:
                inner = data["data"]
                if "tasks" in inner:
                    self.tasks = [Task(**t) for t in inner["tasks"]]
                    imported["tasks"] = len(self.tasks)
                if "categories" in inner:
                    self.categories = [Category(**c) for c in inner["categories"]]
                    imported["categories"] = len(self.categories)
                if "pomodoros" in inner:
                    self.pomodoros = [PomodoroRecord(**p) for p in inner["pomodoros"]]
                    imported["pomodoros"] = len(self.pomodoros)
                if "settings" in inner:
                    self.settings = Settings(**inner["settings"])

            self._save_tasks()
            self._save_categories()
            self._save_pomodoros()
            self._save_settings()

            return {"success": True, "imported": imported}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_data_stats(self) -> Dict[str, int]:
        return {
            "tasks": len(self.tasks),
            "categories": len(self.categories),
            "pomodoros": len(self.pomodoros)
        }
