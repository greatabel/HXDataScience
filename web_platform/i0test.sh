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



hive -e "";
sqoop version;
sleep 50