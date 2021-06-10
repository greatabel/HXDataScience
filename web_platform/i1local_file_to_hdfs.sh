# 关闭只读模式 
hdfs dfsadmin -safemode leave

# 删除旧的同名数据
hdfs dfs -rm -r /hxdata/smi_sensor_all_20210413.csv
hdfs dfs -rm -r /hxdata/smi_sensor_all_20210414.csv

# 在hdfs上创建data目录
hdfs dfs -mkdir /hxdata

# 上传100w记录的csv
hdfs dfs -copyFromLocal smi_sensor_all_20210413.csv /hxdata
hdfs dfs -copyFromLocal smi_sensor_all_20210414.csv /hxdata

#查看文件
hdfs dfs -ls /hxdata