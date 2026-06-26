# 🗂️ Spesifikasi Tugas Anggota 6: QA, DevOps, & Integration Specialist

* **Fokus Utama:** Melakukan penggabungan kode (*code integration*), melakukan uji kelayakan skenario pergeseran sesi, dan mengurus distribusi rilis.
* **Komponen Spesifik yang Harus Dibuat:**
    * **File Dependensi (`requirements.txt`)**: Menyusun daftar pustaka pihak ketiga.
    * **Checklist Pengujian Spesifik:**
        * Memuji input manual tanggal menggunakan widget kalender, memastikan format tanggal tersimpan dengan benar di database.
        * **Uji Kasus Toleransi Sesi:** Menginput materi "Variabel" di RPS Sesi 1, lalu menginput materi "Variabel" di BAP Sesi 3. Memastikan saat tombol validasi diklik, baris Sesi 1 sukses berwarna hijau (**Sesuai**) dengan keterangan pendukung pergeseran sesi.
        * Memastikan tombol `💥 Reset Semua Data` membersihkan seluruh tabel MySQL secara aman tanpa menyisakan cache data tanggal.
    * **Kompilasi Aplikasi**: Menjalankan perintah PyInstaller untuk menghasilkan file siap pakai `main.exe`.
