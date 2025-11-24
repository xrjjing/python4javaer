import pandas as pd


def main() -> None:
    """
    简单销售数据分析脚本。

    假设当前目录下存在 sales.csv 文件，包含列：
    date, product, quantity, price
    """
    df = pd.read_csv("03.项目实战/04_小型数据分析项目_销售统计/sales.csv")

    # 计算金额
    df["amount"] = df["quantity"] * df["price"]

    print("=== 原始数据预览 ===")
    print(df.head())

    print("\n=== 总销售额 ===")
    print(df["amount"].sum())

    print("\n=== 按商品统计销售额（降序） ===")
    by_product = df.groupby("product")["amount"].sum().sort_values(ascending=False)
    print(by_product)

    print("\n=== 按日期统计销售额 ===")
    df["date"] = pd.to_datetime(df["date"])
    by_day = df.groupby("date")["amount"].sum()
    print(by_day)


if __name__ == "__main__":
    main()

