CREATE DATABASE  IF NOT EXISTS `dwh` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dwh`;
-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: dwh
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Temporary view structure for view `composite_rate`
--

DROP TABLE IF EXISTS `composite_rate`;
/*!50001 DROP VIEW IF EXISTS `composite_rate`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `composite_rate` AS SELECT 
 1 AS `dol`,
 1 AS `eur`,
 1 AS `rub`,
 1 AS `chi`,
 1 AS `rate_date`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `currency`
--

DROP TABLE IF EXISTS `currency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `currency` (
  `currency_id` int NOT NULL AUTO_INCREMENT,
  `currency_code` varchar(3) NOT NULL,
  `currency_load_datetime` datetime NOT NULL,
  PRIMARY KEY (`currency_id`),
  UNIQUE KEY `md5_hash_UNIQUE` (`currency_id`),
  UNIQUE KEY `currency_name_UNIQUE` (`currency_code`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `currency_BEFORE_INSERT` BEFORE INSERT ON `currency` FOR EACH ROW BEGIN
	SET NEW.currency_name = NEW.currency_name;
    SET NEW.currency_load_datetime = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `currency_name`
--

DROP TABLE IF EXISTS `currency_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `currency_name` (
  `currency_name_id` int NOT NULL AUTO_INCREMENT,
  `currency_id` int NOT NULL,
  `currency_name_rus` varchar(45) DEFAULT NULL,
  `currency_name_eng` varchar(45) DEFAULT NULL,
  `currency_name_deu` varchar(45) DEFAULT NULL,
  `currency_name_chi` varchar(45) DEFAULT NULL,
  `currency_name_load_datetime` datetime NOT NULL,
  PRIMARY KEY (`currency_name_id`),
  UNIQUE KEY `language_id_UNIQUE` (`currency_name_id`),
  KEY `currency_id_idx` (`currency_id`),
  CONSTRAINT `currency_id` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`currency_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `currency_name_BEFORE_INSERT` BEFORE INSERT ON `currency_name` FOR EACH ROW BEGIN
	SET NEW.currency_name_load_datetime = sysdate();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Temporary view structure for view `currency_on_date`
--

DROP TABLE IF EXISTS `currency_on_date`;
/*!50001 DROP VIEW IF EXISTS `currency_on_date`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `currency_on_date` AS SELECT 
 1 AS `rus`,
 1 AS `rate_value`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `exchange_cost_rub`
--

DROP TABLE IF EXISTS `exchange_cost_rub`;
/*!50001 DROP VIEW IF EXISTS `exchange_cost_rub`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `exchange_cost_rub` AS SELECT 
 1 AS `рубль`,
 1 AS `доллар`,
 1 AS `евро`,
 1 AS `юань`,
 1 AS `дата курса`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `exchange_rub`
--

DROP TABLE IF EXISTS `exchange_rub`;
/*!50001 DROP VIEW IF EXISTS `exchange_rub`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `exchange_rub` AS SELECT 
 1 AS `рубль`,
 1 AS `доллар`,
 1 AS `евро`,
 1 AS `юань`,
 1 AS `дата курса`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `locale`
--

DROP TABLE IF EXISTS `locale`;
/*!50001 DROP VIEW IF EXISTS `locale`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `locale` AS SELECT 
 1 AS `code`,
 1 AS `rus`,
 1 AS `eng`,
 1 AS `deu`,
 1 AS `chi`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `rate`
--

DROP TABLE IF EXISTS `rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rate` (
  `rate_currency_id` int NOT NULL,
  `rate_date` date NOT NULL,
  `rate_value` float DEFAULT NULL,
  `rate_load_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`rate_currency_id`,`rate_date`),
  CONSTRAINT `rate_currency_id` FOREIGN KEY (`rate_currency_id`) REFERENCES `currency` (`currency_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `rate_BEFORE_INSERT` BEFORE INSERT ON `rate` FOR EACH ROW BEGIN
	SET NEW.rate_load_datetime = NOW();
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Temporary view structure for view `rates_view`
--

DROP TABLE IF EXISTS `rates_view`;
/*!50001 DROP VIEW IF EXISTS `rates_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `rates_view` AS SELECT 
 1 AS `currency_code`,
 1 AS `rate_value`,
 1 AS `rate_date`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'dwh'
--

--
-- Dumping routines for database 'dwh'
--

--
-- Final view structure for view `composite_rate`
--

/*!50001 DROP VIEW IF EXISTS `composite_rate`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `composite_rate` AS select `r1`.`dol` AS `dol`,`r2`.`eur` AS `eur`,`r3`.`rub` AS `rub`,`r4`.`chi` AS `chi`,`r1`.`rate_date` AS `rate_date` from ((((select `rate`.`rate_value` AS `dol`,`rate`.`rate_date` AS `rate_date` from `rate` where (`rate`.`rate_currency_id` = 1)) `r1` join (select `rate`.`rate_value` AS `eur`,`rate`.`rate_date` AS `rate_date` from `rate` where (`rate`.`rate_currency_id` = 2)) `r2`) join (select `rate`.`rate_value` AS `rub`,`rate`.`rate_date` AS `rate_date` from `rate` where (`rate`.`rate_currency_id` = 3)) `r3`) join (select `rate`.`rate_value` AS `chi`,`rate`.`rate_date` AS `rate_date` from `rate` where (`rate`.`rate_currency_id` = 4)) `r4` on(((`r1`.`rate_date` = `r2`.`rate_date`) and (`r1`.`rate_date` = `r3`.`rate_date`) and (`r1`.`rate_date` = `r4`.`rate_date`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `currency_on_date`
--

/*!50001 DROP VIEW IF EXISTS `currency_on_date`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `currency_on_date` AS select `l`.`rus` AS `rus`,`p`.`rate_value` AS `rate_value` from ((select `locale`.`rus` AS `rus`,`locale`.`code` AS `code` from `locale`) `l` join (select `rates_view`.`rate_value` AS `rate_value`,`rates_view`.`currency_code` AS `currency_code` from `rates_view` where (`rates_view`.`rate_date` = '2021-07-27')) `p` on((`l`.`code` = `p`.`currency_code`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `exchange_cost_rub`
--

/*!50001 DROP VIEW IF EXISTS `exchange_cost_rub`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `exchange_cost_rub` AS select `exchange_rub`.`рубль` AS `рубль`,round((1 / `exchange_rub`.`доллар`),4) AS `доллар`,round((1 / `exchange_rub`.`евро`),4) AS `евро`,round((1 / `exchange_rub`.`юань`),4) AS `юань`,`exchange_rub`.`дата курса` AS `дата курса` from `exchange_rub` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `exchange_rub`
--

/*!50001 DROP VIEW IF EXISTS `exchange_rub`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `exchange_rub` AS select 1 AS `рубль`,round((`composite_rate`.`rub` / `composite_rate`.`dol`),2) AS `доллар`,round((`composite_rate`.`rub` / `composite_rate`.`eur`),2) AS `евро`,round((`composite_rate`.`rub` / `composite_rate`.`chi`),2) AS `юань`,`composite_rate`.`rate_date` AS `дата курса` from `composite_rate` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `locale`
--

/*!50001 DROP VIEW IF EXISTS `locale`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `locale` AS select `c`.`currency_code` AS `code`,`cn`.`currency_name_rus` AS `rus`,`cn`.`currency_name_eng` AS `eng`,`cn`.`currency_name_deu` AS `deu`,`cn`.`currency_name_chi` AS `chi` from (`currency` `c` join `currency_name` `cn` on((`c`.`currency_id` = `cn`.`currency_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `rates_view`
--

/*!50001 DROP VIEW IF EXISTS `rates_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `rates_view` AS select `c`.`currency_code` AS `currency_code`,`r`.`rate_value` AS `rate_value`,`r`.`rate_date` AS `rate_date` from (`currency` `c` join `rate` `r` on((`c`.`currency_id` = `r`.`rate_currency_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-30  8:24:53
