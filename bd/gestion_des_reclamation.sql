-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Apr 05, 2025 at 05:06 AM
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `configuration_reclamation`
--

INSERT INTO `configuration_reclamation` (`id`, `niveau`, `code_mat`, `date_fermeture`) VALUES
(6, 'L1', 'GCGP_21,GCGP_22,GCGP_23,GCGP_24,GCGP_25,GCGP_26,GCGP_27,GEER_21,GEER_22,GEER_23,GEER_24,GEER_25,GEER_26,HE_21,HE_22,HE_23,ST_21,ST_22,ST_23', '2025-04-05');

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
