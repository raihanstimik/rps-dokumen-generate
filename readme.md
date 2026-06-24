# 📝 Sistem Penyusunan Dokumen RPS (Rencana Pembelajaran Semester)

Sistem Penyusunan Dokumen RPS adalah aplikasi berbasis web yang dirancang khusus untuk membantu dosen atau staf akademik di **STMIK Mardira Indonesia** dalam menyusun, mengelola, dan mencetak dokumen Rencana Pembelajaran Semester (RPS) secara terstruktur, dinamis, dan otomatis menjadi berkas siap cetak berformat PDF.

Aplikasi ini dibangun menggunakan framework **Flask (Python)** untuk sisi *backend*, **Tailwind CSS** untuk antarmuka pengguna (*frontend*) yang responsif, serta **MySQL** sebagai penyimpanan basis data. Untuk pembuatan dokumen PDF, aplikasi ini memanfaatkan pustaka **FPDF**.

---

## ✨ Fitur Utama

- **Manajemen Identitas Mata Kuliah:** Memungkinkan pengisian nama mata kuliah, kode, semester berjalan, hingga tanggal penyusunan dengan konversi format otomatis (`YYYY-MM-DD` ke `DD-MM-YYYY`).
- **Input Sesi Dinamis per Pertemuan:** Menambahkan baris sesi perkuliahan secara berurutan, lengkap dengan input Kalender Tanggal Sesi terdedikasi di atas nomor pertemuan.
- **Tampilan Tabel Preview Terpisah:** Kolom **Sesi** dan **Tanggal** ditampilkan secara terpisah di panel pratinjau web untuk mempermudah pemeriksaan jadwal sebelum dicetak.
- **Ekspor Resmi ke PDF (A4):** Menghasilkan dokumen PDF berstandar dengan Kop Surat resmi STMIK Mardira Indonesia, kalkulasi tinggi baris tabel otomatis secara matematis (*auto-wrap text*), pembatas halaman pintar (*auto page break protection*), serta *footer* halaman dinamis.
- **Penamaan File Pintar:** Berkas PDF yang diunduh otomatis diberi nama sesuai dengan nama mata kuliah yang sedang aktif (contoh: `RPS_PEMROGRAMAN_BERORIENTASI_OBJEK.pdf`).
- **Reset Form Instan:** Tombol kliring data untuk mengosongkan formulir identitas dan menghapus seluruh isi tabel sesi sekaligus dengan proteksi konfirmasi pop-up.

---

## 🚀 Teknologi yang Digunakan

- **Backend:** Python 3.x, Flask
- **Frontend:** HTML5, Tailwind CSS (via CDN)
- **Database:** MySQL, PyMySQL (sebagai database driver)
- **PDF Generator:** FPDF (Pustaka Python)

---

## 📁 Struktur Repositori

```text
├── app.py               # Berkas utama aplikasi Flask (Routing & Logika PDF)
├── templates/
│   └── index.html       # Antarmuka web utama (Form & Live Preview Tabel)
├── README.md            # Dokumentasi proyek (File ini)
└── database.sql         # (Opsional) Berkas dump/struktur database MySQL

```

---

## 🛠️ Langkah Instalasi dan Penggunaan

### 1. Prasyarat

Pastikan Anda sudah menginstal **Python 3** dan server database lokal seperti **XAMPP / Laragon** di komputer Anda.

### 2. Kloning Repositori

```bash
git clone [https://github.com/USERNAME_ANDA/NAMA_REPOSITORI.git](https://github.com/USERNAME_ANDA/NAMA_REPOSITORI.git)
cd NAMA_REPOSITORI

```

### 3. Instalasi Pustaka (Dependencies)

Instal pustaka Python yang diperlukan melalui terminal/CMD:

```bash
pip install flask pymysql fpdf

```

### 4. Konfigurasi Database

1. Nyalakan **Apache** dan **MySQL** di XAMPP/Laragon Anda.
2. Buka `http://localhost/phpmyadmin/` dan buat database baru bernama `rps_db`.
3. Buat dua tabel utama berikut:
**Tabel `detail_mata_kuliah`:**
```sql
CREATE TABLE detail_mata_kuliah (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_mk VARCHAR(255) NULL,
    semester VARCHAR(50) NULL,
    tgl_penyusunan VARCHAR(50) NULL,
    tgl_raw DATE NULL
);
-- Masukkan satu baris data default awal
INSERT INTO detail_mata_kuliah (id, nama_mk, semester, tgl_penyusunan, tgl_raw) 
VALUES (1, '', '', '', NULL);

```


**Tabel `sesi_rps`:**
```sql
CREATE TABLE sesi_rps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    no_sesi VARCHAR(20) NOT NULL,
    tgl_sesi VARCHAR(30) NULL,
    sub_cp_mk TEXT NOT NULL,
    sub_pokok_bahasan TEXT NOT NULL
);

```



### 5. Menjalankan Aplikasi

Jalankan file `app.py` menggunakan terminal:

```bash
python app.py

```

Buka browser kesayangan Anda dan akses tautan lokal berikut:

```text
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

```

---

## 📸 Pratinjau Alur Kerja Aplikasi

1. **Langkah 1:** Isi Identitas Mata Kuliah lalu klik "Simpan & Lanjutkan". Banner gelap di bagian atas akan aktif menampilkan mata kuliah terpilih.
2. **Langkah 2:** Form Sesi akan terbuka secara otomatis. Masukkan Tanggal Sesi melalui kalender picker, Nomor Sesi, isi Sub-CP-MK, dan Pokok Bahasan materi, lalu klik "Tambahkan Sesi Ke Tabel".
3. **Pratinjau & Cetak:** Cek susunan jadwal pada tabel preview di bagian kanan. Jika sudah sesuai, klik tombol "Cetak Dokumen RPS" di bagian pojok kanan atas untuk membuka atau mengunduh PDF resminya.

---

## 📜 Lisensi

Proyek ini dikembangkan untuk kebutuhan internal akademik dan administrasi perkuliahan di lingkungan **STMIK Mardira Indonesia**. Silakan digunakan dan dimodifikasi sesuai kebutuhan pengembangan lebih lanjut.

```

### 💡 Tips Sebelum Melakukan Push ke GitHub:
1. Ganti tulisan `USERNAME_ANDA` dan `NAMA_REPOSITORI` pada bagian Langkah 2 di atas dengan username dan nama repositori asli milik Anda di GitHub.
2. Anda bisa menambahkan file `.gitignore` berisi baris `__pycache__/` agar folder cache Python tidak ikut terunggah ke repositori GitHub Anda.

```