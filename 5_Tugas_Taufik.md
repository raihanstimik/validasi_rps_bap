# 🗂️ Spesifikasi Tugas Anggota 4: PDF Data Extractor (`pdf_extractor.py`)

* **Fokus Utama:** Mengurus penyerapan berkas dokumen luar berbentuk PDF (RPS maupun BAP) menggunakan library `PyPDF2` atau `pdfplumber`.
* **Komponen Spesifik yang Harus Dibuat:**
    * **Fungsi `extract_rps_to_db(file_path)`**: Membaca dokumen cetak RPS, memilah teks Pokok Bahasan dan Materi RPS per sesi, lalu menyimpannya ke database.
    * **Fungsi `extract_bap_to_db(file_path)`**: Membaca dokumen PDF Berita Acara cetakan sistem kampus, mengekstrak teks tanggal, pokok bahasan, dan materi secara otomatis ke dalam tabel `bap`.
