CREATE DATABASE  IF NOT EXISTS `antoine_data` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `antoine_data`;
-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: antoine_data
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `antoine_data`
--

DROP TABLE IF EXISTS `antoine_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `antoine_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `compound_name` varchar(100) NOT NULL,
  `A` float NOT NULL,
  `B` float NOT NULL,
  `C` float NOT NULL,
  `temp_min` float DEFAULT NULL,
  `temp_max` float DEFAULT NULL,
  `pressure_unit` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `antoine_data`
--

LOCK TABLES `antoine_data` WRITE;
/*!40000 ALTER TABLE `antoine_data` DISABLE KEYS */;
INSERT INTO `antoine_data` VALUES (1,'Water',8.07131,1730.63,233.426,1,100,'mmHg'),(2,'Ethanol',8.20417,1642.89,230.3,78,203,'mmHg'),(3,'Methanol',7.8975,1474.08,232.979,64,120,'mmHg'),(4,'Benzene',6.90565,1211.03,220.79,8,103,'mmHg'),(5,'Toluene',6.95465,1344.8,219.48,35,111,'mmHg'),(6,'Acetone',7.02447,1161,224,3,78,'mmHg'),(7,'Hexane',6.87762,1171.53,224,19,92,'mmHg');
/*!40000 ALTER TABLE `antoine_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `liquids`
--

DROP TABLE IF EXISTS `liquids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `liquids` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `chemical_formula` varchar(50) DEFAULT NULL,
  `cas_number` varchar(20) DEFAULT NULL,
  `molecular_weight` float DEFAULT NULL,
  `boiling_point` float DEFAULT NULL,
  `antoine_a` float DEFAULT NULL,
  `antoine_b` float DEFAULT NULL,
  `antoine_c` float DEFAULT NULL,
  `temperature_min` float DEFAULT NULL,
  `temperature_max` float DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `name_2` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `liquids`
--

LOCK TABLES `liquids` WRITE;
/*!40000 ALTER TABLE `liquids` DISABLE KEYS */;
INSERT INTO `liquids` VALUES (1,'Water','H2O','7732-18-5',18.015,100,8.07131,1730.63,233.426,1,100,'Pure water'),(2,'Ethanol','C2H6O','64-17-5',46.069,78.37,8.20417,1642.89,230.3,3,78,'Ethanol'),(3,'Methanol','CH4O','67-56-1',32.042,64.7,7.8975,1474.08,232.904,10,80,'Methanol'),(4,'Acetone','C3H6O','67-64-1',58.08,56.05,7.02447,1161,224,5,60,'Acetone'),(5,'Benzene','C6H6','71-43-2',78.114,80.1,6.90565,1211.03,220.79,5,85,'Benzene'),(6,'Toluene','C7H8','108-88-3',92.141,110.6,6.95464,1344.8,219.48,10,120,'Toluene'),(7,'Hexane','C6H14','110-54-3',86.178,68.7,6.87762,1171.53,224.368,10,80,'n-Hexane'),(8,'Heptane','C7H16','142-82-5',100.204,98.4,6.89677,1268.64,216.831,10,110,'n-Heptane'),(9,'Octane','C8H18','111-65-9',114.232,125.7,6.98273,1351.76,209.865,20,140,'n-Octane'),(10,'Propanol','C3H8O','71-23-8',60.095,97.2,8.71668,1640.21,230,10,100,'1-Propanol');
/*!40000 ALTER TABLE `liquids` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `username` varchar(30) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `is_verified` tinyint(1) DEFAULT '0',
  `verification_code` varchar(6) DEFAULT NULL,
  `date_created` datetime DEFAULT CURRENT_TIMESTAMP,
  `reset_code` varchar(6) DEFAULT NULL,
  `reset_expiration` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'HOUSSINE','BEN YAHYA','HOUSSINE_123','housinebabnyhaya123@gmail.com','$2b$12$A0Nosx3niLQTcO2WMqJ3Gua2itmvIUAMkCtLGUFFI2qn51DF9ASd.',0,'724988','2026-04-07 15:26:42',NULL,NULL),(2,'HOUSSINE','banyahya','houssine_user','houssineuser123@gamil.com','$2b$12$9NLes626Vt9p.mb74LHmZeoaYX.8rEP.Ro5gn4u11yYtZkTkm6m7S',0,'173088','2026-04-07 15:33:23',NULL,NULL),(3,'Marouane','El haouari','marouane_user','elhouarimarouane56@gmail.com','$2b$12$QOUz72rq/BrrBCAIYG1Mt.km51oa0wu..5f3szgGJOwebJhs6XB6C',1,'118223','2026-04-07 15:35:10','916201','2026-04-09 14:50:50'),(4,'HOUSSINE','benyahya','houssine','elhoussinebenyahia19@gmail.com','$2b$12$2lAT/JgAgVJjr99hkY/ZpOwyByZXutMDl9M.bJPA9DE3P9xvzWnDe',0,'783233','2026-04-07 15:54:30',NULL,NULL),(5,'mansour','oukchiren','mansour_user123','manssouroukchiran@gmail.com','$2b$12$rE3qxqPXDhLOWy2Lv4d/g.APB9lP3Nm4UURcrFmKLFzgLhDtILICG',1,NULL,'2026-04-07 16:57:55',NULL,NULL),(6,'EL HAIDI ','zakaria','ZACK','elhaidizakaria28@gmail.com','$2b$12$yNhQq8WrSBGS/hHUyHuQ2u9ZCWoUkiDu9wU4eAAL8UVa1xIUOdq62',1,NULL,'2026-04-07 18:00:02',NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_log`
--

DROP TABLE IF EXISTS `user_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `username_attempted` varchar(100) DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `mac_address` varchar(17) DEFAULT NULL,
  `action` varchar(100) DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_log`
--

LOCK TABLES `user_log` WRITE;
/*!40000 ALTER TABLE `user_log` DISABLE KEYS */;
INSERT INTO `user_log` VALUES (1,5,NULL,'127.0.0.1',NULL,'Login Success','2026-04-07 23:49:48'),(2,3,NULL,'127.0.0.1',NULL,'Login Failed - Email Not Verified','2026-04-07 23:53:30'),(3,3,NULL,'127.0.0.1',NULL,'Login Failed - Email Not Verified','2026-04-07 23:53:43'),(4,3,NULL,'127.0.0.1',NULL,'Login Failed - Email Not Verified','2026-04-07 23:54:08'),(5,3,NULL,'127.0.0.1',NULL,'Login Failed - Email Not Verified','2026-04-07 23:56:05'),(6,5,NULL,'127.0.0.1',NULL,'Login Success','2026-04-07 23:56:16'),(7,3,NULL,'127.0.0.1',NULL,'Login Failed - Email Not Verified','2026-04-07 23:57:12'),(8,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: marouane_user)','2026-04-08 00:10:22'),(9,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: marouane_user)','2026-04-08 00:10:27'),(10,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: marouane_user)','2026-04-08 00:10:32'),(11,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Email Not Verified','2026-04-08 00:10:33'),(12,6,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: ZACK)','2026-04-08 00:30:12'),(13,6,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: ZACK)','2026-04-08 00:30:22'),(14,6,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: ZACK)','2026-04-08 00:32:09'),(15,6,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: ZACK)','2026-04-08 00:32:14'),(16,6,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: ZACK)','2026-04-08 00:32:19'),(17,6,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: ZACK)','2026-04-08 00:32:24'),(18,6,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: ZACK)','2026-04-08 00:32:29'),(19,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Requested','2026-04-08 00:34:32'),(20,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Requested','2026-04-08 00:34:35'),(21,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Requested','2026-04-08 00:48:58'),(22,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Successful','2026-04-08 00:50:29'),(23,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Email Not Verified','2026-04-08 00:50:45'),(24,5,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 00:51:30'),(25,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Requested','2026-04-08 01:02:33'),(26,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Successful','2026-04-08 01:03:45'),(27,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Email Not Verified','2026-04-08 01:03:54'),(28,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Email Not Verified','2026-04-08 01:09:30'),(29,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: marouane_user)','2026-04-08 01:10:05'),(30,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Requested','2026-04-08 10:09:37'),(31,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Successful','2026-04-08 10:10:21'),(32,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Email Not Verified','2026-04-08 10:10:28'),(33,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: marouane_user)','2026-04-08 10:20:32'),(34,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: marouane_user)','2026-04-08 10:20:35'),(35,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: marouane_user)','2026-04-08 10:20:37'),(36,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Requested','2026-04-08 10:21:49'),(37,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Successful - Auto Verified','2026-04-08 10:22:43'),(38,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Invalid Credentials (Username: marouane_user)','2026-04-08 10:23:18'),(39,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 10:25:01'),(40,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Wrong Password','2026-04-08 10:25:51'),(41,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Wrong Password','2026-04-08 10:33:18'),(42,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Wrong Password','2026-04-08 10:35:50'),(43,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 10:44:01'),(44,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Wrong Password','2026-04-08 10:50:35'),(45,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 10:50:45'),(46,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 10:58:35'),(47,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 11:18:18'),(48,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 11:30:53'),(49,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Wrong Password','2026-04-08 17:29:24'),(50,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Wrong Password','2026-04-08 17:29:29'),(51,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Wrong Password','2026-04-08 17:29:31'),(52,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 17:38:16'),(53,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 17:43:22'),(54,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 18:25:54'),(55,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 18:27:11'),(56,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 18:34:39'),(57,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 18:37:34'),(58,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 18:39:47'),(59,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 18:42:06'),(60,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 18:46:00'),(61,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 18:47:44'),(62,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Requested','2026-04-08 18:52:11'),(63,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 18:52:54'),(64,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 19:10:29'),(65,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 19:15:47'),(66,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 19:21:56'),(67,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 19:24:44'),(68,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Requested','2026-04-08 19:27:58'),(69,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Wrong Password','2026-04-08 19:28:07'),(70,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Wrong Password','2026-04-08 19:28:10'),(71,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Failed - Wrong Password','2026-04-08 19:28:12'),(72,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-08 21:00:58'),(73,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-09 13:41:57'),(74,3,NULL,'127.0.0.1','00:00:00:00:00:00','Password Reset Requested','2026-04-09 14:40:50'),(75,3,NULL,'127.0.0.1','00:00:00:00:00:00','Login Success','2026-04-09 14:44:57');
/*!40000 ALTER TABLE `user_log` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-09 23:55:08
