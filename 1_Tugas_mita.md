# 🗂️ Spesifikasi Tugas Anggota 1: UI/UX & Main Interface (`main.py`)

## 🎯 Fokus Utama
Membangun tampilan aplikasi (GUI) yang simple, minimalis, dan responsif menggunakan Tkinter grid layout, serta menggabungkan seluruh modul dari anggota lain ke dalam satu window utama.

## 🛠️ Rincian Komponen GUI yang Harus Dibuat:
1. **Window Utama (`tk.Tk`)**: Ukuran default `1100x650` piksel, warna latar belakang terang/bersih (`#F8F9FA`), dapat ditarik/diperbesar (resizable).
2. **Header Panel**: Area atas dengan warna kontras profesional (`#1E3A8A`) berisi judul aplikasi yang tebal.
3. **Control Panel**: Barisan tombol minimalis yang disusun secara horizontal:
   - Tombol `📄 Load RPS (PDF)` (Warna Hijau) -> Terhubung ke fungsi Anggota 4.
   - Tombol `📋 Upload BAP (PDF)` (Warna Ungu) -> Terhubung ke fungsi Anggota 4.
   - Tombol `🔍 Proses Validasi` (Warna Biru) -> Terhubung ke fungsi Anggota 3.
   - Tombol `📥 Cetak Laporan` (Warna Merah) -> Terhubung ke fungsi Anggota 5.
4. **Main Output Area**: Menggunakan sistem kolom grid (`weight`) sehingga saat window diperbesar, area ini ikut melebar:
   - **Sisi Kiri (Tabel `ttk.Treeview`)**: Memiliki kolom Pertemuan, Materi RPS, Materi BAP, Status, dan Keterangan. Wajib memiliki tag warna baris: Sesuai (Hijau Muda), Tidak Sesuai (Kuning Muda), Hilang (Merah Muda).
   - **Sisi Kanan (Live Terminal Log)**: Widget `tk.Text` dengan latar belakang hitam (`#111827`) dan teks hijau (`#10B981`) bergaya font `Consolas` untuk memantau aktivitas sistem.

## 📥 Input & Output Data:
- **Input**: Klik tombol aksi dari user.
- **Output**: Memperbarui baris data pada tabel Treeview dan mencetak baris log baru ke widget terminal.