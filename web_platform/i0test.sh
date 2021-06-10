if [ "$1" = "time" ]
then
  echo "type is time"
  echo "type: $1";
  echo "start: $2";
  echo "end: $3";
fi

if [ "$1" = "sensorid" ]
then
  echo "type is sensorid"
  echo "type: $1"
  echo "sensorid is $2"
fi



hive -e "select from_unixtime(unix_timestamp(substr(create_time,2, 10), 'yyyy-MM-dd')),sensor_id  from smi_sensor where sensor_id < $2  and  from_unixtime(unix_timestamp(substr(create_time,2, 10), 'yyyy-MM-dd')) <=  from_unixtime(unix_timestamp('2021-06-06', 'yyyy-MM-dd'))  limit 5"

sqoop version;
sleep 20