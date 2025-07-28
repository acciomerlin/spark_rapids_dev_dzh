#!/bin/bash

# 这是一个用于启动 Spark+RAPIDS 性能分析任务的脚本。
# 它会使用 NVIDIA Nsight Systems 工具来生成性能报告。

# --- 配置 ---
# 请确保将此路径设置为您的项目根目录
PROJECT_ROOT="/root/spark_rapids_dev" 
NSYS_REPORTS_DIR="${PROJECT_ROOT}/nsys-reports"
SPARK_EVENTS_DIR="file://${PROJECT_ROOT}/data/spark-events"
RAPIDS_JAR="${PROJECT_ROOT}/source/rapids-4-spark_2.12-25.06.0.jar"

# --- 检查 nsys 是否可用 ---
if ! command -v nsys &> /dev/null
then
    echo "错误：'nsys' 命令未找到。"
    echo "请确保 NVIDIA Nsight Systems 已安装并且 'nsys' 在您的系统 PATH 中。"
    exit 1
fi

# --- 准备工作 ---
echo ">>> 清理并创建 nsys 报告输出目录..."
mkdir -p "${NSYS_REPORTS_DIR}"
rm -f "${NSYS_REPORTS_DIR}"/*.nsys-rep

echo ">>> 准备启动 Spark 任务进行性能分析..."

# --- 使用 nsys 包装 spark-submit 命令 ---
nsys profile \
    --trace=cuda,nvtx --stats=true \
    -o "${NSYS_REPORTS_DIR}/spark_rapids_profile_$(date +%Y%m%d_%H%M%S)" \
    -f true \
    spark-submit \
    --master "local[*]" \
    --name "SparkRapidsProfileDemo" \
    --jars "${RAPIDS_JAR}" \
    --conf spark.plugins=com.nvidia.spark.SQLPlugin \
    --conf spark.eventLog.enabled=true \
    --conf spark.eventLog.dir="${SPARK_EVENTS_DIR}" \
    --conf spark.rapids.sql.enabled=true \
    --conf spark.rapids.sql.explain=NONE \
    --conf spark.executorEnv.CUDA_VISIBLE_DEVICES="0" \
    "${PROJECT_ROOT}/data/test_nsight.py"

echo ">>> 脚本执行完毕。"
echo ">>> 请检查输出目录 ${NSYS_REPORTS_DIR} 中的分析报告。"