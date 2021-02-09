'''
# python代码是直接调用hdfs接口，如果代码因为未知原因不work时候，
# 还可以使用hdfs的命令，直接处理，具体如下:

# 以 100w条数据的 2020-12-28_generated_demo.csv 为例子，
直接hdfs的bash 命令的方式， 步骤如下：

# 关闭只读模式 
hdfs dfsadmin -safemode leave

# 删除旧的同名数据
hdfs dfs -rm -r 2020-12-28_generated_demo.csv

# 在hdfs上创建data目录
hdfs dfs -mkdir /data

# 上传100w记录的csv
hdfs dfs -copyFromLocal 2020-12-28_generated_demo.csv data

#查看文件
hdfs dfs -ls /data



'''



'''
 -------------
 
 https://crs4.github.io/pydoop/api_docs/hdfs_api.html#module-pydoop.hdfs
'''

import pydoop.hdfs as hdfs


a = hdfs.path.isdir('/test_not_exist')
b = hdfs.path.isdir('/data')
print(a==False, b==True)

if b==True :
	hdfs_client = hdfs.hdfs()
	data_list = hdfs_client.list_directory('/data')
	print(data_list)

	for item in data_list:
	    print(item['name'])
	    if '2020-12-28_generated_demo.csv' in item['name']:
	        print('rm -->', item['name'])
	        hdfs.rm(item['name'], recursive=True, user=None)

	print('---after rm ---')
	data_list = hdfs_client.list_directory('/data')
	print(data_list)

	print('---get test ---')
	lines = []
	with hdfs.open('hdfs://127.0.0.1:9000/data/source_demo.csv') as f:
		for line in f:
			# print(line, type(line))
			l = line.decode('utf-8')
			if '2020-11-15' in l:
				lines.append(l)
	print(lines)
	print('---end get----')

	hdfs.put('2021-02-09_generated_demo.csv', '/data')
	print('---after put ---')
	data_list = hdfs_client.list_directory('/data')
	print(data_list)


