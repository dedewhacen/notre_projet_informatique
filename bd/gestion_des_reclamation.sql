-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Apr 11, 2025 at 01:26 AM
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
  `date_fermeture` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_config` (`niveau`,`date_fermeture`),
  KEY `idx_date_fermeture` (`date_fermeture`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=58 ;

--
-- Dumping data for table `configuration_reclamation`
--

INSERT INTO `configuration_reclamation` (`id`, `niveau`, `code_mat`, `date_fermeture`) VALUES
(56, 'L3', 'GCGP_54,GCGP_55', '2025-04-11 22:34:00');

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
(23501, '23501@isme.esp.mr', 'GCGP', 'L1', '1111'),
(23502, '23502@isme.esp.mr', 'GEER', 'L2', '1234'),
(23503, '23503@isme.esp.mr', 'GCGP', 'L1', '123');

-- --------------------------------------------------------

--
-- Table structure for table `matiere`
--

CREATE TABLE IF NOT EXISTS `matiere` (
  `code_mat` varchar(50) NOT NULL DEFAULT '',
  `niveau_de_licence` varchar(50) DEFAULT NULL,
  `semestre` varchar(2) DEFAULT NULL,
  `dept_mat` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`code_mat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `matiere`
--

INSERT INTO `matiere` (`code_mat`, `niveau_de_licence`, `semestre`, `dept_mat`) VALUES
('GCGP_11', 'L1', 'S1', 'GCGP'),
('GCGP_12', 'L1', 'S1', 'GCGP'),
('GCGP_13', 'L1', 'S1', 'GCGP'),
('GCGP_14', 'L1', 'S1', 'GCGP'),
('GCGP_15', 'L1', 'S1', 'GCGP'),
('GCGP_16', 'L1', 'S1', 'GCGP'),
('GCGP_21', 'L1', 'S2', 'GCGP'),
('GCGP_22', 'L1', 'S2', 'GCGP'),
('GCGP_23', 'L1', 'S2', 'GCGP'),
('GCGP_24', 'L1', 'S2', 'GCGP'),
('GCGP_25', 'L1', 'S2', 'GCGP'),
('GCGP_26', 'L1', 'S2', 'GCGP'),
('GCGP_27', 'L1', 'S2', 'GCGP'),
('GCGP_31', 'L2', 'S3', 'GCGP'),
('GCGP_32', 'L2', 'S3', 'GCGP'),
('GCGP_33', 'L2', 'S3', 'GCGP'),
('GCGP_34', 'L2', 'S3', 'GCGP'),
('GCGP_35', 'L2', 'S3', 'GCGP'),
('GCGP_36', 'L2', 'S3', 'GCGP'),
('GCGP_37', 'L2', 'S3', 'GCGP'),
('GCGP_38', 'L2', 'S3', 'GCGP'),
('GCGP_41', 'L2', 'S4', 'GCGP'),
('GCGP_42', 'L2', 'S4', 'GCGP'),
('GCGP_43', 'L2', 'S4', 'GCGP'),
('GCGP_44', 'L2', 'S4', 'GCGP'),
('GCGP_45', 'L2', 'S4', 'GCGP'),
('GCGP_46', 'L2', 'S4', 'GCGP'),
('GCGP_51', 'L3', 'S5', 'GCGP'),
('GCGP_52', 'L3', 'S5', 'GCGP'),
('GCGP_53', 'L3', 'S5', 'GCGP'),
('GCGP_54', 'L3', 'S5', 'GCGP'),
('GCGP_55', 'L3', 'S5', 'GCGP'),
('GCGP_56', 'L3', 'S5', 'GCGP'),
('GCGP_57', 'L3', 'S5', 'GCGP'),
('GEER_11', 'L1', 'S1', 'GEER'),
('GEER_12', 'L1', 'S1', 'GEER'),
('GEER_13', 'L1', 'S1', 'GEER'),
('GEER_14', 'L1', 'S1', 'GEER'),
('GEER_15', 'L1', 'S1', 'GEER'),
('GEER_16', 'L1', 'S1', 'GEER'),
('GEER_21', 'L1', 'S2', 'GEER'),
('GEER_22', 'L1', 'S2', 'GEER'),
('GEER_23', 'L1', 'S2', 'GEER'),
('GEER_24', 'L1', 'S2', 'GEER'),
('GEER_25', 'L1', 'S2', 'GEER'),
('GEER_26', 'L1', 'S2', 'GEER'),
('GEER_31', 'L2', 'S3', 'GEER'),
('GEER_32', 'L2', 'S3', 'GEER'),
('GEER_33', 'L2', 'S3', 'GEER'),
('GEER_34', 'L2', 'S3', 'GEER'),
('GEER_35', 'L2', 'S3', 'GEER'),
('GEER_36', 'L2', 'S3', 'GEER'),
('GEER_37', 'L2', 'S3', 'GEER'),
('GEER_38', 'L2', 'S3', 'GEER'),
('GEER_41', 'L2', 'S4', 'GEER'),
('GEER_42', 'L2', 'S4', 'GEER'),
('GEER_43', 'L2', 'S4', 'GEER'),
('GEER_44', 'L2', 'S4', 'GEER'),
('GEER_45', 'L2', 'S4', 'GEER'),
('GEER_46', 'L2', 'S4', 'GEER'),
('GEER_51', 'L3', 'S5', 'GEER'),
('GEER_52', 'L3', 'S5', 'GEER'),
('GEER_53', 'L3', 'S5', 'GEER'),
('GEER_54', 'L3', 'S5', 'GEER'),
('GEER_55', 'L3', 'S5', 'GEER'),
('GEER_56', 'L3', 'S5', 'GEER'),
('GEER_57', 'L3', 'S5', 'GEER'),
('HE_11', 'L1', 'S1', 'COMN'),
('HE_12', 'L1', 'S1', 'COMN'),
('HE_13', 'L1', 'S1', 'COMN'),
('HE_21', 'L1', 'S2', 'COMN'),
('HE_22', 'L1', 'S2', 'COMN'),
('HE_23', 'L1', 'S2', 'COMN'),
('HE_31', 'L2', 'S3', 'COMN'),
('HE_32', 'L2', 'S3', 'COMN'),
('HE_33', 'L2', 'S3', 'COMN'),
('HE_41', 'L2', 'S4', 'COMN'),
('HE_42', 'L2', 'S4', 'COMN'),
('HE_43', 'L2', 'S4', 'COMN'),
('HE_51', 'L3', 'S5', 'COMN'),
('HE_52', 'L3', 'S5', 'COMN'),
('HE_53', 'L3', 'S5', 'COMN'),
('ST_11', 'L1', 'S1', 'COMN'),
('ST_12', 'L1', 'S1', 'COMN'),
('ST_13', 'L1', 'S1', 'COMN'),
('ST_21', 'L1', 'S2', 'COMN'),
('ST_22', 'L1', 'S2', 'COMN'),
('ST_23', 'L1', 'S2', 'COMN'),
('ST_31', 'L2', 'S3', 'COMN'),
('ST_41', 'L2', 'S4', 'COMN');

-- --------------------------------------------------------

--
-- Table structure for table `reclamation`
--

CREATE TABLE IF NOT EXISTS `reclamation` (
  `id_rec` int(11) NOT NULL AUTO_INCREMENT,
  `Détails` text NOT NULL,
  `Objet_rec` varchar(255) NOT NULL,
  `moment_de_creation` datetime NOT NULL,
  `matricule_etd` int(11) NOT NULL,
  `code_mat` varchar(50) DEFAULT NULL,
  `statut` enum('En attente','En traitement','Accepté','Refusé') DEFAULT 'En attente',
  PRIMARY KEY (`id_rec`),
  UNIQUE KEY `unique_reclamation` (`matricule_etd`,`code_mat`),
  KEY `matricule_etd` (`matricule_etd`),
  KEY `code_mat` (`code_mat`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=90 ;

--
-- Dumping data for table `reclamation`
--

INSERT INTO `reclamation` (`id_rec`, `Détails`, `Objet_rec`, `moment_de_creation`, `matricule_etd`, `code_mat`, `statut`) VALUES
(17, 'nnnnnnn', 'Devoir', '2025-04-05 00:00:00', 23502, 'GEER_34', 'Accepté'),
(19, 'kalma \r\n', 'Examen', '2025-04-07 00:00:00', 23502, 'GEER_41', 'Refusé'),
(21, '15\r\n', 'Devoir', '2025-04-08 00:00:00', 23502, 'GEER_45', 'Refusé'),
(38, '2222', 'Examen', '2025-04-08 00:00:00', 23502, 'GEER_46', 'Refusé'),
(66, '20/20/20', 'Devoir', '2025-04-08 16:45:21', 23502, 'HE_42', 'En attente'),
(68, '20\r\n\r\n', 'Devoir', '2025-04-08 17:01:01', 23502, 'GEER_44', 'En attente'),
(85, '20/20', 'Devoir', '2025-04-09 18:51:36', 23502, 'GEER_43', 'En attente'),
(86, 'je pense mon note est 17', 'Devoir', '2025-04-10 21:49:33', 23501, 'HE_22', 'Accepté'),
(87, 'j''ai trouve 0 ', 'TP', '2025-04-10 21:50:36', 23501, 'GCGP_22', 'Refusé'),
(88, '20/20', 'Examen', '2025-04-10 21:51:14', 23501, 'ST_22', 'Refusé'),
(89, 'c''est pas bon', 'Examen', '2025-04-10 22:24:45', 23501, 'GCGP_23', 'En attente');

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
