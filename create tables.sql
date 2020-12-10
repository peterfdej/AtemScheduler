-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Gegenereerd op: 02 dec 2020 om 18:24
-- Serverversie: 8.0.22
-- PHP-versie: 8.0.0RC4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Atemdb`
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `host`
--

CREATE TABLE `host` (
  `hostname` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `schedules`
--

CREATE TABLE `schedules` (
  `id` bigint NOT NULL,
  `swtime` time NOT NULL,
  `swdate` date NOT NULL,
  `scene` varchar(255) NOT NULL,
  `transition` varchar(255) NOT NULL,
  `duration` time NOT NULL,
  `repeattime` varchar(25) NOT NULL,
  `processed` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `host`
--
ALTER TABLE `host`
  ADD PRIMARY KEY (`hostname`);

--
-- Indexen voor tabel `schedules`
--
ALTER TABLE `schedules`
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT voor een tabel `schedules`
--
ALTER TABLE `schedules`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
