import sys
import argparse

# https://stackoverflow.com/questions/58057157/filtering-out-files-in-hdfs-with-time-range
def my_parser():
    parser = argparse.ArgumentParser(description='sku(type)  color pdate(produce date)')
    parser.add_argument('-sensorid', dest='sensorid', default="1234", required=True, type=str)

    parser_result = parser.parse_args()
    print(parser_result.sensorid, type(parser_result.sensorid))
    return parser_result.sensorid



senorid =my_parser()
for line in sys.stdin:
    line = line.strip()
    keys = line.split(',')
    if len(keys) > 5:
    	if keys[5] == senorid:
    		print(line)
    # if '2468' in line:
    #     print('line=>', line)