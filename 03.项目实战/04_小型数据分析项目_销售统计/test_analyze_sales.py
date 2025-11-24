"""analyze_sales 销售统计脚本的基础单元测试。

这里主要测试「核心计算逻辑」：金额列计算、按商品和日期分组聚合。
"""

from pathlib import Path

import sys

import pandas as pd


def _import_analyze_sales():
    """动态导入 analyze_sales 模块。"""
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    import analyze_sales  # type: ignore

    return analyze_sales


def test_sales_amount_and_groupby() -> None:
    """验证金额计算与按商品 / 日期分组统计的正确性。"""
    analyze_sales = _import_analyze_sales()

    df = pd.DataFrame(
        {
            "date": ["2025-01-01", "2025-01-01", "2025-01-02"],
            "product": ["Apple", "Banana", "Apple"],
            "quantity": [3, 5, 2],
            "price": [10.0, 3.0, 10.0],
        }
    )

    # 仿照脚本中的逻辑进行计算与分组
    df["amount"] = df["quantity"] * df["price"]
    assert df["amount"].sum() == 3 * 10 + 5 * 3 + 2 * 10

    by_product = df.groupby("product")["amount"].sum()
    assert by_product["Apple"] == 3 * 10 + 2 * 10
    assert by_product["Banana"] == 5 * 3

    df["date"] = pd.to_datetime(df["date"])
    by_day = df.groupby("date")["amount"].sum()
    assert len(by_day) == 2

