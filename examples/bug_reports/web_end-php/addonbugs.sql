-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Generation Time: Dec 15, 2019 at 06:34 PM
-- Server version: 5.7.25-log
-- PHP Version: 7.1.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `addonbugs`
--
CREATE DATABASE IF NOT EXISTS `addonbugs` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `addonbugs`;

-- --------------------------------------------------------

--
-- Table structure for table `bugs_table`
--

DROP TABLE IF EXISTS `bugs_table`;
CREATE TABLE `bugs_table` (
  `ind` int(11) NOT NULL,
  `description` varchar(10000) CHARACTER SET ascii NOT NULL DEFAULT 'Report missing description',
  `submitted` date DEFAULT NULL,
  `resolved` int(11) DEFAULT '0',
  `resolution` text
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bugs_table`
--
ALTER TABLE `bugs_table`
  ADD UNIQUE KEY `ind` (`ind`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bugs_table`
--
ALTER TABLE `bugs_table`
  MODIFY `ind` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
