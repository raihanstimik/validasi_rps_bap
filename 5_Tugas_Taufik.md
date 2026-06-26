# 🗂️ Spesifikasi Tugas Anggota 4: PDF Data Extractor (`pdf_extractor.py`)

## 🎯 Fokus Utama
Membuka dokumen file PDF fisik (RPS/BAP) yang dipilih oleh user, mengekstrak baris teks mentahnya, memilah datanya, lalu menyimpannya secara otomatis ke database MySQL.

## 🛠️ Rincian Fungsi Utama Class `PDFExtractor`:
1. `extract_rps_to_db(file_path)`:
   - Membuka dokumen PDF menggunakan library seperti `PyPDF2` atau `pdfplumber`.
   - Melakukan looping membaca teks dari setiap halaman.
   - Menggunakan logika pencarian baris atau pemisahan string (*string splitting*) untuk mendeteksi teks "Pertemuan" dan "Materi/Pokok Bahasan".
   - Melakukan query `INSERT INTO rps (pertemuan, pokok_bahasan) VALUES (%s, %s)` memanfaatkan class database milik Anggota 2.
2. `extract_bap_from_pdf(file_path)`:
   - Membuka berkas PDF realisasi perkuliahan/BAP.
   - Membaca dan memilah teks nomor pertemuan dan materi yang diajarkan dosen.
   - Melakukan query `INSERT INTO bap (pertemuan, materi) VALUES (%s, %s)`.

## 📥 Input & Output Data:
- **Input**: String alamat lokasi file (`file_path`) yang didapatkan dari tombol *filedialog* milik Anggota 1.
- **Output**: Mengembalikan nilai INT berupa total jumlah baris data yang sukses dimasukkan ke database untuk memicu notifikasi sukses di GUI.