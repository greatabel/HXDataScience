mapred streaming -input hdfs://127.0.0.1:9000/user/abel/data/2020-12-28_generated_demo.csv -output /user/abel/output0  -mapper "python3 i2csv_mapper.py" -jobconf mapred.reduce.tasks=0 


hadoop fs -cat output0/part-00000


--------------------

传感器分类

--------------------

mapred streaming -input /data/luquan/* -output /user/abel/output1  -mapper "python3 i4hdfs_mapper_to_dic.py" -jobconf mapred.reduce.tasks=0


hadoop fs -cat output1/part-00000

--------------------

mapred streaming -input /data/luquan/* -output /user/abel/output1  -mapper "python3 i4hdfs_mapper_to_dic.py -sensorid 2468" -jobconf mapred.reduce.tasks=0


hadoop fs -cat output1/part-00000