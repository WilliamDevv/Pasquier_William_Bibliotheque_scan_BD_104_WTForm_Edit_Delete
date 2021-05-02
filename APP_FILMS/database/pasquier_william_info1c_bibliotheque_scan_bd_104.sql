-- phpMyAdmin SQL Dump
-- version 4.5.4.1
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Ven 05 Mars 2021 à 20:08
-- Version du serveur :  5.7.11
-- Version de PHP :  5.6.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `pasquier_william_info1c_bibliotheque_scan_bd_104`
--

-- --------------------------------------------------------
--

-- Database: pasquier_william_info1c_bibliotheque_scan_bd_104
-- Détection si une autre base de donnée du même nom existe

DROP DATABASE IF EXISTS pasquier_william_info1c_bibliotheque_scan_bd_104;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS pasquier_william_info1c_bibliotheque_scan_bd_104;

-- Utilisation de cette base de donnée

USE pasquier_william_info1c_bibliotheque_scan_bd_104;

--
-- --------------------------------------------------------

--
-- Structure de la table `t_avis`
--

CREATE TABLE `t_avis` (
  `id_avis` int(11) NOT NULL,
  `avis_note` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_avis`
--

CREATE TABLE `t_avoir_avis` (
  `id_avoir_avis` int(11) NOT NULL,
  `fk_avis` int(11) NOT NULL,
  `fk_scan` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_langue`
--

CREATE TABLE `t_avoir_langue` (
  `id_avoir_langue` int(11) NOT NULL,
  `fk_langue` int(11) NOT NULL,
  `fk_scan` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_mail`
--

CREATE TABLE `t_avoir_mail` (
  `id_avoir_mail` int(11) NOT NULL,
  `fk_mail` int(11) NOT NULL,
  `fk_personne` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_avoir_mail`
--

INSERT INTO `t_avoir_mail` (`id_avoir_mail`, `fk_mail`, `fk_personne`) VALUES
(1, 1, 1);

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_maisondedition`
--

CREATE TABLE `t_avoir_maisondedition` (
  `id_avoir_maisondedition` int(11) NOT NULL,
  `fk_maisondedition` int(11) NOT NULL,
  `fk_scan` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_motdepasse`
--

CREATE TABLE `t_avoir_motdepasse` (
  `id_avoir_motDePasse` int(11) NOT NULL,
  `fk_motdepasse` int(11) NOT NULL,
  `fk_personne` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_pseudo`
--

CREATE TABLE `t_avoir_pseudo` (
  `id_avoir_pseudo` int(11) NOT NULL,
  `fk_pseudo` int(11) NOT NULL,
  `fk_personne` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_avoir_pseudo`
--

INSERT INTO `t_avoir_pseudo` (`id_avoir_pseudo`, `fk_pseudo`, `fk_personne`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 5),
(5, 5, 6);

-- --------------------------------------------------------

--
-- Structure de la table `t_mail`
--

CREATE TABLE `t_mail` (
  `id_mail` int(11) NOT NULL,
  `mail` varchar(320) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_mail`
--

INSERT INTO `t_mail` (`id_mail`, `mail`) VALUES
(1, 'wpasquier61@gmail.com');

-- --------------------------------------------------------

--
-- Structure de la table `t_maisondedition`
--

CREATE TABLE `t_maisondedition` (
  `id_maisondedition` int(11) NOT NULL,
  `maisonDEdition_nom` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_motdepasse`
--

CREATE TABLE `t_motdepasse` (
  `id_motDePasse` int(11) NOT NULL,
  `motDePasse` varchar(75) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_personne`
--

CREATE TABLE `t_personne` (
  `id_personne` int(11) NOT NULL,
  `pers_nom` varchar(40) NOT NULL,
  `pers_prenom` varchar(40) NOT NULL,
  `pers_dateDeNaissance` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_personne`
--

INSERT INTO `t_personne` (`id_personne`, `pers_nom`, `pers_prenom`, `pers_dateDeNaissance`) VALUES
(1, 'Pasquier', 'William', '2002-08-17'),
(2, 'Zeppeli', 'Jayro', '2021-03-03'),
(3, 'Cergneux', 'Wren', '2002-10-13'),
(4, 'Kira', 'Yoshikage', '2020-12-16'),
(5, 'Devis', 'Daniel', NULL),
(6, 'Larabe', 'Siphano', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `t_pseudo`
--

CREATE TABLE `t_pseudo` (
  `id_pseudo` int(11) NOT NULL,
  `pseudo` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_pseudo`
--

INSERT INTO `t_pseudo` (`id_pseudo`, `pseudo`) VALUES
(1, 'Homie'),
(2, 'JayroLeDozo'),
(3, 'WrenAvecPermis'),
(4, 'LeDozoAuGrosZGEG'),
(5, 'Siphano');

-- --------------------------------------------------------

--
-- Structure de la table `t_scan`
--

CREATE TABLE `t_scan` (
  `id_scan` int(11) NOT NULL,
  `scan_titre` varchar(40) NOT NULL,
  `scan_auteur` varchar(40) NOT NULL,
  `scan_dessinateur` varchar(40) NOT NULL,
  `scan_nombreDePages` int(3) NOT NULL,
  `scan_genre` varchar(40) NOT NULL,
  `scan_themes` varchar(40) NOT NULL,
  `scan_maisonDEdition` int(40) NOT NULL,
  `scan_langue` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_scan`
--

INSERT INTO `t_scan` (`id_scan`, `scan_titre`, `scan_auteur`, `scan_dessinateur`, `scan_nombreDePages`, `scan_genre`, `scan_themes`, `scan_maisonDEdition`, `scan_langue`) VALUES
(1, 'Berserk 01', 'Kentaro Miura', 'Kentaro Miura', 224, 'Seinen', 'Combat', 1, 'Français'),
(2, 'Berserk 01', 'Kentaro Miura', 'Kentaro Miura', 224, 'Seinen', 'Combat', 1, 'Français');

-- --------------------------------------------------------

--
-- Structure de la table `t_souhaiter_lire`
--

CREATE TABLE `t_souhaiter_lire` (
  `id_souhaiter_lire` int(11) NOT NULL,
  `fk_scan` int(11) NOT NULL,
  `fk_personne` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_souhaiter_lire`
--

INSERT INTO `t_souhaiter_lire` (`id_souhaiter_lire`, `fk_scan`, `fk_personne`) VALUES
(1, 1, 1);

-- --------------------------------------------------------

--
-- Structure de la table `t_telecharger`
--

CREATE TABLE `t_telecharger` (
  `id_telecharger` int(11) NOT NULL,
  `fk_scan` int(11) NOT NULL,
  `fk_personne` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_telecharger`
--

INSERT INTO `t_telecharger` (`id_telecharger`, `fk_scan`, `fk_personne`) VALUES
(1, 1, 1);

--
-- Index pour les tables exportées
--

--
-- Index pour la table `t_avis`
--
ALTER TABLE `t_avis`
  ADD PRIMARY KEY (`id_avis`);

--
-- Index pour la table `t_avoir_avis`
--
ALTER TABLE `t_avoir_avis`
  ADD PRIMARY KEY (`id_avoir_avis`),
  ADD KEY `fk_avis` (`fk_avis`),
  ADD KEY `fk_scan` (`fk_scan`);

--
-- Index pour la table `t_avoir_langue`
--
ALTER TABLE `t_avoir_langue`
  ADD PRIMARY KEY (`id_avoir_langue`),
  ADD KEY `fk_langue` (`fk_langue`),
  ADD KEY `fk_scan` (`fk_scan`);

--
-- Index pour la table `t_avoir_mail`
--
ALTER TABLE `t_avoir_mail`
  ADD PRIMARY KEY (`id_avoir_mail`),
  ADD KEY `fk_mail` (`fk_mail`),
  ADD KEY `fk_personne` (`fk_personne`);

--
-- Index pour la table `t_avoir_maisondedition`
--
ALTER TABLE `t_avoir_maisondedition`
  ADD PRIMARY KEY (`id_avoir_maisondedition`),
  ADD KEY `fk_maisondedition` (`fk_maisondedition`),
  ADD KEY `fk_scan` (`fk_scan`);

--
-- Index pour la table `t_avoir_motdepasse`
--
ALTER TABLE `t_avoir_motdepasse`
  ADD PRIMARY KEY (`id_avoir_motDePasse`),
  ADD KEY `fk_motdepasse` (`fk_motdepasse`),
  ADD KEY `fk_personne` (`fk_personne`);

--
-- Index pour la table `t_avoir_pseudo`
--
ALTER TABLE `t_avoir_pseudo`
  ADD PRIMARY KEY (`id_avoir_pseudo`),
  ADD KEY `fk_pseudo` (`fk_pseudo`),
  ADD KEY `fk_personne` (`fk_personne`);

--
-- Index pour la table `t_mail`
--
ALTER TABLE `t_mail`
  ADD PRIMARY KEY (`id_mail`);

--
-- Index pour la table `t_maisondedition`
--
ALTER TABLE `t_maisondedition`
  ADD PRIMARY KEY (`id_maisondedition`);

--
-- Index pour la table `t_motdepasse`
--
ALTER TABLE `t_motdepasse`
  ADD PRIMARY KEY (`id_motDePasse`);

--
-- Index pour la table `t_personne`
--
ALTER TABLE `t_personne`
  ADD PRIMARY KEY (`id_personne`);

--
-- Index pour la table `t_pseudo`
--
ALTER TABLE `t_pseudo`
  ADD PRIMARY KEY (`id_pseudo`);

--
-- Index pour la table `t_scan`
--
ALTER TABLE `t_scan`
  ADD PRIMARY KEY (`id_scan`);

--
-- Index pour la table `t_souhaiter_lire`
--
ALTER TABLE `t_souhaiter_lire`
  ADD PRIMARY KEY (`id_souhaiter_lire`),
  ADD KEY `fk_scan` (`fk_scan`),
  ADD KEY `fk_personne` (`fk_personne`);

--
-- Index pour la table `t_telecharger`
--
ALTER TABLE `t_telecharger`
  ADD PRIMARY KEY (`id_telecharger`),
  ADD KEY `fk_scan` (`fk_scan`),
  ADD KEY `fk_personne` (`fk_personne`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `t_avis`
--
ALTER TABLE `t_avis`
  MODIFY `id_avis` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_avoir_avis`
--
ALTER TABLE `t_avoir_avis`
  MODIFY `id_avoir_avis` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_avoir_langue`
--
ALTER TABLE `t_avoir_langue`
  MODIFY `id_avoir_langue` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_avoir_mail`
--
ALTER TABLE `t_avoir_mail`
  MODIFY `id_avoir_mail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `t_avoir_maisondedition`
--
ALTER TABLE `t_avoir_maisondedition`
  MODIFY `id_avoir_maisondedition` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_avoir_motdepasse`
--
ALTER TABLE `t_avoir_motdepasse`
  MODIFY `id_avoir_motDePasse` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_avoir_pseudo`
--
ALTER TABLE `t_avoir_pseudo`
  MODIFY `id_avoir_pseudo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT pour la table `t_mail`
--
ALTER TABLE `t_mail`
  MODIFY `id_mail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `t_maisondedition`
--
ALTER TABLE `t_maisondedition`
  MODIFY `id_maisondedition` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_motdepasse`
--
ALTER TABLE `t_motdepasse`
  MODIFY `id_motDePasse` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_personne`
--
ALTER TABLE `t_personne`
  MODIFY `id_personne` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT pour la table `t_pseudo`
--
ALTER TABLE `t_pseudo`
  MODIFY `id_pseudo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT pour la table `t_scan`
--
ALTER TABLE `t_scan`
  MODIFY `id_scan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_souhaiter_lire`
--
ALTER TABLE `t_souhaiter_lire`
  MODIFY `id_souhaiter_lire` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `t_telecharger`
--
ALTER TABLE `t_telecharger`
  MODIFY `id_telecharger` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `t_avoir_avis`
--
ALTER TABLE `t_avoir_avis`
  ADD CONSTRAINT `t_avoir_avis_ibfk_1` FOREIGN KEY (`fk_avis`) REFERENCES `t_avis` (`id_avis`),
  ADD CONSTRAINT `t_avoir_avis_ibfk_2` FOREIGN KEY (`fk_scan`) REFERENCES `t_scan` (`id_scan`);

--
-- Contraintes pour la table `t_avoir_mail`
--
ALTER TABLE `t_avoir_mail`
  ADD CONSTRAINT `t_avoir_mail_ibfk_1` FOREIGN KEY (`fk_mail`) REFERENCES `t_mail` (`id_mail`),
  ADD CONSTRAINT `t_avoir_mail_ibfk_2` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`);

--
-- Contraintes pour la table `t_avoir_motdepasse`
--
ALTER TABLE `t_avoir_motdepasse`
  ADD CONSTRAINT `t_avoir_motdepasse_ibfk_1` FOREIGN KEY (`fk_motdepasse`) REFERENCES `t_motdepasse` (`id_motDePasse`),
  ADD CONSTRAINT `t_avoir_motdepasse_ibfk_2` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`);

--
-- Contraintes pour la table `t_avoir_pseudo`
--
ALTER TABLE `t_avoir_pseudo`
  ADD CONSTRAINT `t_avoir_pseudo_ibfk_1` FOREIGN KEY (`fk_pseudo`) REFERENCES `t_pseudo` (`id_pseudo`),
  ADD CONSTRAINT `t_avoir_pseudo_ibfk_2` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`);

--
-- Contraintes pour la table `t_souhaiter_lire`
--
ALTER TABLE `t_souhaiter_lire`
  ADD CONSTRAINT `t_souhaiter_lire_ibfk_1` FOREIGN KEY (`fk_scan`) REFERENCES `t_scan` (`id_scan`),
  ADD CONSTRAINT `t_souhaiter_lire_ibfk_2` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`);

--
-- Contraintes pour la table `t_telecharger`
--
ALTER TABLE `t_telecharger`
  ADD CONSTRAINT `t_telecharger_ibfk_1` FOREIGN KEY (`fk_scan`) REFERENCES `t_scan` (`id_scan`),
  ADD CONSTRAINT `t_telecharger_ibfk_2` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`id_personne`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
