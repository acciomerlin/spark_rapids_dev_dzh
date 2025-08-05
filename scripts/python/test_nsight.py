# 导入 time 和 nvtx 模块
import time
import nvtx  # <--- 新增导入
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, desc
import os

def main():
    """
    主函数，演示使用 RAPIDS 加速的 Spark 数据处理流程。
    """
    # --- 1. 初始化 SparkSession ---
    # Spark 配置已移至 run_profiling.sh 脚本中，以实现集中管理。
    # 这里的 builder 只用于获取或创建现有的 SparkSession 实例。
    spark = SparkSession.builder \
        .appName("SparkRapidsParquetDemo") \
        .getOrCreate()

    # 定义数据和输出目录
    data_dir = "data"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # ================= 核心逻辑开始 =================
    start_time = time.time()
    
    # 使用 NVTX 包裹整个核心逻辑，以便在报告中看到总体耗时
    with nvtx.annotate("Core Logic: Full Process", color="green"):

        # --- 2. 数据读取 ---
        with nvtx.annotate("Data Read", color="blue"):
            sales_df = spark.read.parquet(os.path.join(data_dir, "sales.parquet"))
            products_df = spark.read.parquet(os.path.join(data_dir, "products.parquet"))

        # --- 3. 转换 (Transformation) ---
        with nvtx.annotate("Data Transformation", color="purple"):
            joined_df = sales_df.join(products_df, "product_id")
            filtered_df = joined_df.filter(
                (col("category_id") == 1) & (col("sale_amount") > 500)
            )
            aggregated_df = filtered_df.groupBy("product_name", "category_id") \
                .agg(sum("sale_amount").alias("total_sales"))
            sorted_df = aggregated_df.orderBy(desc("total_sales"))
            final_df = sorted_df.select("product_name", "category_id", "total_sales")

        # --- 4. 触发计算并打印结果 ---
        with nvtx.annotate("Action: Show", color="red"):
            final_df.show()

        # --- 5. 数据写入 ---
        output_path = os.path.join(output_dir, "report.parquet")
        with nvtx.annotate("Action: Write Parquet", color="orange"):
            final_df.write.mode("overwrite").parquet(output_path)
    
    # ================= 核心逻辑结束 =================
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"**************************************************")
    print(f"*** 程序核心逻辑执行耗时: {elapsed_time:.2f} 秒 ***")
    print(f"**************************************************")

    # --- 6. 停止 SparkSession ---
    print("Spark Job Finished. Stopping SparkSession.")
    spark.stop()
    print("SparkSession 已停止。")

if __name__ == "__main__":
    main()