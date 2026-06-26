# 🗂️ Spesifikasi Tugas Anggota 2: Database Administrator (`database.py`)

* **Fokus Utama:** Mengelola siklus hidup koneksi basis data MySQL lokal (XAMPP) dan memastikan struktur tabel mendukung pencatatan tipe data tanggal (`DATE`).
* **Komponen Spesifik yang Harus Dibuat:**
    * **Inisialisasi Tabel `rps`**: Kolom `pertemuan` (INT PK), `pokok_bahasan` (VARCHAR 255), dan `materi_rps` (TEXT).
    * **Inisialisasi Tabel `bap`**: Kolom `pertemuan` (INT PK), `tanggal` (DATE), `pokok_bahasan_bap` (VARCHAR 255), dan `materi` (TEXT).
    * **Fungsi `execute_query` & `fetch_all`**: Mengamankan penyimpanan string tanggal format `YYYY-MM-DD` dari GUI ke MySQL serta mendukung aksi `TRUNCATE TABLE` untuk fitur tombol **Reset Semua Data**.
