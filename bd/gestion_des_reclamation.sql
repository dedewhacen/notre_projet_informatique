-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Apr 20, 2025 at 01:38 PM
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
  `date_ouverture` datetime NOT NULL,
  `date_fermeture` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_config` (`niveau`,`date_fermeture`),
  KEY `idx_date_fermeture` (`date_fermeture`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;

--
-- Dumping data for table `configuration_reclamation`
--

INSERT INTO `configuration_reclamation` (`id`, `niveau`, `code_mat`, `date_ouverture`, `date_fermeture`) VALUES
(14, 'L2', 'GCGP_41,GCGP_42,GCGP_43,GCGP_44,GCGP_45,GCGP_46,GEER_41,GEER_42,GEER_43,GEER_44,GEER_45,GEER_46,HE_41,HE_42,HE_43,ST_41', '0000-00-00 00:00:00', '2025-04-20 22:08:00');

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
(20, 'dedewhacen@gmail.com', 'GCGP', 'L3', '$2b$12$aHk3S.AwkeBC52cD34NQVu9u.5HLoJ66b6Jxax7y87kfA0mDUqzqi'),
(20542, '20542@isme.esp.mr', 'GCGP', 'L3', '1234'),
(20543, '20543@isme.esp.mr', 'GEER', 'L3', '1234'),
(23501, '23501@isme.esp.mr', 'GCGP', 'L1', '$2b$12$Nt1lWb4Ny5.wcN1ufW330OYnrgx5yY8L0ifheWsdoAI2NAcdEvum.'),
(23502, '23502@isme.esp.mr', 'GEER', 'L2', '$2b$12$ucKvY7DR5ez9.ZxVqTwfzu8RzLXsJWGBSU1YiqaVKVFaejaYSfuT6'),
(23503, '23503@isme.esp.mr', 'GEER', 'L1', '123'),
(23504, '23504@isme.esp.mr', 'GCGP', 'L2', '$2b$12$islC0XCDkkiL1t.YxLahAuuAZqHN.on868yASsLD1Msy2/CnZ9rqm'),
(23542, '23542@isme.esp.mr', 'GCGP', 'L2', '$2b$12$TbJNf8jjz7Fe5ruc6S02ouEolv4l4r9V0GtXvM6WD7QGNlmskOlD6');

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
  `config_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_rec`),
  UNIQUE KEY `unique_reclamation` (`matricule_etd`,`code_mat`),
  KEY `matricule_etd` (`matricule_etd`),
  KEY `code_mat` (`code_mat`),
  KEY `idx_config_id` (`config_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=139 ;

--
-- Dumping data for table `reclamation`
--

INSERT INTO `reclamation` (`id_rec`, `Détails`, `Objet_rec`, `moment_de_creation`, `matricule_etd`, `code_mat`, `statut`, `config_id`) VALUES
(17, 'nnnnnnn', 'Devoir', '2025-04-05 00:00:00', 23502, 'GEER_34', 'Accepté', NULL),
(19, 'kalma \r\n', 'Examen', '2025-04-07 00:00:00', 23502, 'GEER_41', 'Refusé', NULL),
(21, '15\r\n', 'Devoir', '2025-04-08 00:00:00', 23502, 'GEER_45', 'Refusé', NULL),
(38, '2222', 'Examen', '2025-04-08 00:00:00', 23502, 'GEER_46', 'Refusé', NULL),
(66, '20/20/20', 'Devoir', '2025-04-08 16:45:21', 23502, 'HE_42', 'En attente', NULL),
(68, '20\r\n\r\n', 'Devoir', '2025-04-08 17:01:01', 23502, 'GEER_44', 'En attente', NULL),
(85, '20/20', 'Devoir', '2025-04-09 18:51:36', 23502, 'GEER_43', 'En attente', NULL),
(86, 'je pense mon note est 17', 'Devoir', '2025-04-10 21:49:33', 23501, 'HE_22', 'Accepté', NULL),
(87, 'j''ai trouve 0 ', 'TP', '2025-04-10 21:50:36', 23501, 'GCGP_22', 'Refusé', NULL),
(88, '20/20', 'Examen', '2025-04-10 21:51:14', 23501, 'ST_22', 'Refusé', NULL),
(89, 'c''est pas bon', 'Examen', '2025-04-10 22:24:45', 23501, 'GCGP_23', 'Accepté', NULL),
(108, 'qqqqqqqq', 'Examen', '2025-04-11 17:45:39', 23503, 'GEER_26', 'Refusé', NULL),
(109, '03 n8ava', 'Devoir', '2025-04-11 17:54:02', 23503, 'GEER_22', 'Accepté', NULL),
(110, '43', 'Examen', '2025-04-11 18:10:28', 20543, 'GEER_55', 'Accepté', NULL),
(111, '42', 'Examen', '2025-04-11 18:11:12', 20542, 'GCGP_57', 'Accepté', NULL),
(112, '222222', 'Examen', '2025-04-11 18:12:06', 23501, 'GCGP_25', 'Accepté', NULL),
(114, '02', 'Devoir', '2025-04-11 18:13:54', 23502, 'GEER_42', 'En attente', NULL),
(115, 'wwwwawww', 'Devoir', '2025-04-14 12:03:12', 23502, 'HE_41', 'Accepté', NULL),
(116, 'sssssssssssssss', 'Devoir', '2025-04-16 19:08:39', 23501, 'HE_23', 'En attente', NULL),
(117, 'hhhhh', 'Devoir', '2025-04-19 17:42:30', 23504, 'GCGP_42', 'En attente', NULL),
(120, '2002', 'Examen', '2025-04-19 18:10:54', 23504, 'GCGP_45', 'En attente', NULL),
(123, '04', 'Devoir', '2025-04-19 18:19:57', 23504, 'GCGP_44', 'En attente', NULL),
(124, 'joli', 'Devoir', '2025-04-19 18:52:01', 23504, 'HE_42', 'En attente', NULL),
(134, '04', 'Devoir, Examen', '2025-04-20 00:25:17', 23504, 'ST_41', 'En attente', 14),
(137, 'hhhhhhhhhhhhhhhhhhhhhh', 'TP', '2025-04-20 01:58:28', 23504, 'GCGP_41', 'Accepté', 14);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `email_admin` varchar(23) NOT NULL,
  `pwd_admin` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`email_admin`, `pwd_admin`) VALUES
('admin@isme.esp.mr', '$2b$12$.9bNk14onlywcKI/raiiDuH45oFdQ200Ea3sSL7aMltBO8Qo40YG2');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reclamation`
--
ALTER TABLE `reclamation`
  ADD CONSTRAINT `fk_config_id` FOREIGN KEY (`config_id`) REFERENCES `configuration_reclamation` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `reclamation_ibfk_1` FOREIGN KEY (`matricule_etd`) REFERENCES `etudiant` (`matricule_etd`),
  ADD CONSTRAINT `reclamation_ibfk_2` FOREIGN KEY (`code_mat`) REFERENCES `matiere` (`code_mat`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
