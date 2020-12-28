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

import pyhdfs


fs = pyhdfs.HdfsClient(hosts='127.0.0.1,50070',user_name='hdfs')
print(fs.get_home_directory() )#返回这个用户的根目录
fs.get_active_namenode()#返回可用的namenode节点