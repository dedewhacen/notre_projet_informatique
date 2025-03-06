-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Mar 04, 2025 at 04:51 PM
-- Server version: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `gestion_des_reclamation`
--

-- --------------------------------------------------------

--
-- Table structure for table `administration`
--

CREATE TABLE IF NOT EXISTS `administration` (
  `email` varchar(50) NOT NULL DEFAULT '',
  `mot_de_passe` varchar(50) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `etudiant`
--

CREATE TABLE IF NOT EXISTS `etudiant` (
  `matricule_etd` int(11) NOT NULL DEFAULT '0',
  `nom_etd` varchar(50) NOT NULL,
  `prénom_etd` varchar(50) NOT NULL,
  PRIMARY KEY (`matricule_etd`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `matiér`
--

CREATE TABLE IF NOT EXISTS `matiér` (
  `code_mat` varchar(50) NOT NULL DEFAULT '',
  `nom_mat` varchar(50) NOT NULL,
  PRIMARY KEY (`code_mat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `réclamation`
--

CREATE TABLE IF NOT EXISTS `réclamation` (
  `id_rec` int(11) NOT NULL DEFAULT '0',
  `type` varchar(50) NOT NULL,
  `matricule_etd` int(11) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `code_mat` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_rec`),
  KEY `matricule_etd` (`matricule_etd`),
  KEY `email` (`email`),
  KEY `code_mat` (`code_mat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `réclamation`
--
ALTER TABLE `réclamation`
  ADD CONSTRAINT `réclamation_ibfk_1` FOREIGN KEY (`matricule_etd`) REFERENCES `etudiant` (`matricule_etd`),
  ADD CONSTRAINT `réclamation_ibfk_2` FOREIGN KEY (`email`) REFERENCES `administration` (`email`),
  ADD CONSTRAINT `réclamation_ibfk_3` FOREIGN KEY (`code_mat`) REFERENCES `matiér` (`code_mat`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
