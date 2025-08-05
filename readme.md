
## 容器创建、运行

没镜像，需要先执行 build_image.sh 脚本，生成镜像
然后再执行脚本 run_container.sh，然后把set_up_spark_rapids.sh拖进生成的挂载目录里在容器里安装好spark&rapids4spark

## spark程序运行
写pyspark，运行scripts/python下的程序就好，现在找到比较好的官方的：
Spark rapids example
https://github.com/NVIDIA/spark-rapids-examples?tab=readme-ov-file

## Profiling Tool 1: spark rapids tools
如何安装及使用:
https://docs.nvidia.com/spark-rapids/user-guide/latest/profiling/quickstart.html

我用pip的：
```
pip install spark-rapids-user-tools
```

我注意到安装方式中有 build from source，看 GitHub 是一个由 core tools 和user tools 组成的仓库：https://github.com/NVIDIA/spark-rapids-tools 

使用: 先有跑出来的eventlogs, 最简单像下面这样使用：
```
 spark_rapids profiling -- \
   --eventlogs /tmp/my-eventlog.json \
   --output_folder ./rapids-output \
```
