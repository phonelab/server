-- MySQL dump 10.13  Distrib 5.1.63, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: phonelab_dev
-- ------------------------------------------------------
-- Server version	5.1.63-0ubuntu0.11.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `application_application`
--

DROP TABLE IF EXISTS `application_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `application_application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `package_name` varchar(100) NOT NULL,
  `intent_name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `type` varchar(30) NOT NULL,
  `starttime` datetime DEFAULT NULL,
  `endtime` datetime DEFAULT NULL,
  `version` varchar(10) NOT NULL,
  `active` varchar(1) NOT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_id` (`user_id_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `application_application`
--

LOCK TABLES `application_application` WRITE;
/*!40000 ALTER TABLE `application_application` DISABLE KEYS */;
INSERT INTO `application_application` VALUES (2,76,'app1','app1.pack','manoj','','.apk',NULL,NULL,'1','E','2012-07-09 00:11:58','2012-07-09 00:11:58'),(3,51,'app2','app2.pack','manoj','','.apk',NULL,NULL,'1','E','2012-07-09 00:12:36','2012-07-09 00:12:36');
/*!40000 ALTER TABLE `application_application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'group1');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add application',8,'add_application'),(23,'Can change application',8,'change_application'),(24,'Can delete application',8,'delete_application'),(25,'Can add device',9,'add_device'),(26,'Can change device',9,'change_device'),(27,'Can delete device',9,'delete_device'),(28,'Can add device application',10,'add_deviceapplication'),(29,'Can change device application',10,'change_deviceapplication'),(30,'Can delete device application',10,'delete_deviceapplication'),(31,'Can add device profile',11,'add_deviceprofile'),(32,'Can change device profile',11,'change_deviceprofile'),(33,'Can delete device profile',11,'delete_deviceprofile'),(34,'Can add transaction',12,'add_transaction'),(35,'Can change transaction',12,'change_transaction'),(36,'Can delete transaction',12,'delete_transaction'),(37,'Can add transaction dev app',13,'add_transactiondevapp'),(38,'Can change transaction dev app',13,'change_transactiondevapp'),(39,'Can delete transaction dev app',13,'delete_transactiondevapp'),(40,'Can add user profile',14,'add_userprofile'),(41,'Can change user profile',14,'change_userprofile'),(42,'Can delete user profile',14,'delete_userprofile');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=78 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'manoj','','','manojmyl@buffalo.edu','pbkdf2_sha256$10000$zeqG4Criglb2$c6RKwwerHQXlz0/qYcDxeHYRFFJgQGEgxXowoQRUplY=',1,1,1,'2012-07-09 00:00:44','2012-06-21 14:08:10'),(76,'manojmc89','Manoj','Mylap','mcmanojster@gmail.com','pbkdf2_sha256$10000$hlsQNKkjQ31x$e6UhqwE5ysvTmGXr17PesGcJ/BRz0dZCrDHY58MjEMU=',0,1,0,'2012-07-09 10:26:53','2012-07-06 12:32:52'),(51,'manojmc','','','mnj_mc@yahoo.com','pbkdf2_sha256$10000$wTk3RexqoMqx$2IBh9CEpyQy/YM1Rvu3K7r35xkVvxn9JRLMB5ehSrDU=',0,1,0,'2012-07-09 13:09:26','2012-06-29 19:45:13'),(77,'manOOO','','','mnj_mc@yahoo.com','pbkdf2_sha256$10000$4zsU1N8OWtkq$Hcm9Kd5Zrc8AoWZCapfi7VjLxFO0LS/q+8h1Q7FxWV0=',0,0,0,'2012-07-09 12:33:55','2012-07-09 12:33:55');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,51,1),(2,76,1);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_device`
--

DROP TABLE IF EXISTS `device_device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_device` (
  `id` varchar(15) NOT NULL,
  `email` varchar(30) NOT NULL,
  `reg_id` varchar(300) NOT NULL,
  `collapse_key` varchar(255) NOT NULL,
  `last_messaged` datetime DEFAULT NULL,
  `failed_push` tinyint(1) NOT NULL,
  `update_interval` varchar(5) NOT NULL,
  `active` varchar(1) NOT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_device`
--

LOCK TABLES `device_device` WRITE;
/*!40000 ALTER TABLE `device_device` DISABLE KEYS */;
INSERT INTO `device_device` VALUES ('355031040585610','phonelab@gmail.com','APA91bEra29OF2aUaLu6VRrTktGfLOHAlwIL3FOr2eioFxTagi7ktVoq40Ltr3A_4TOjknTPtv84TC5UwS6DJ9EcuOawFiUnLOrpk3HDj5KB0FX5uEY5sd8SFZ4_GWfl5Ch8YO8w43XKSGAvTlRyDKPDuVydDaQHbK0CVHrgWmAQW8V0xS-JdjINB28A5sMWpvPBKoJnG_80','10',NULL,0,'10','E','2012-07-09 00:01:53','2012-07-09 00:01:53'),('355031040690899','phonelab@gmail.com','APA91bEra29OF2aUaLu6VRrTktGfLOHAlwIL3FOr2eioFxTagi7ktVoq40Ltr3A_4TOjknTPtv84TC5UwS6DJ9EcuOawFiUnLOrpk3HDj5KB0FX5uEY5sd8SFZ4_GWfl5Ch8YO8w43XKSGAvTlRyDKPDuVydDaQHbK0CVHrgWmAQW8V0xS-JdjINB28A5sMWpvPBKoJnG_80','10',NULL,0,'10','E','2012-07-09 00:02:27','2012-07-09 00:02:27'),('355031041145620','phonelab@gmail.com','APA91bEra29OF2aUaLu6VRrTktGfLOHAlwIL3FOr2eioFxTagi7ktVoq40Ltr3A_4TOjknTPtv84TC5UwS6DJ9EcuOawFiUnLOrpk3HDj5KB0FX5uEY5sd8SFZ4_GWfl5Ch8YO8w43XKSGAvTlRyDKPDuVydDaQHbK0CVHrgWmAQW8V0xS-JdjINB28A5sMWpvPBKoJnG_80','10',NULL,0,'10','E','2012-07-09 00:03:00','2012-07-09 00:03:00'),('A000002A28E17B','phonelab@gmail.com','APA91bESzOPlmDphFl3mm-94KWIxNh0WpHQRp18SH7FWt-eX0oOgKPQA1pc5cb7l2vA4OSM3p42p_UnVc922xXgs1_Pre8MyLm4Dh6tkGcaOLCWGK9rOzxmZyLO3iKjNzOWgEU8ISilsmWaSNToFvA9CMv-txQby6p1FF8ukFpWZZ0Ys4xBtJJOoLyLd2ZQ9EQeSFnfvDjYN','10',NULL,0,'10','E','2012-07-09 00:06:24','2012-07-09 00:06:24'),('A000002A28E207','phonelab@gmail.com','APA91bEra29OF2aUaLu6VRrTktGfLOHAlwIL3FOr2eioFxTagi7ktVoq40Ltr3A_4TOjknTPtv84TC5UwS6DJ9EcuOawFiUnLOrpk3HDj5KB0FX5uEY5sd8SFZ4_GWfl5Ch8YO8w43XKSGAvTlRyDKPDuVydDaQHbK0CVHrgWmAQW8V0xS-JdjINB28A5sMWpvPBKoJnG_80','10',NULL,0,'10','E','2012-07-09 00:06:46','2012-07-09 00:06:46'),('A000002A2866B6','phonelab@gmail.com','APA91bFlAEicM1c53Pe-s-VMWFX8OW_TMD0NoTf0_z-_GYuD092RyNJFUNuv-Hb9awXZK8tbPNVGWtqXy3VWlkTAC9xwfAkEG6okHrs6RyvwJ2w1OzkTTK_3KS31DM4OY8AD5-7NQ-x09VAy0b1_U9xlPLzZ68JuKiCdFzczP1yv2m4ToV7rx5aIbft5ehTUIkpGHjIToTTU','10',NULL,0,'10','E','2012-07-09 00:07:28','2012-07-09 00:07:28'),('A000002A28C4A1','phonelab@gmail.com','APA91bE3BRgit4WoeeMniRI-_gK4g8a_t626ZDzUZVrTuAUcoBqZ1bzJKeKfciQSpAn4SZbHV_QRwLB9vVsrW6Sd9fVyrJib4W8_tU_q7X7rG_LFI9m4_gXx1rg2C5VMXjs8AEU_VtjW1RfW9E0RMC3HH123OnLF-VFUS2P6hIz9weKuP3-vSPj8Xk-Tqryiu92nFhi4-rCw','10',NULL,0,'10','E','2012-07-09 00:08:02','2012-07-09 00:08:02');
/*!40000 ALTER TABLE `device_device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_deviceapplication`
--

DROP TABLE IF EXISTS `device_deviceapplication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_deviceapplication` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dev_id` varchar(15) NOT NULL,
  `app_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dev_id` (`dev_id`,`app_id`),
  KEY `device_deviceapplication_260276da` (`dev_id`),
  KEY `device_deviceapplication_269da59a` (`app_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_deviceapplication`
--

LOCK TABLES `device_deviceapplication` WRITE;
/*!40000 ALTER TABLE `device_deviceapplication` DISABLE KEYS */;
INSERT INTO `device_deviceapplication` VALUES (1,'A000002A28E17B',2),(2,'A000002A28E207',3);
/*!40000 ALTER TABLE `device_deviceapplication` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_deviceprofile`
--

DROP TABLE IF EXISTS `device_deviceprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_deviceprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dev_id` varchar(15) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `phone_no` varchar(13) DEFAULT NULL,
  `working` varchar(1) NOT NULL,
  `plan` varchar(45) DEFAULT NULL,
  `image_version` varchar(45) DEFAULT NULL,
  `phone_purpose` varchar(1) NOT NULL,
  `service_type` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dev_id` (`dev_id`),
  KEY `device_deviceprofile_fbfc09f1` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_deviceprofile`
--

LOCK TABLES `device_deviceprofile` WRITE;
/*!40000 ALTER TABLE `device_deviceprofile` DISABLE KEYS */;
INSERT INTO `device_deviceprofile` VALUES (1,'A000002A28E17B',76,'716-245-3483','Y','Bug Tracking','1.0','P','4'),(2,'A000002A28E207',51,'716-245-3521','Y','Bug Tracking','1.0','P','4');
/*!40000 ALTER TABLE `device_deviceprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2012-07-09 00:01:53',1,9,'355031040585610','355031040585610',1,''),(2,'2012-07-09 00:02:27',1,9,'355031040690899','355031040690899',1,''),(3,'2012-07-09 00:03:00',1,9,'355031041145620','355031041145620',1,''),(4,'2012-07-09 00:06:24',1,9,'A000002A28E17B','A000002A28E17B',1,''),(5,'2012-07-09 00:06:46',1,9,'A000002A28E207','A000002A28E207',1,''),(6,'2012-07-09 00:07:28',1,9,'A000002A2866B6','A000002A2866B6',1,''),(7,'2012-07-09 00:08:02',1,9,'A000002A28C4A1','A000002A28C4A1',1,''),(8,'2012-07-09 00:09:39',1,11,'1','DeviceProfile object',1,''),(9,'2012-07-09 00:10:19',1,11,'2','DeviceProfile object',1,''),(10,'2012-07-09 00:11:58',1,8,'2','app1',1,''),(11,'2012-07-09 00:12:06',1,10,'1','DeviceApplication object',1,''),(12,'2012-07-09 00:12:36',1,8,'3','app2',1,''),(13,'2012-07-09 00:12:38',1,10,'2','DeviceApplication object',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'application','application','application'),(9,'device','device','device'),(10,'device application','device','deviceapplication'),(11,'device profile','device','deviceprofile'),(12,'transaction','transaction','transaction'),(13,'transaction dev app','transaction','transactiondevapp'),(14,'user profile','users','userprofile');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('36225cfc822b9779fbd9caa597e324de','ZWNmZWM3NTE5NjBlNTYwNDg3ZTE4YTQ3ZWM1MmIxODBkYmFiODE5NTqAAn1xAVUKdGVzdGNvb2tp\nZVUGd29ya2VkcQJzLg==\n','2012-07-06 15:12:28'),('ce4760abcdfe0e9254e8a323f5a84958','ZWNmZWM3NTE5NjBlNTYwNDg3ZTE4YTQ3ZWM1MmIxODBkYmFiODE5NTqAAn1xAVUKdGVzdGNvb2tp\nZVUGd29ya2VkcQJzLg==\n','2012-07-09 16:51:34'),('3a7632b37496fec4bd2043ecc5edb3c7','Njc5ZTAxM2YyYmY5YmRkZjIyMTkwY2IxMTRmZTg0M2JiYjFmZTUzMjqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-10 12:08:05'),('244f5d2b1778ebc07c98f91f68298381','Njc5ZTAxM2YyYmY5YmRkZjIyMTkwY2IxMTRmZTg0M2JiYjFmZTUzMjqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-10 19:39:56'),('4ccdfc2562ae0770a4d1b7c3cdb70af9','Njc5ZTAxM2YyYmY5YmRkZjIyMTkwY2IxMTRmZTg0M2JiYjFmZTUzMjqAAn1xAVUKdGVzdGNvb2tp\nZXECVQZ3b3JrZWRxA3Mu\n','2012-07-10 20:02:21'),('f8d880686d9658977794f33fbbc91140','ZWNmZWM3NTE5NjBlNTYwNDg3ZTE4YTQ3ZWM1MmIxODBkYmFiODE5NTqAAn1xAVUKdGVzdGNvb2tp\nZVUGd29ya2VkcQJzLg==\n','2012-07-12 21:29:17'),('d1fdb64a1b3509469f1caddbad032810','YjBlZTQ0NjVjZWI5OTc1ZjAzODhiMzliNDRlZWJlZjZiNTQ3NGJkMDqAAn1xAShVCnRlc3Rjb29r\naWVxAlUGd29ya2VkcQNVDV9hdXRoX3VzZXJfaWSKARZVEl9hdXRoX3VzZXJfYmFja2VuZFUpZGph\nbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmR1Lg==\n','2012-07-12 23:36:53'),('6b81be42f93987664f54bc4aaadae1f7','MWUyMGYzMDRkYjBiYWMyOGEwNjdhZTc2OGI2NWM5OTU3Yzg3MTgxOTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKATl1Lg==\n','2012-07-17 11:06:25'),('655b2224720a37c8d8b2119cd45f99b4','Yjg4YzE5NDE2ZjE0MDdlMDZhZDUwOGZmZjVmMmQ2ZGI0N2MwOWIyODqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKATx1Lg==\n','2012-07-16 19:33:23'),('0afa1874a41e3c4faf007ade1271380a','NDY5OTM5NzkxMmVlMTEyYzMxYzRiNzkyZDZkNDVlMGNlMjhiYTI1YzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKATt1Lg==\n','2012-07-13 20:28:52'),('698d6fb37b6e467c7db8c0760b932194','MWUyMGYzMDRkYjBiYWMyOGEwNjdhZTc2OGI2NWM5OTU3Yzg3MTgxOTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKATl1Lg==\n','2012-07-17 14:48:54'),('a9e3c4446eb383fd5fb0e0c76c7156be','MWUyMGYzMDRkYjBiYWMyOGEwNjdhZTc2OGI2NWM5OTU3Yzg3MTgxOTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKATl1Lg==\n','2012-07-19 13:51:34'),('34613b4485d935adac9eee4e2c7bdae9','NzM3Yzg3Yzk3ZTU2ZmNlYWJhMDkxZmFlODQ5MjllYjg2YWYwZTIyZjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAUx1Lg==\n','2012-07-20 12:34:12'),('0cded8ba9ec590402b8a212aada68b91','NjY5NGVjMWI0ZjQ0YjNjYmZhNDZlYzlhOGM3MDdmYWM2MWNlYTBlMzqAAn1xAS4=\n','2012-07-23 02:53:29'),('0d276f7a286480f491dd4f0fcf752d56','YmY1NzBjZTI0ZGM2ODdmYjMyOGQ0YWYyOTFhZmU4NGU3YWZhNzdhNDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKATN1Lg==\n','2012-07-23 13:09:26');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_transaction`
--

DROP TABLE IF EXISTS `transaction_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction_transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  `progress` int(11) NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `transaction_transaction_fbfc09f1` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_transaction`
--

LOCK TABLES `transaction_transaction` WRITE;
/*!40000 ALTER TABLE `transaction_transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `transaction_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_transactiondevapp`
--

DROP TABLE IF EXISTS `transaction_transactiondevapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction_transactiondevapp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tid_id` int(11) NOT NULL,
  `dev_id` varchar(15) NOT NULL,
  `app_id` int(11) NOT NULL,
  `action` varchar(1) NOT NULL,
  `result` varchar(2) NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tid_id` (`tid_id`,`dev_id`,`app_id`),
  KEY `transaction_transactiondevapp_76e9cc14` (`tid_id`),
  KEY `transaction_transactiondevapp_260276da` (`dev_id`),
  KEY `transaction_transactiondevapp_269da59a` (`app_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_transactiondevapp`
--

LOCK TABLES `transaction_transactiondevapp` WRITE;
/*!40000 ALTER TABLE `transaction_transactiondevapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `transaction_transactiondevapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_userprofile`
--

DROP TABLE IF EXISTS `users_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `ub_id` varchar(30) DEFAULT NULL,
  `activation_key` varchar(40) NOT NULL,
  `key_expires` datetime NOT NULL,
  `user_type` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=48 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_userprofile`
--

LOCK TABLES `users_userprofile` WRITE;
/*!40000 ALTER TABLE `users_userprofile` DISABLE KEYS */;
INSERT INTO `users_userprofile` VALUES (30,60,NULL,'e4fbb7653100e4af16ba9aca51369f97','2012-07-04 19:27:20','participant'),(21,51,NULL,'e0e04617f3569b86687b3b95804ba0ce','2012-07-01 19:45:13','leader'),(46,76,'None','bd2990ee6d93d11181bd8f94db41eda8','2012-07-08 12:32:52','member'),(47,77,NULL,'2e8ac81849e9747daf45cbe630fbe552','2012-07-11 12:33:55','member');
/*!40000 ALTER TABLE `users_userprofile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-07-10 11:41:45
