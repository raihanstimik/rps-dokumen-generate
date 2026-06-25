-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 24 Jun 2026 pada 22.10
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rps_db`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `detail_mata_kuliah`
--

CREATE TABLE `detail_mata_kuliah` (
  `id` int(11) NOT NULL DEFAULT 1,
  `nama_mk` varchar(150) DEFAULT NULL,
  `semester` varchar(20) DEFAULT NULL,
  `tgl_penyusunan` varchar(30) DEFAULT NULL,
  `tgl_raw` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `detail_mata_kuliah`
--

INSERT INTO `detail_mata_kuliah` (`id`, `nama_mk`, `semester`, `tgl_penyusunan`, `tgl_raw`) VALUES
(1, '', '', '', NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `sesi_rps`
--

CREATE TABLE `sesi_rps` (
  `id` int(11) NOT NULL,
  `no_sesi` varchar(10) NOT NULL,
  `tgl_sesi` varchar(30) DEFAULT NULL,
  `sub_cp_mk` text NOT NULL,
  `sub_pokok_bahasan` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `detail_mata_kuliah`
--
ALTER TABLE `detail_mata_kuliah`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `sesi_rps`
--
ALTER TABLE `sesi_rps`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `sesi_rps`
--
ALTER TABLE `sesi_rps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
