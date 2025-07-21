import csv
import random
from datetime import date, timedelta

# --- 配置 ---
SALES_RECORDS = 10000
PRODUCTS_RECORDS = 100
CATEGORIES = 5
START_DATE = date(2023, 1, 1)
END_DATE = date(2023, 12, 31)

# --- 文件路径 ---
SALES_FILE = "data/sales.csv"
PRODUCTS_FILE = "data/products.csv"

# --- 生成 products.csv ---
print(f"正在生成 {PRODUCTS_FILE}...")
products_header = ["product_id", "product_name", "category_id"]
products_data = []
for i in range(1, PRODUCTS_RECORDS + 1):
    products_data.append([
        i,
        f"Product_{i}",
        random.randint(1, CATEGORIES)
    ])

with open(PRODUCTS_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(products_header)
    writer.writerows(products_data)
print(f"{PRODUCTS_FILE} 生成完毕.")

# --- 生成 sales.csv ---
print(f"正在生成 {SALES_FILE}...")
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

with open(SALES_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(sales_header)
    writer.writerows(sales_data)

print(f"{SALES_FILE} 生成完毕.") 