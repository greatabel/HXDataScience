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
inputFile = "../original_data/smi_sensor_all_*.csv"
conf = SparkConf().setAppName("SparkSQLSMI")
sc = SparkContext()
hiveCtx = HiveContext(sc)
print("Loading data from " + inputFile)

input = hiveCtx.read.csv(inputFile, inferSchema="true", quote="").toDF(
    "id",
    "company_id",
    "facility_one",
    "facility_two",
    "facility_three",
    "monitor_id",
    "plant_id",
    "cost_id",
    "sensor_status",
    "energy",
    "service_time",
    "total_time",
    "sensor_type",
    "sensor_value",
    "create_by",
    "create_time",
    "update_by",
    "update_time",
    "remark",
    "is_del",
    "original_value",
    "batch_time",
    "packet",
    "conversion_id",
    "sensor_id",
    "voltage",
    "facility_type",
)
"""
' select `id`, `company_id`, `facility_one`, 
`facility_two`, `facility_three`, `monitor_id`, `plant_id`, `cost_id`, `sensor_status`,
 `energy`, `service_time`, `total_time`, `sensor_type`, `sensor_value`, `create_by`, `create_time`,
  `update_by`, `update_time`, `remark`, `is_del`, `original_value`, `batch_time`, `packet`, `conversion_id`,
   `sensor_id`, `voltage`, `facility_type`
"""

input.registerTempTable("smi_sensor")
# print(input.show())
topSensors = hiveCtx.sql(
    "SELECT monitor_id, sensor_type, batch_time, sensor_value \
 FROM smi_sensor ORDER BY create_time asc LIMIT 50"
)
print("依据 A =", topSensors.collect())


print("\n\n")


inputFile_monitor = "../original_data/smi_monitor_luquan.csv"

print("Loading data from " + inputFile_monitor)
input1 = hiveCtx.read.csv(inputFile_monitor, inferSchema="true", quote="")
input1.registerTempTable("smi_mointor")
topMonitors = hiveCtx.sql(
    "SELECT _c0 as monitor_id ,_c2 as monitor_code \
 FROM smi_mointor "
)

from pyspark.sql.types import IntegerType
from pyspark.sql.functions import *

# remove quotes “ ” from a column of a Spark dataframe in pyspark
topMonitors = topMonitors.withColumn(
    "monitor_id", regexp_replace("monitor_id", '"', "")
)
topMonitors = topMonitors.withColumn(
    "monitor_code", regexp_replace("monitor_code", '"', "")
)

# 转换字符串为int
topMonitors = topMonitors.withColumn(
    "monitor_id", topMonitors["monitor_id"].cast(IntegerType())
)

print("依据 B =", topMonitors.collect())
print(type(topMonitors))

print("\n--join--\n")
topSensors.join(topMonitors, ["monitor_id"], "left").show()
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
