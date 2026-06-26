```markdown
# 📥 Panduan Instalasi Terpadu: Sistem Validasi RPS vs BAP

Dokumentasi ini wajib diikuti oleh seluruh anggota kelompok (Anggota 1-6) sebelum mulai menulis kode program. Panduan ini dibuat untuk memastikan environment pengembangan di setiap laptop seragam, guna menghindari error saat penggabungan kode (*code integration*).

---

## 🐍 Langkah 1: Instalasi Python (Semua Anggota)

### 🪟 Pengguna Windows
1. Unduh installer resmi melalui tautan berikut: [python.org/downloads](https://www.python.org/downloads/).
2. Buka file installer `.exe` yang sudah diunduh.
3. **⚠️ PERINGATAN KRUSIAL:** Pada jendela pertama installer, pastikan Anda mencentang kotak opsi **`[x] Add python.exe to PATH`** di bagian paling bawah sebelum mengklik tombol instal.
4. Klik **Install Now** dan tunggu hingga proses selesai.


```

*Atau, unduh paket instalasi resmi berformat `.pkg` melalui website Python.*

> **💡 Cara Memverifikasi Berhasil atau Tidak:**
> Buka Terminal / Command Prompt (CMD) di laptop Anda, lalu ketik perintah:
> `python --version`
> Jika muncul tulisan `Python 3.10.x` atau `Python 3.11.x`, berarti instalasi Anda telah sukses berjalan dengan benar.

---

## 📦 Langkah 2: Instalasi Dependensi Library via PIP (Semua Anggota)

Untuk meminimalkan potensi kegagalan impor modul (*ModuleNotFoundError*) saat integrasi, **seluruh anggota wajib menginstal semua paket library di bawah ini**.

Buka Terminal / Command Prompt di folder proyek Anda, lalu salin dan jalankan perintah tunggal berikut:

```bash
pip install mysql-connector-python tkcalendar fpdf2 PyPDF2 python-dotenv pyinstaller

```

### 📋 Distribusi Kebutuhan Library Berdasarkan Jobdesk Anggota:

* **Anggota 1 (UI/UX)**: Memerlukan komponen kalender dari paket `tkcalendar`.
* **Anggota 2 (Database)**: Memerlukan konektor driver `mysql-connector-python` dan pembaca variabel lingkungan `python-dotenv`.
* **Anggota 3 (Core Logic)**: Menggunakan modul bawaan Python (`re` dan `set`), tidak ada dependensi eksternal khusus.
* **Anggota 4 (PDF Extractor)**: Memerlukan modul pembaca berkas lewat `PyPDF2`.
* **Anggota 5 (Report Cetak)**: Memerlukan modul perancang dokumen dari `fpdf2`.
* **Anggota 6 (QA & Rilisan)**: Memerlukan paket kompilator program via `pyinstaller`.

---

## 🚨 Solusi Kilat Mengatasi Kendala Error Instalasi

Apabila ada anggota kelompok yang mengalami kendala saat inisialisasi awal, silakan gunakan panduan penyelesaian cepat di bawah ini:

### 1. Pesan Error: `"pip" is not recognized as an internal or external command`

* **Penyebab**: Anggota tersebut lupa mencentang opsi "Add Python to PATH" pada saat instalasi awal.
* **Solusi**: Buka kembali file installer Python yang diunduh sebelumnya, pilih opsi **Modify**, centang bagian **Add to PATH**, lalu selesaikan instruksinya. Alternatif lain, gunakan perintah awalan: `python -m pip install [nama_library]`.

### 2. Pesan Error: `ModuleNotFoundError: No module named 'mysql'`

* **Penyebab**: Library terpasang di komputer, namun VS Code menggunakan environment/interpreter Python yang berbeda dari sistem utama.
* **Solusi**: Tekan tombol kombinasi `Ctrl + Shift + P` di VS Code, ketik **Python: Select Interpreter**, lalu pilih versi Python utama (Global/System) yang memiliki jalur berkas sama dengan hasil instalasi Anda di awal.

### 3. Pesan Error: `Error 1049 (42000): Unknown database 'pbo_rps_bap'`

* **Penyebab**: Script Python mencoba melakukan jembatan koneksi, namun database fisik di phpMyAdmin belum dibuat.
* **Solusi**: Silakan masuk kembali ke browser Anda di alamat `localhost/phpmyadmin`, lalu buat satu database kosong dengan nama **`pbo_rps_bap`** (pastikan penulisan hurufnya kecil semua).

```
SELAMAT MENGERJAKAN
```