# 🗂️ Spesifikasi Tugas Anggota 1: UI/UX & Main Interface (`main.py`)

## 🎯 Fokus Utama
Membangun tampilan aplikasi (GUI) yang simple, minimalis, dan responsif menggunakan Tkinter grid layout,

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
