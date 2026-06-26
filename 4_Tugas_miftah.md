# 🗂️ Spesifikasi Tugas Anggota 5: Report PDF Generator (`report_generator.py`)

## 🎯 Fokus Utama
Mengambil data cache hasil komparasi terakhir dari window utama, lalu merancangnya menjadi dokumen berkas PDF resmi yang siap dicetak dan ditandatangani.

## 🛠️ Rincian Fungsi Utama Class `ReportGenerator`:
1. `export_report(file_path, results, persen)`:
   - Menerima data hasil validasi dari GUI utama.
   - Menginisialisasi dokumen baru menggunakan library `fpdf2` (`FPDF()`).
2. **Desain Tata Letak Halaman PDF**:
   - **Header**: Membuat kotak latar warna biru formal, teks judul besar, nama instansi, dan garis pembatas tebal.
   - **Summary Card**: Menuliskan tanggal cetak, total pertemuan yang diperiksa, dan angka persentase kelayakan (gunakan warna hijau jika $\ge 75\%$ dan merah jika $< 75\%$).
   - **Detail Table**: Membuat kolom tabel PDF (`pdf.cell`). Lakukan looping terhadap data `results`. Gunakan fungsi `pdf.set_fill_color` untuk mewarnai latar baris tabel sesuai status agar sinkron dengan warna di aplikasi GUI.
   - **Text Wrapping**: Wajib menggunakan fungsi `pdf.multi_cell` pada kolom keterangan agar kalimat penjelasan yang panjang otomatis turun ke bawah dan tidak terpotong keluar dari kertas PDF.
   - **Pembersihan String Anti-Crash**: Membuat fungsi internal `clean_pdf_text` untuk menyaring string menggunakan teknik `.encode('latin-1', 'replace').decode('latin-1')` guna memastikan karakter tanda baca tersembunyi (seperti em-dash `—`) tidak merusak proses *rendering* halaman.