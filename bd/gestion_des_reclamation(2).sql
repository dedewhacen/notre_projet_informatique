-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Mar 29, 2025 at 01:20 AM
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
-- Table structure for table `etudiant`
--

CREATE TABLE IF NOT EXISTS `etudiant` (
  `matricule_etd` int(11) NOT NULL DEFAULT '0',
  `Email` varchar(50) NOT NULL,
  `Departement` varchar(50) NOT NULL,
  `Licence` varchar(50) NOT NULL,
  `pwd` char(5) NOT NULL,
  PRIMARY KEY (`matricule_etd`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `etudiant`
--

INSERT INTO `etudiant` (`matricule_etd`, `Email`, `Departement`, `Licence`, `pwd`) VALUES
(23501, '23501@isme.esp.mr', 'GCGP', 'L1', '2222'),
(23502, '23502@isme.esp.mr', 'GEER', 'L2', '1111'),
(23503, '23503@isme.esp.mr', 'GCGP', 'L1', '123');

-- --------------------------------------------------------

--
-- Table structure for table `matiér`
--

CREATE TABLE IF NOT EXISTS `matiér` (
  `code_mat` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`code_mat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `matiér`
--

INSERT INTO `matiér` (`code_mat`) VALUES
('GCGP_11'),
('GCGP_12'),
('GCGP_13'),
('GCGP_14'),
('GCGP_15'),
('GCGP_16'),
('GCGP_21'),
('GCGP_22'),
('GCGP_23'),
('GCGP_24'),
('GCGP_25'),
('GCGP_26'),
('GCGP_27'),
('GCGP_31'),
('GCGP_32'),
('GCGP_33'),
('GCGP_34'),
('GCGP_35'),
('GCGP_36'),
('GCGP_37'),
('GCGP_38'),
('GCGP_41'),
('GCGP_42'),
('GCGP_43'),
('GCGP_44'),
('GCGP_45'),
('GCGP_46'),
('GCGP_51'),
('GCGP_52'),
('GCGP_53'),
('GCGP_54'),
('GCGP_55'),
('GCGP_56'),
('GCGP_57'),
('HE_11'),
('HE_12'),
('HE_13'),
('HE_21'),
('HE_22'),
('HE_23'),
('HE_31'),
('HE_32'),
('HE_33'),
('HE_41'),
('HE_42'),
('HE_43'),
('HE_51'),
('HE_52'),
('HE_53'),
('ST_11'),
('ST_12'),
('ST_13'),
('ST_21'),
('ST_22'),
('ST_23'),
('ST_31'),
('ST_41');

-- --------------------------------------------------------

--
-- Table structure for table `réclamation`
--

CREATE TABLE IF NOT EXISTS `réclamation` (
  `id_rec` int(11) NOT NULL AUTO_INCREMENT,
  `Détails` varchar(50) NOT NULL,
  `Objet_rec` varchar(255) NOT NULL,
  `moment_de_creation` date NOT NULL,
  `matricule_etd` int(11) NOT NULL,
  `code_mat` varchar(50) DEFAULT NULL,
  `statut` varchar(20) DEFAULT 'En attente',
  PRIMARY KEY (`id_rec`),
  UNIQUE KEY `unique_reclamation` (`matricule_etd`,`code_mat`),
  KEY `matricule_etd` (`matricule_etd`),
  KEY `code_mat` (`code_mat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `email_admin` varchar(23) NOT NULL,
  `pwd_admin` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`email_admin`, `pwd_admin`) VALUES
('admin@isme.esp.mr', 'admin123');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `réclamation`
--
ALTER TABLE `réclamation`
  ADD CONSTRAINT `réclamation_ibfk_1` FOREIGN KEY (`matricule_etd`) REFERENCES `etudiant` (`matricule_etd`),
  ADD CONSTRAINT `réclamation_ibfk_2` FOREIGN KEY (`code_mat`) REFERENCES `matiér` (`code_mat`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
