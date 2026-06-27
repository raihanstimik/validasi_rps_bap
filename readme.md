markdown
#  Panduan Instalasi Terpadu: Sistem Validasi RPS vs BAP

## Langkah 1: Instalasi Dependensi Library via PIP (Semua Anggota)

Untuk meminimalkan potensi kegagalan impor modul (*ModuleNotFoundError*) saat integrasi, **seluruh anggota wajib menginstal semua paket library di bawah ini**.

Buka Terminal / Command Prompt di folder proyek Anda, lalu salin dan jalankan perintah tunggal berikut:

```bash
pip install mysql-connector-python tkcalendar fpdf2 PyPDF2 python-dotenv pyinstaller

```

## SISTEM VALIDASI KESESUAIAN RPS VS BAP PINTAR (BERBASIS NLP MATCHER)

---

## 📌 1. Deskripsi Umum Proyek
Proyek ini bertujuan untuk membangun aplikasi desktop manajemen mutu akademik. Aplikasi ini memvalidasi kesesuaian materi antara dokumen **Rencana Pembelajaran Semester (RPS)** dan **Berita Acara Perkuliahan (BAP)**. 

Sistem mendukung input otomatis (PDF Extractor) dan input manual (Form GUI dengan penentu Tanggal Kalender). Aplikasi ini mengadopsi tabel matriks formal dengan kolom Tanggal Terintegrasi, Live Log Terminal mode terang (*Light Mode*), serta **Logika Toleransi Pergeseran Sesi** (Materi RPS sesi X tetap dinyatakan *Valid/Sesuai* meskipun baru diajarkan di BAP pada sesi Y).

---

## 👥 2. Matriks Struktur Tim & Spesifikasi Berkas Kerja (Sangat Rinci)

### 👤 tugas 1: UI/UX & Interface Engineer (`main.py`)
* **Fokus Utama:** Menyusun tata letak jendela utama yang minimalis, responsif (menggunakan Tkinter `grid`), dan mengintegrasikan seluruh fungsi tombol serta komponen kalender.
* **Komponen Spesifik yang Harus Dibuat:**
    * **Main Window (`tk.Tk`)**: Batasan ukuran `1250x700` piksel, warna latar belakang abu-abu terang (`#F3F4F6`).
    * **Left Panel (Form Input Manual BAP)**: `tk.LabelFrame` berisi:
        * `Entry` No Sesi / Pertemuan.
        * `DateEntry` (`tkcalendar`) untuk memilih **Tanggal Sesi Perkuliahan** secara visual.
        * `Entry` Pokok Bahasan BAP.
        * `Text` Materi BAP.
        * Tombol `➕ Tambahkan BAP` dan `🧹 Bersihkan Form`.
    * **Right Top Panel (Tabel Matriks Berkolom Tanggal)**: Komponen `ttk.Treeview` dengan kolom yang diperluas: `NO SESI`, `TANGGAL`, `POKOK BAHASAN (RPS)`, `MATERI (RPS)`, `POKOK BAHASAN (BAP)`, `MATERI (BAP)`, `STATUS`, dan `KETERANGAN`. Wajib memiliki tag warna baris otomatis (Hijau/Kuning/Merah).
    * **Right Bottom Panel (Light Mode Live Log)**: Komponen `tk.Text` dengan latar belakang krem lembut (`#FFFBEB`) dan teks warna biru tua (`#1E3A8A`) untuk pelacakan sistem.

### 👤 tugas 2: Database Administrator & CRUD Engineer (`database.py`)
* **Fokus Utama:** Mengelola siklus hidup koneksi basis data MySQL lokal (XAMPP) dan memastikan struktur tabel mendukung pencatatan tipe data tanggal (`DATE`).
* **Komponen Spesifik yang Harus Dibuat:**
    * **Inisialisasi Tabel `rps`**: Kolom `pertemuan` (INT PK), `pokok_bahasan` (VARCHAR 255), dan `materi_rps` (TEXT).
    * **Inisialisasi Tabel `bap`**: Kolom `pertemuan` (INT PK), `tanggal` (DATE), `pokok_bahasan_bap` (VARCHAR 255), dan `materi` (TEXT).
    * **Fungsi `execute_query` & `fetch_all`**: Mengamankan penyimpanan string tanggal format `YYYY-MM-DD` dari GUI ke MySQL serta mendukung aksi `TRUNCATE TABLE` untuk fitur tombol **Reset Semua Data**.

### 👤 tugas 3: NLP Matcher & Cross-Session Logic Architect (`models.py`)
* **Fokus Utama:** Merancang algoritma pembersihan string dan **Logika Pencarian Lintas Sesi (Cross-Session Matching)**.
* **Komponen Spesifik yang Harus Dibuat:**
    * **Fungsi `clean_text(text)`**: Mengubah string ke lowercase, menghapus tanda baca (`/`, `,`, `-`, `.`) via Regex menjadi spasi, dan memecah kalimat menjadi kumpulan kata unik (`set`).
    * **Fungsi `validate()` dengan Logika Toleransi Pergeseran Sesi**:
        * Sistem pertama-tama akan mengecek kecocokan materi pada nomor sesi yang sama (Sesi RPS 1 vs Sesi BAP 1).
        * **Logika Tambahan (Pencarian Lintas Sesi):** Jika pada sesi yang sama tidak cocok, sistem tidak langsung memberikan status "Tidak Sesuai". Sistem akan melakukan *scanning* (pencarian sekunder) ke seluruh sesi BAP lainnya. 
        * Jika materi RPS Sesi 1 ternyata ditemukan di BAP Sesi 3, sistem akan tetap menetapkan status **"Sesuai"** dengan catatan otomatis di kolom Keterangan: *"Valid! Materi diajarkan bergeser pada Sesi 3"*.
    * **Kalkulator Kepatuhan**: Menghitung persentase kelayakan akhir berdasarkan total materi yang berhasil terlaksana.

### 👤 tugas 4: PDF Data Extractor (`pdf_extractor.py`)
* **Fokus Utama:** Mengurus penyerapan berkas dokumen luar berbentuk PDF (RPS maupun BAP) menggunakan library `PyPDF2` atau `pdfplumber`.
* **Komponen Spesifik yang Harus Dibuat:**
    * **Fungsi `extract_rps_to_db(file_path)`**: Membaca dokumen cetak RPS, memilah teks Pokok Bahasan dan Materi RPS per sesi, lalu menyimpannya ke database.
    * **Fungsi `extract_bap_to_db(file_path)`**: Membaca dokumen PDF Berita Acara cetakan sistem kampus, mengekstrak teks tanggal, pokok bahasan, dan materi secara otomatis ke dalam tabel `bap`.

### 👤 tugas 5: Report Document Generator (`report_generator.py`)
* **Fokus Utama:** Menyusun layout berkas fisik cetak laporan kelayakan resmi berformat PDF berkolom tanggal menggunakan library `FPDF2`.
* **Komponen Spesifik yang Harus Dibuat:**
    * **Fungsi `export_report(file_path, results, persen)`**: Menerima data matriks lengkap dari GUI termasuk variabel tanggal.
    * **Desain Lembar Cetak**: Membuat kop resmi, mencetak skor persentase kelayakan, dan menyusun grid tabel berkolom tanggal yang presisi. Menggunakan fungsi `multi_cell` untuk mencegah teks terpotong dan filter biner `.encode('latin-1', 'replace')` agar terhindar dari *crash* karakter asing.

### 👤 tugas 6: Quality Assurance (QA) & DevOps Specialist
* **Fokus Utama:** Melakukan penggabungan kode (*code integration*), melakukan uji kelayakan skenario pergeseran sesi, dan mengurus distribusi rilis.
* **Komponen Spesifik yang Harus Dibuat:**
    * **File Dependensi (`requirements.txt`)**: Menyusun daftar pustaka pihak ketiga.
    * **Checklist Pengujian Spesifik:**
        * Memuji input manual tanggal menggunakan widget kalender, memastikan format tanggal tersimpan dengan benar di database.
        * **Uji Kasus Toleransi Sesi:** Menginput materi "Variabel" di RPS Sesi 1, lalu menginput materi "Variabel" di BAP Sesi 3. Memastikan saat tombol validasi diklik, baris Sesi 1 sukses berwarna hijau (**Sesuai**) dengan keterangan pendukung pergeseran sesi.
        * Memastikan tombol `💥 Reset Semua Data` membersihkan seluruh tabel MySQL secara aman tanpa menyisakan cache data tanggal.
    * **Kompilasi Aplikasi**: Menjalankan perintah PyInstaller untuk menghasilkan file siap pakai `main.exe`.

---

## ⏱️ 3. Urutan Alur Implementasi (Timeline Kerja Paralel Aman)

```text
[FASE 1: PONDASI & STRUKTUR TANGGAL]
 ├── Anggota 2: Menyelesaikan skema DB mendukung tipe data DATE & file database.py 
 └── Anggota 1: Mendesain Form GUI dengan widget tkcalendar, Matriks Kolom Tanggal, & Log Terang 

[FASE 2: PARSING DATA & LOGIKA LINTAS SESI]
 ├── Anggota 4: Membuat parser pembaca dokumen PDF termasuk ekstraksi teks tanggal 
 └── Anggota 3: Membuat core NLP & Algoritma validasi pencarian Lintas Sesi 

[FASE 3: LAPORAN CETAK & RILIS EXE]
 ├── Anggota 5: Membuat layout cetak dokumen PDF dari data matriks berkolom tanggal 
 └── Anggota 6: Integrasi kode seluruh file, uji coba bug skenario pergeseran materi, & build EXE 


```
SELAMAT MENGERJAKAN
```
