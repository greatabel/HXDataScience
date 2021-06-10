DROP TABLE smi_sensor ;
CREATE TABLE smi_sensor (
  `id` bigint NOT NULL ,
  `company_id` int  COMMENT '公司ID',
  `facility_one` string  COMMENT '一级设备编号',
  `facility_two` string  COMMENT '二级设备编号',
  `facility_three` string  COMMENT '三级级设备编号',
  `monitor_id` int NOT NULL COMMENT '监控点（测量点）编号',
  `plant_id` int  COMMENT '工厂id',
  `cost_id` int  COMMENT '成本中心ID',
  `sensor_status` tinyint  COMMENT '运行状态：0：正常，1：警告，2：错误',
  `energy` string COMMENT '剩余电量',
  `service_time` int COMMENT '已使用时间',
  `total_time` int COMMENT '剩余使用时间',
  `sensor_type` tinyint  COMMENT '采集类型：0：x轴震动；1：y轴震动；2：z轴震动；3：声音；4：电流（A相）；5：电流（B相）；6：电流（C相）7：温度；8：液位；15：跑偏',
  `sensor_value` decimal  COMMENT '传感器值',
  `create_by` string ,
  `create_time` string  ,
  `update_by` string ,
  `update_time` string  ,
  `remark` string ,
  `is_del` tinyint NOT NULL ,
  `original_value` string COMMENT '原始值',
  `batch_time` string   COMMENT '批次时间',
  `packet` tinyint  COMMENT '丢包率：0到10',
  `conversion_id` int  COMMENT '关联 io id',
  `sensor_id` int  COMMENT '关联传感器ID',
  `voltage` decimal ,
  `facility_type` tinyint  COMMENT '设备类型'

) 
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',' ;
ALTER TABLE smi_sensor SET serdeproperties ('serialization.encoding'='UTF-8');
LOAD DATA INPATH '/hxdata/smi_sensor_20210605small.csv' OVERWRITE INTO TABLE smi_sensor ;