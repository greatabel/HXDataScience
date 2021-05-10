import sys

# https://stackoverflow.com/questions/58057157/filtering-out-files-in-hdfs-with-time-range

for line in sys.stdin:
    line = line.strip()
    keys = line.split(',')
    if len(keys) > 5:
    	if keys[5] == '2468':
    		print(line)
    # if '2468' in line:
    #     print('line=>', line)