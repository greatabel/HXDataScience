SELECT
	a.monitor_id,
	a.sensor_type,
	DATE_FORMAT( a.batch_time, '%Y-%m-%d %H:%i:%s' ) create_time,
	max( a.sensor_value ) sensor_value,
	b.monitor_code 
FROM
	(
	$ { strSql }) a
	LEFT JOIN smi_monitor b ON a.monitor_id = b.id 
WHERE
	a.sensor_value IS NOT NULL < IF test = "facilityThrees != null" > 
	AND a.facility_three IN $ { facilityThrees } </ IF > 
	AND a.batch_time >= #{s.startDate,jdbcType=TIMESTAMP} and a.batch_time &lt;= #{s.endDate,jdbcType=TIMESTAMP}
	
GROUP BY
	a.monitor_id,
	a.batch_time,
	a.sensor_type 
ORDER BY
	a.create_time ASC

这条sql是有关联其它表查询的    

-------------------------


SELECT
	* 
FROM
	smi_sensor_20210105 
WHERE
	create_time BETWEEN '2021-01-20 00:00:00' 
	AND '2021-01-20 23:59:59'
 这条是单独查归档的表数据的sql    