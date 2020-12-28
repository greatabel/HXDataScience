'''
# 以 100w条数据的 2020-12-28_generated_demo.csv 为例子，
直接hdfs的bash 命令的方式， 步骤如下：

# 关闭只读模式 
hdfs dfsadmin -safemode leave

# 删除旧的同名数据
hdfs dfs -rm -r 2020-12-28_generated_demo.csv

# 在hdfs上创建data目录
hdfs dfs -mkdir data

# 上传100w记录的csv
hdfs dfs -copyFromLocal 2020-12-28_generated_demo.csv data

#查看文件
hdfs dfs -ls data



'''
from snakebite.client import Client

client = Client('localhost', 9000)
for x in client.ls(['/']):
   print(x)
