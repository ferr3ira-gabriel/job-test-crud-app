CREATE DATABASE IF NOT EXISTS crud_app;
USE crud_app;

DROP TABLE IF EXISTS `deploy_info`;

CREATE TABLE `deploy_infos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `component` varchar(30) NOT NULL,
  `version` varchar(30) NOT NULL,
  `owner` varchar(30) NOT NULL,
  `status` varchar(30) NOT NULL,
  `data` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
)