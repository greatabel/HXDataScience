import sys

# https://stackoverflow.com/questions/58057157/filtering-out-files-in-hdfs-with-time-range

for line in sys.stdin:
    line = line.strip()
    keys = line.split()
    for key in keys:
        value = 0
        print('{0}\t{1}'.format(key, value) )
    if '2468' in line:
        print('line=>', line)