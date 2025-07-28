# 导入 time 模块
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, desc
import os

def main():
    """
    主函数，演示使用 RAPIDS 加速的 Spark 数据处理流程。
    """
    # --- 1. 初始化 SparkSession ---
    # ... (你的 SparkSession 配置保持不变)
    spark = SparkSession.builder \
        .appName("SparkRapidsParquetDemo") \
        .master("local[*]") \
        .config("spark.plugins", "com.nvidia.spark.SQLPlugin") \
        .config("spark.jars", "/root/spark_rapids_dev/source/rapids-4-spark_2.12-25.06.0.jar") \
        .config("spark.eventLog.enabled", "true") \
        .config("spark.eventLog.dir", "file:/root/spark_rapids_dev/data/spark-events") \
        .config("spark.rapids.sql.enabled", "true") \
        .config("spark.rapids.sql.explain", "NONE") \
        .config("spark.executorEnv.CUDA_VISIBLE_DEVICES", "0") \
        .getOrCreate()

    # ================= 核心逻辑开始计时 =================
    start_time = time.time()

    # --- 2. 数据读取 ---
    # print("正在读取数据...")
    sales_df = spark.read.parquet("data/sales.parquet")
    products_df = spark.read.parquet("data/products.parquet")

    # --- 3. 转换 (Transformation) ---
    # print("开始数据转换...")
    joined_df = sales_df.join(products_df, "product_id")
    filtered_df = joined_df.filter(
        (col("category_id") == 1) & (col("sale_amount") > 500)
    )
    aggregated_df = filtered_df.groupBy("product_name", "category_id") \
        .agg(sum("sale_amount").alias("total_sales"))
    sorted_df = aggregated_df.orderBy(desc("total_sales"))
    final_df = sorted_df.select("product_name", "category_id", "total_sales")
    # print("数据转换完成。")

    # --- 4. 触发计算并打印结果 ---
    # print("显示最终结果:")
    final_df.show()

    # print("打印执行计划以确认 RAPIDS 加速:")
    # final_df.explain()

    # --- 5. 数据写入 ---
    output_path = "output_report.parquet"
    # print(f"正在将结果写入到 {output_path}...")
    final_df.write.mode("overwrite").parquet(output_path)
    # print("数据写入完毕。")
    
    # ================= 核心逻辑结束计时 =================
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"**************************************************")
    print(f"*** 程序核心逻辑执行耗时: {elapsed_time:.2f} 秒 ***")
    print(f"**************************************************")


    # --- 6. 停止 SparkSession ---
    print("按 Enter 键停止 SparkSession...")
    # 为了自动化测试，你可以注释掉 input()
    # input() 
    spark.stop()
    print("SparkSession 已停止。")

if __name__ == "__main__":
    main()