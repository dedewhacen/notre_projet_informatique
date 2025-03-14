-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Mar 14, 2025 at 12:22 PM
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
  `Semestre` varchar(50) NOT NULL,
  PRIMARY KEY (`matricule_etd`),
  UNIQUE KEY `Email` (`Email`)
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

--
-- Dumping data for table `matiér`
--

INSERT INTO `matiér` (`code_mat`, `nom_mat`) VALUES
('GCGP15', 'GCGP15'),
('GEER34', 'GEER34'),
('HE_11', 'HE_11'),
('HE_12', 'HE_12'),
('HE_13', 'HE_13'),
('HE_22', 'HE_22'),
('ST_11', 'ST_11'),
('ST_12', 'ST_12'),
('ST_13', 'ST_13');

-- --------------------------------------------------------

--
-- Table structure for table `réclamation`
--

CREATE TABLE IF NOT EXISTS `réclamation` (
  `id_rec` int(11) NOT NULL AUTO_INCREMENT,
  `Détails` varchar(50) NOT NULL,
  `Objet_rec` varchar(50) NOT NULL,
  `moment_de_creation` date NOT NULL,
  `matricule_etd` int(11) NOT NULL,
  `code_mat` varchar(50) DEFAULT NULL,
  `statut` varchar(20) DEFAULT 'En attente',
  PRIMARY KEY (`id_rec`),
  KEY `matricule_etd` (`matricule_etd`),
  KEY `code_mat` (`code_mat`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=18 ;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `email` varchar(23) NOT NULL,
  `pwd` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`email`, `pwd`) VALUES
('23501@isme.esp.mr', '2350123501'),
('23502@isme.esp.mr', '2350223502'),
('23503@isme.esp.mr', '2350323503'),
('23504@isme.esp.mr', '2350423504'),
('23505@isme.esp.mr', '2350523505'),
('23506@isme.esp.mr', '2350623506'),
('23507@isme.esp.mr', '2350723507'),
('23508@isme.esp.mr', '2350823508'),
('23509@isme.esp.mr', '2350923509'),
('23510@isme.esp.mr', '2351023510');

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
