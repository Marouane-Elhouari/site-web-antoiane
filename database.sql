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
  `date_created` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'abdo','labdo','abdolabdo','abdo1@gmail.com','$2b$12$yv3ov2wyN36hFB5ufgp10OD1xGMjyRyqv0jLOEkH2V3nwtkuQoQwS','2026-04-03 16:53:30'),(2,'hamza','kassi','hamzakassi','hamza12@gmail.com','$2b$12$z6l9yp6TOynbGH21PYzr9.NoTaZWeBam6JY5VUsblJ0hNir4qRb.e','2026-04-03 17:33:39'),(3,'atha','taha','athataha','atha@gmail.com','$2b$12$H.UfhweMjPRxmH3z.IOmcOvP0GRCwlFYpFfFm7RwNNH03AXD3LZKO','2026-04-03 18:06:40'),(4,'HOUSSINE','BOUSINE','HUSSINE','HOUSSINE@GAMIL.COM','$2b$12$ivLgCWRzy39TBwvaJtJ4gufnJ4baUQWbKUF6iwzoxqfs.5FJNl/5m','2026-04-03 18:59:52');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-03 19:44:17
