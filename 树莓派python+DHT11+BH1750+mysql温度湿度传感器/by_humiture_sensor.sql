/*
Navicat MySQL Data Transfer

Source Server         : 192.168.20.142_树莓派B3Awifi
Source Server Version : 50555
Source Host           : 192.168.20.142:13306
Source Database       : com_it

Target Server Type    : MYSQL
Target Server Version : 50555
File Encoding         : 65001

Date: 2017-07-15 17:49:12
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `by_humiture_sensor`
-- ----------------------------
DROP TABLE IF EXISTS `by_humiture_sensor`;
CREATE TABLE `by_humiture_sensor` (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT '系统流水号',
  `t_dict` varchar(30) DEFAULT '00' COMMENT '星期',
  `t_dictweek` varchar(30) DEFAULT '00' COMMENT '星期代码',
  `t_time` varchar(30) DEFAULT NULL COMMENT '时间2017-07-13 10:47:33',
  `t_hm` varchar(10) DEFAULT '00' COMMENT '月单位',
  `t_hD` varchar(10) DEFAULT '00' COMMENT '日单位t_str_hD',
  `t_hH` varchar(10) DEFAULT '00' COMMENT '小时单位t_str_hH',
  `t_mm` varchar(10) DEFAULT '00' COMMENT '秒单位t_str_mm',
  `G_ch` varchar(10) DEFAULT '23' COMMENT '采集端口号',
  `G_temperature` varchar(10) DEFAULT '00' COMMENT '温度',
  `G_humidity` varchar(10) DEFAULT '00' COMMENT '湿度',
  `G_lx_B` varchar(10) DEFAULT NULL COMMENT '光照强度单位B点',
  `G_lx` varchar(10) DEFAULT '00' COMMENT '光照强度单位A点',
  `G_atmosphere` varchar(20) DEFAULT '00' COMMENT '空气质量单位',
  `G_windpower` varchar(20) DEFAULT '00' COMMENT '风力',
  `sensor_name` varchar(80) DEFAULT NULL COMMENT '采集地点',
  `city_longitude` varchar(20) DEFAULT 'ww' COMMENT '经度',
  `city_latitude` varchar(20) DEFAULT 'ww' COMMENT '纬度',
  `add_name_id` int(20) DEFAULT '0' COMMENT '所有人ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='传感器采集数据表';

-- ----------------------------
-- Records of by_humiture_sensor
-- ----------------------------
