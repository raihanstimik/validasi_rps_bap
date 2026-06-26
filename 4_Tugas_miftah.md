# 🗂️ Spesifikasi Tugas Anggota 5: Report PDF Generator (`report_generator.py`)

* **Fokus Utama:** Menyusun layout berkas fisik cetak laporan kelayakan resmi berformat PDF berkolom tanggal menggunakan library `FPDF2`.
* **Komponen Spesifik yang Harus Dibuat:**
    * **Fungsi `export_report(file_path, results, persen)`**: Menerima data matriks lengkap dari GUI termasuk variabel tanggal.
    * **Desain Lembar Cetak**: Membuat kop resmi, mencetak skor persentase kelayakan, dan menyusun grid tabel berkolom tanggal yang presisi. Menggunakan fungsi `multi_cell` untuk mencegah teks terpotong dan filter biner `.encode('latin-1', 'replace')` agar terhindar dari *crash* karakter asing.
