-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Apr 04, 2025 at 08:11 PM
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
-- Table structure for table `configuration_reclamation`
--

CREATE TABLE IF NOT EXISTS `configuration_reclamation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `niveau` varchar(2) NOT NULL,
  `code_mat` text NOT NULL,
  `date_fermeture` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_config` (`niveau`,`date_fermeture`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `configuration_reclamation`
--

INSERT INTO `configuration_reclamation` (`id`, `niveau`, `code_mat`, `date_fermeture`) VALUES
(1, 'L1', 'GEER_22,GCGP_27,GCGP_22,GEER_24,GEER_23,GEER_25,GCGP_26,GCGP_21,GEER_26,GEER_21,GCGP_24,GCGP_25,ST_22,ST_23,ST_21,GCGP_23', '2025-04-12'),
(2, 'L1', 'ST_22,ST_23,ST_21', '2025-04-05'),
(3, 'L2', 'GEER_41,GEER_42,GEER_43,GEER_44,GEER_45,GEER_46', '2025-04-12'),
(4, 'L3', 'GCGP_51,GCGP_52,GCGP_53,GCGP_54,GCGP_55,GCGP_56,GCGP_57', '2025-04-12'),
(5, 'L2', 'GCGP_41,GCGP_42,GCGP_43,GCGP_44,GCGP_45,GCGP_46,GEER_41,GEER_42,GEER_43,GEER_44,GEER_45,GEER_46,HE_41,HE_42,HE_43,ST_41', '2025-04-05');

-- --------------------------------------------------------

--
-- Table structure for table `etudiant`
--

CREATE TABLE IF NOT EXISTS `etudiant` (
  `matricule_etd` int(11) NOT NULL DEFAULT '0',
  `Email` varchar(50) NOT NULL,
  `Departement` varchar(50) NOT NULL,
  `Licence` varchar(50) NOT NULL,
  `pwd` varchar(255) NOT NULL,
  PRIMARY KEY (`matricule_etd`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `etudiant`
--

INSERT INTO `etudiant` (`matricule_etd`, `Email`, `Departement`, `Licence`, `pwd`) VALUES
(23501, '23501@isme.esp.mr', 'GCGP', 'L1', '2222'),
(23502, '23502@isme.esp.mr', 'GEER', 'L2', '1234'),
(23503, '23503@isme.esp.mr', 'GCGP', 'L1', '123');

-- --------------------------------------------------------

--
-- Table structure for table `matiere`
--

CREATE TABLE IF NOT EXISTS `matiere` (
  `code_mat` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`code_mat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `matiere`
--

INSERT INTO `matiere` (`code_mat`) VALUES
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
('GEER_11'),
('GEER_12'),
('GEER_13'),
('GEER_14'),
('GEER_15'),
('GEER_16'),
('GEER_21'),
('GEER_22'),
('GEER_23'),
('GEER_24'),
('GEER_25'),
('GEER_26'),
('GEER_31'),
('GEER_32'),
('GEER_33'),
('GEER_34'),
('GEER_35'),
('GEER_36'),
('GEER_37'),
('GEER_38'),
('GEER_41'),
('GEER_42'),
('GEER_43'),
('GEER_44'),
('GEER_45'),
('GEER_46'),
('GEER_51'),
('GEER_52'),
('GEER_53'),
('GEER_54'),
('GEER_55'),
('GEER_56'),
('GEER_57'),
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
-- Table structure for table `reclamation`
--

CREATE TABLE IF NOT EXISTS `reclamation` (
  `id_rec` int(11) NOT NULL AUTO_INCREMENT,
  `Détails` text NOT NULL,
  `Objet_rec` varchar(255) NOT NULL,
  `moment_de_creation` date NOT NULL,
  `matricule_etd` int(11) NOT NULL,
  `code_mat` varchar(50) DEFAULT NULL,
  `statut` varchar(20) DEFAULT 'En attente',
  PRIMARY KEY (`id_rec`),
  UNIQUE KEY `unique_reclamation` (`matricule_etd`,`code_mat`),
  KEY `matricule_etd` (`matricule_etd`),
  KEY `code_mat` (`code_mat`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=14 ;

--
-- Dumping data for table `reclamation`
--

INSERT INTO `reclamation` (`id_rec`, `Détails`, `Objet_rec`, `moment_de_creation`, `matricule_etd`, `code_mat`, `statut`) VALUES
(11, 'lo', 'devoir', '2025-03-29', 23502, 'GCGP_11', 'En attente'),
(13, 'kkk', 'Devoir', '2025-03-29', 23501, 'ST_12', 'En attente');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `email_admin` varchar(23) NOT NULL,
  `pwd_admin` varchar(255) NOT NULL
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
-- Constraints for table `reclamation`
--
ALTER TABLE `reclamation`
  ADD CONSTRAINT `reclamation_ibfk_1` FOREIGN KEY (`matricule_etd`) REFERENCES `etudiant` (`matricule_etd`),
  ADD CONSTRAINT `reclamation_ibfk_2` FOREIGN KEY (`code_mat`) REFERENCES `matiere` (`code_mat`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
