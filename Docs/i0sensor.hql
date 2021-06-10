DROP TABLE smi_sensor ;
CREATE TABLE `smi_sensor` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) DEFAULT NULL COMMENT '公司ID',
  `facility_one` varchar(20) DEFAULT NULL COMMENT '一级设备编号',
  `facility_two` varchar(20) DEFAULT NULL COMMENT '二级设备编号',
  `facility_three` varchar(20) DEFAULT NULL COMMENT '三级级设备编号',
  `monitor_id` int(11) NOT NULL COMMENT '监控点（测量点）编号',
  `plant_id` int(11) DEFAULT NULL COMMENT '工厂id',
  `cost_id` int(11) DEFAULT NULL COMMENT '成本中心ID',
  `sensor_status` tinyint(4) DEFAULT '0' COMMENT '运行状态：0：正常，1：警告，2：错误',
  `energy` varchar(20) DEFAULT NULL COMMENT '剩余电量',
  `service_time` int(11) DEFAULT NULL COMMENT '已使用时间',
  `total_time` int(11) DEFAULT NULL COMMENT '剩余使用时间',
  `sensor_type` tinyint(4) DEFAULT NULL COMMENT '采集类型：0：x轴震动；1：y轴震动；2：z轴震动；3：声音；4：电流（A相）；5：电流（B相）；6：电流（C相）7：温度；8：液位；15：跑偏',
  `sensor_value` decimal(10,3) DEFAULT NULL COMMENT '传感器值',
  `create_by` varchar(50) DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_by` varchar(50) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `remark` varchar(200) DEFAULT NULL,
  `is_del` tinyint(4) NOT NULL DEFAULT '0',
  `original_value` text COMMENT '原始值',
  `batch_time` datetime DEFAULT NULL COMMENT '批次时间',
  `packet` tinyint(4) DEFAULT NULL COMMENT '丢包率：0到10',
  `conversion_id` int(11) DEFAULT NULL COMMENT '关联 io id',
  `sensor_id` int(11) DEFAULT NULL COMMENT '关联传感器ID',
  `voltage` double(11,3) DEFAULT NULL,
  `facility_type` tinyint(4) DEFAULT NULL COMMENT '设备类型'

)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',' ;
LOAD DATA INPATH '/hxdata/smi_sensor_20210605small.csv' OVERWRITE INTO TABLE smi_sensor ;