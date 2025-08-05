import pandas as pd
import random
from datetime import date, timedelta
import os

# --- 配置 ---
SALES_RECORDS = 10000
PRODUCTS_RECORDS = 100
CATEGORIES = 5
START_DATE = date(2023, 1, 1)
END_DATE = date(2023, 12, 31)

# --- 文件路径 (修改为 .parquet) ---
DATA_DIR = "data"
SALES_FILE_PARQUET = os.path.join(DATA_DIR, "sales.parquet")
PRODUCTS_FILE_PARQUET = os.path.join(DATA_DIR, "products.parquet")

# 确保目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# --- 生成 products.parquet ---
print(f"正在生成 {PRODUCTS_FILE_PARQUET}...")
products_header = ["product_id", "product_name", "category_id"]
products_data = []
for i in range(1, PRODUCTS_RECORDS + 1):
    products_data.append([
        i,
        f"Product_{i}",
        random.randint(1, CATEGORIES)
    ])

# 将数据转换为 Pandas DataFrame
products_df = pd.DataFrame(products_data, columns=products_header)

# 直接写入 Parquet 文件
products_df.to_parquet(PRODUCTS_FILE_PARQUET, index=False)

print(f"{PRODUCTS_FILE_PARQUET} 生成完毕.")

# --- 生成 sales.parquet ---
print(f"正在生成 {SALES_FILE_PARQUET}...")
sales_header = ["sale_id", "product_id", "sale_amount", "sale_date"]
sales_data = []
time_delta = END_DATE - START_DATE
for i in range(1, SALES_RECORDS + 1):
    random_days = random.randint(0, time_delta.days)
    sales_data.append([
        i,
        random.randint(1, PRODUCTS_RECORDS),
        round(random.uniform(10.5, 999.9), 2),
        START_DATE + timedelta(days=random_days)
    ])

# 将数据转换为 Pandas DataFrame
sales_df = pd.DataFrame(sales_data, columns=sales_header)

# 直接写入 Parquet 文件
sales_df.to_parquet(SALES_FILE_PARQUET, index=False)

print(f"{SALES_FILE_PARQUET} 生成完毕.")