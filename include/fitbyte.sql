-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 18, 2020 at 09:25 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fitbyte`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `account_id` int(11) NOT NULL,
  `username` varchar(32) NOT NULL,
  `password_salt` char(16) NOT NULL,
  `password_hash` char(64) NOT NULL,
  `date_created` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`account_id`, `username`, `password_salt`, `password_hash`, `date_created`) VALUES
(1, 'testuser', '$2b$12$zqGhGcF..', '$2b$12$zqGhGcF..kAFui9WCMBwreQmV16M5y.euavA06hQ5gsWUdsYySRXm', '2020-04-15 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `achieved_badges`
--

CREATE TABLE `achieved_badges` (
  `badge_entry_id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  `badge_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `badges`
--

CREATE TABLE `badges` (
  `badge_id` int(11) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `badges`
--

INSERT INTO `badges` (`badge_id`, `description`) VALUES
(1, 'First Goal - Successfully complete one goal'),
(2, 'Doubling up - Successfully complete 2 goals'),
(3, 'Streak - Successfully complete 5 goals'),
(4, 'Goal getter - Successfully complete 10 goals'),
(5, 'Expert - Successfully complete 15 goals'),
(6, 'Dedicated - Successfully complete 20 goals'),
(7, 'Motivated - Successfully complete 25 goals'),
(8, 'Addicted - Successfully complete 35 goals'),
(9, 'Bullseye - Successfully complete 50 goal'),
(10, 'Supreme - Successfully complete 75 goals'),
(11, 'Godly - Successfully complete 100 goals');

-- --------------------------------------------------------

--
-- Table structure for table `current_goals`
--

CREATE TABLE `current_goals` (
  `goal_id` int(11) NOT NULL,
  `target` float NOT NULL,
  `metric` varchar(64) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `set_interval` float NOT NULL,
  `account_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `current_goals`
--

INSERT INTO `current_goals` (`goal_id`, `target`, `metric`, `start_date`, `end_date`, `set_interval`, `account_id`) VALUES
(1, 80, 'weight', '2020-04-16', '2020-05-01', 7, 1);

-- --------------------------------------------------------

--
-- Table structure for table `energy_intake`
--

CREATE TABLE `energy_intake` (
  `entry_id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `value` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `fat_intake`
--

CREATE TABLE `fat_intake` (
  `account_id` int(11) NOT NULL,
  `entry_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `value` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `fibre_intake`
--

CREATE TABLE `fibre_intake` (
  `account_id` int(11) NOT NULL,
  `entry_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `value` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `profiles`
--

CREATE TABLE `profiles` (
  `profile_id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  `first_name` varchar(35) NOT NULL,
  `last_name` varchar(35) NOT NULL,
  `DOB` date NOT NULL,
  `current_weight` float NOT NULL,
  `height` float NOT NULL,
  `sex` char(1) NOT NULL,
  `activity_rating` int(11) NOT NULL,
  `goals_completed` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `profiles`
--

INSERT INTO `profiles` (`profile_id`, `account_id`, `first_name`, `last_name`, `DOB`, `current_weight`, `height`, `sex`, `activity_rating`) VALUES
(1, 1, 'Philip', '', '2000-10-26', 80, 100, 'm', 3);

-- --------------------------------------------------------

--
-- Table structure for table `protein_intake`
--

CREATE TABLE `protein_intake` (
  `account_id` int(11) NOT NULL,
  `entry_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `value` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `salt_intake`
--

CREATE TABLE `salt_intake` (
  `account_id` int(11) NOT NULL,
  `entry_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `value` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sugar_intake`
--

CREATE TABLE `sugar_intake` (
  `account_id` int(11) NOT NULL,
  `entry_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `value` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `weight`
--

CREATE TABLE `weight` (
  `account_id` int(11) NOT NULL,
  `entry_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `value` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `weight`
--

INSERT INTO `weight` (`account_id`, `entry_id`, `date`, `value`) VALUES
(1, 1, '2020-04-14', 80),
(1, 2, '2020-04-07', 78),
(1, 3, '2020-03-29', 80),
(1, 6, '2020-04-17', 78),
(1, 7, '2020-04-15', 80);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`account_id`);

--
-- Indexes for table `achieved_badges`
--
ALTER TABLE `achieved_badges`
  ADD PRIMARY KEY (`badge_entry_id`);

--
-- Indexes for table `badges`
--
ALTER TABLE `badges`
  ADD PRIMARY KEY (`badge_id`);

--
-- Indexes for table `current_goals`
--
ALTER TABLE `current_goals`
  ADD PRIMARY KEY (`goal_id`);

--
-- Indexes for table `energy_intake`
--
ALTER TABLE `energy_intake`
  ADD PRIMARY KEY (`entry_id`);

--
-- Indexes for table `fat_intake`
--
ALTER TABLE `fat_intake`
  ADD PRIMARY KEY (`entry_id`);

--
-- Indexes for table `fibre_intake`
--
ALTER TABLE `fibre_intake`
  ADD PRIMARY KEY (`entry_id`);

--
-- Indexes for table `profiles`
--
ALTER TABLE `profiles`
  ADD PRIMARY KEY (`profile_id`);

--
-- Indexes for table `protein_intake`
--
ALTER TABLE `protein_intake`
  ADD PRIMARY KEY (`entry_id`);

--
-- Indexes for table `salt_intake`
--
ALTER TABLE `salt_intake`
  ADD PRIMARY KEY (`entry_id`);

--
-- Indexes for table `sugar_intake`
--
ALTER TABLE `sugar_intake`
  ADD PRIMARY KEY (`entry_id`);

--
-- Indexes for table `weight`
--
ALTER TABLE `weight`
  ADD PRIMARY KEY (`entry_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `account_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `achieved_badges`
--
ALTER TABLE `achieved_badges`
  MODIFY `badge_entry_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `badges`
--
ALTER TABLE `badges`
  MODIFY `badge_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `current_goals`
--
ALTER TABLE `current_goals`
  MODIFY `goal_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `energy_intake`
--
ALTER TABLE `energy_intake`
  MODIFY `entry_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fat_intake`
--
ALTER TABLE `fat_intake`
  MODIFY `entry_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fibre_intake`
--
ALTER TABLE `fibre_intake`
  MODIFY `entry_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `profiles`
--
ALTER TABLE `profiles`
  MODIFY `profile_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `protein_intake`
--
ALTER TABLE `protein_intake`
  MODIFY `entry_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `salt_intake`
--
ALTER TABLE `salt_intake`
  MODIFY `entry_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sugar_intake`
--
ALTER TABLE `sugar_intake`
  MODIFY `entry_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `weight`
--
ALTER TABLE `weight`
  MODIFY `entry_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
