-- MariaDB dump 10.19  Distrib 10.4.18-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: bd_megakom
-- ------------------------------------------------------
-- Server version	10.4.18-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `media`
--

DROP TABLE IF EXISTS `media`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `media` (
  `hash` varchar(256) NOT NULL,
  `extension` char(26) DEFAULT NULL,
  `size` int(10) unsigned DEFAULT NULL,
  `path` char(1) DEFAULT NULL,
  `post_date` datetime DEFAULT NULL,
  `poster_id` char(26) DEFAULT NULL,
  PRIMARY KEY (`hash`),
  KEY `poster_id` (`poster_id`),
  CONSTRAINT `media_ibfk_1` FOREIGN KEY (`poster_id`) REFERENCES `user` (`phone_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `media`
--

LOCK TABLES `media` WRITE;
/*!40000 ALTER TABLE `media` DISABLE KEYS */;
/*!40000 ALTER TABLE `media` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `phone_num` char(26) NOT NULL,
  `password` char(1) DEFAULT NULL,
  `first_name` char(1) DEFAULT NULL,
  `last_name` char(1) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `username` char(1) DEFAULT NULL,
  `email` char(1) DEFAULT NULL,
  `gender` enum('M','F') DEFAULT NULL,
  `referral_id` char(26) DEFAULT NULL,
  `registration_date` date DEFAULT NULL,
  `ref_account_balance` float unsigned DEFAULT NULL,
  `Momo_num` int(10) unsigned DEFAULT NULL,
  `OM_num` int(10) unsigned DEFAULT NULL,
  `account_balance` float unsigned DEFAULT NULL,
  `town` char(1) DEFAULT NULL,
  `nationality` char(1) DEFAULT NULL,
  `business` tinyint(1) DEFAULT 0,
  `deleted` tinyint(1) DEFAULT 0,
  `last_activity` datetime DEFAULT NULL,
  `loyalty_bonus` tinyint(3) unsigned zerofill DEFAULT 000,
  PRIMARY KEY (`phone_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
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

-- Dump completed on 2021-10-22  8:16:40
