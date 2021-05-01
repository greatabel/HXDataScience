import findspark
findspark.init()
# A simple demo for working with SparkSQL and Tweets
from pyspark import SparkContext, SparkConf
from pyspark.sql import HiveContext, Row
from pyspark.sql.types import IntegerType
import json
import sys
from termcolor import colored

# 自带表头
# inputFile = '../original_data/smi_sensor_202011_202011261650.csv'

# 没有表头
inputFile = '../original_data/smi_sensor_all_*.csv'
conf = SparkConf().setAppName("SparkSQLSMI")
sc = SparkContext()
hiveCtx = HiveContext(sc)
print("Loading data from " + inputFile)

input = hiveCtx.read.csv(inputFile,
        inferSchema="true",
        quote="").toDF("id","company_id","facility_one",
    "facility_two","facility_three","monitor_id","plant_id","cost_id","sensor_status",
    "energy","service_time","total_time","sensor_type","sensor_value","create_by","create_time",
    "update_by","update_time","remark","is_del","original_value","batch_time","packet","conversion_id",
    "sensor_id","voltage","facility_type")
'''
' select `id`, `company_id`, `facility_one`, 
`facility_two`, `facility_three`, `monitor_id`, `plant_id`, `cost_id`, `sensor_status`,
 `energy`, `service_time`, `total_time`, `sensor_type`, `sensor_value`, `create_by`, `create_time`,
  `update_by`, `update_time`, `remark`, `is_del`, `original_value`, `batch_time`, `packet`, `conversion_id`,
   `sensor_id`, `voltage`, `facility_type`
'''
input.registerTempTable("smi_sensor")
# print(input.show())
topTweets = hiveCtx.sql("SELECT monitor_id, sensor_type, batch_time, sensor_value \
 FROM smi_sensor ORDER BY create_time asc LIMIT 10")
print('依据 A =', topTweets.collect() )

# https://stackoverflow.com/questions/39535447/attributeerror-dataframe-object-has-no-attribute-map
# topTweetText = topTweets.rdd.map(lambda row : row.text)
# print(topTweetText.collect() )
# # Make a happy person row
# happyPeopleRDD = sc.parallelize([Row(name="holden", favouriteBeverage="coffee")])

# #https://blog.csdn.net/m0_37870649/article/details/81603764
# happyPeopleSchemaRDD = hiveCtx.createDataFrame(happyPeopleRDD)
# happyPeopleSchemaRDD.registerTempTable("happy_people")
# # Make a UDF to tell us how long some text is
# hiveCtx.registerFunction("strLenPython", lambda x: len(x), IntegerType())
# lengthSchemaRDD = hiveCtx.sql("SELECT strLenPython('text') FROM tweets LIMIT 10")
# print(lengthSchemaRDD.collect() )
sc.stop()
