mapred streaming -input hdfs://127.0.0.1:9000/user/abel/data/2020-12-28_generated_demo.csv -output /user/abel/output0  -mapper "python3 i2csv_mapper.py" -jobconf mapred.reduce.tasks=0 


hadoop fs -cat output0/part-00000
