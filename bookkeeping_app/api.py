"""PyWebView API - 记账应用接口（增强版）"""
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

from services.bookkeeping import BookkeepingService


def api_error_handler(func):
    """API错误处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return {"success": False, "error": str(e), "error_type": "validation"}
        except FileNotFoundError as e:
            return {"success": False, "error": f"文件未找到: {e}", "error_type": "file"}
        except PermissionError as e:
            return {"success": False, "error": f"权限不足: {e}", "error_type": "permission"}
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "unknown",
                "traceback": traceback.format_exc()
            }
    return wrapper


class Api:
    def __init__(self, data_dir: Path):
        self.bookkeeping = BookkeepingService(data_dir / "记账数据")

    def __dir__(self):
        return [name for name, val in self.__class__.__dict__.items() if callable(val)]

    # ========== 分类管理（含多级） ==========
    def get_categories(self, type_filter: str = "", include_children: bool = True):
        return self.bookkeeping.get_categories(type_filter, include_children)

    def get_flat_categories(self, type_filter: str = ""):
        return self.bookkeeping.get_flat_categories(type_filter)

    @api_error_handler
    def add_category(self, name: str, icon: str, color: str, cat_type: str, parent_id: str = ""):
        return self.bookkeeping.add_category(name, icon, color, cat_type, parent_id)

    @api_error_handler
    def update_category(self, id: str, name: str, icon: str, color: str):
        return self.bookkeeping.update_category(id, name, icon, color)

    @api_error_handler
    def delete_category(self, id: str, strategy: str = "check", migrate_to: str = ""):
        return self.bookkeeping.delete_category(id, strategy, migrate_to)

    # ========== 标签管理 ==========
    def get_tags(self, category_id: str = ""):
        return self.bookkeeping.get_tags(category_id)

    @api_error_handler
    def add_tag(self, name: str, category_id: str = ""):
        return self.bookkeeping.add_tag(name, category_id)

    @api_error_handler
    def delete_tag(self, id: str):
        return self.bookkeeping.delete_tag(id)

    # ========== 账户管理 ==========
    def get_accounts(self):
        return self.bookkeeping.get_accounts()

    @api_error_handler
    def add_account(self, name: str, acc_type: str, icon: str, color: str, balance: float = 0.0, credit_limit: float = 0.0, billing_day: int = 0, repayment_day: int = 0, note: str = ""):
        return self.bookkeeping.add_account(name, acc_type, icon, color, balance, credit_limit, billing_day, repayment_day, note)

    @api_error_handler
    def update_account(self, id: str, name: str, icon: str, color: str, balance: float = None, credit_limit: float = None, billing_day: int = None, repayment_day: int = None, note: str = None):
        return self.bookkeeping.update_account(id, name, icon, color, balance, credit_limit, billing_day, repayment_day, note)

    @api_error_handler
    def delete_account(self, id: str, strategy: str = "check", migrate_to: str = ""):
        return self.bookkeeping.delete_account(id, strategy, migrate_to)

    def get_total_assets(self):
        return self.bookkeeping.get_total_assets()

    # ========== 预算管理 ==========
    def get_budgets(self, ledger_id: str = ""):
        return self.bookkeeping.get_budgets(ledger_id)

    @api_error_handler
    def add_budget(self, name: str, budget_type: str, amount: float, category_id: str = "", period: str = "month", ledger_id: str = ""):
        return self.bookkeeping.add_budget(name, budget_type, amount, category_id, period, ledger_id)

    @api_error_handler
    def update_budget(self, id: str, name: str, amount: float):
        return self.bookkeeping.update_budget(id, name, amount)

    @api_error_handler
    def delete_budget(self, id: str):
        return self.bookkeeping.delete_budget(id)

    def get_budget_status(self, ledger_id: str = ""):
        return self.bookkeeping.get_budget_status(ledger_id)

    # ========== 账本管理 ==========
    def get_ledgers(self, include_archived: bool = False):
        return self.bookkeeping.get_ledgers(include_archived)

    @api_error_handler
    def add_ledger(self, name: str, icon: str, color: str):
        return self.bookkeeping.add_ledger(name, icon, color)

    @api_error_handler
    def update_ledger(self, id: str, name: str, icon: str, color: str):
        return self.bookkeeping.update_ledger(id, name, icon, color)

    @api_error_handler
    def archive_ledger(self, id: str):
        return self.bookkeeping.archive_ledger(id)

    @api_error_handler
    def delete_ledger(self, id: str):
        return self.bookkeeping.delete_ledger(id)

    # ========== 记录管理 ==========
    def get_records(self, start_date: str = "", end_date: str = "", type_filter: str = "", category_id: str = "", account_id: str = "", ledger_id: str = "", limit: int = 0):
        return self.bookkeeping.get_records(start_date, end_date, type_filter, category_id, account_id, ledger_id, limit)

    @api_error_handler
    def add_record(self, rec_type: str, amount: float, category_id: str, date: str, time: str = "", note: str = "", tags: List[str] = None, account_id: str = "", ledger_id: str = ""):
        return self.bookkeeping.add_record(rec_type, amount, category_id, date, time, note, tags, account_id, ledger_id)

    @api_error_handler
    def update_record(self, id: str, rec_type: str, amount: float, category_id: str, date: str, time: str = "", note: str = "", tags: List[str] = None, account_id: str = "", ledger_id: str = ""):
        return self.bookkeeping.update_record(id, rec_type, amount, category_id, date, time, note, tags, account_id, ledger_id)

    @api_error_handler
    def delete_record(self, id: str):
        return self.bookkeeping.delete_record(id)

    # ========== 智能推荐 ==========
    def get_smart_suggestions(self):
        return self.bookkeeping.get_smart_suggestions()

    # ========== 统计功能 ==========
    def get_today_summary(self, ledger_id: str = ""):
        today = datetime.now().strftime("%Y-%m-%d")
        return self.bookkeeping.get_summary(today, today, ledger_id)

    def get_week_summary(self, ledger_id: str = ""):
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        return self.bookkeeping.get_summary(monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d"), ledger_id)

    def get_month_summary(self, ledger_id: str = ""):
        today = datetime.now()
        start = today.replace(day=1).strftime("%Y-%m-%d")
        if today.month == 12:
            end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        return self.bookkeeping.get_summary(start, end.strftime("%Y-%m-%d"), ledger_id)

    def get_year_summary(self, ledger_id: str = ""):
        year = datetime.now().year
        return self.bookkeeping.get_summary(f"{year}-01-01", f"{year}-12-31", ledger_id)

    def get_summary(self, start_date: str, end_date: str, ledger_id: str = ""):
        return self.bookkeeping.get_summary(start_date, end_date, ledger_id)

    def get_daily_stats(self, start_date: str, end_date: str, ledger_id: str = ""):
        return self.bookkeeping.get_daily_stats(start_date, end_date, ledger_id)

    def get_weekly_stats(self, date: str = "", ledger_id: str = ""):
        return self.bookkeeping.get_weekly_stats(date, ledger_id)

    def get_monthly_stats(self, year: int = 0, ledger_id: str = ""):
        if not year:
            year = datetime.now().year
        return self.bookkeeping.get_monthly_stats(year, ledger_id)

    def get_category_stats(self, start_date: str, end_date: str, rec_type: str = "expense", ledger_id: str = ""):
        return self.bookkeeping.get_category_stats(start_date, end_date, rec_type, ledger_id)

    def get_asset_trend(self, months: int = 6):
        return self.bookkeeping.get_asset_trend(months)

    # ========== 数据导出 ==========
    def export_records_csv(self, start_date: str = "", end_date: str = "", ledger_id: str = ""):
        return self.bookkeeping.export_records_csv(start_date, end_date, ledger_id)

    def export_summary_csv(self, year: int = 0, ledger_id: str = ""):
        if not year:
            year = datetime.now().year
        return self.bookkeeping.export_summary_csv(year, ledger_id)
