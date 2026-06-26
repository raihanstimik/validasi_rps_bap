# 🗂️ Spesifikasi Tugas Anggota 6: QA, DevOps, & Integration Specialist

## 🎯 Fokus Utama
Menggabungkan potongan kode dari Anggota 1 hingga 5, menguji fungsionalitas alur sistem, menyusun dokumentasi repositori GitHub, serta melakukan distribusi aplikasi siap pakai.

## 🛠️ Rincian Alur Tugas & Pengujian:
1. **Integrasi Kode & Git Management**: Mengumpulkan file `main.py`, `database.py`, `models.py`, `pdf_extractor.py`, dan `report_generator.py` ke dalam satu direktori. Memastikan seluruh *import statement* antar file terhubung dengan benar tanpa error `ModuleNotFoundError`.
2. **Skenario Pengujian Sistem (Quality Assurance)**:
   - **Test 1**: Memasukkan file PDF RPS Dasar Pemrograman yang memiliki variasi spasi banyak dan tanda baca acak. Memastikan proses masuk database lancar.
   - **Test 2**: Memastikan tombol "Proses Validasi" tidak membeku (*stuck*) apabila database dalam keadaan kosong.
   - **Test 3**: Memastikan window aplikasi responsif (komponen tabel otomatis memanjang secara proporsional saat ukuran aplikasi ditarik penuh oleh user).
3. **Penyusunan Dokumentasi & Rilisan**:
   - Menulis file `README.md` utama di root folder berisi langkah instalasi library dan tata cara menjalankan aplikasi.
   - Membuat file konfigurasi dependensi `requirements.txt`.
   - Menggunakan perintah **PyInstaller** di terminal (`python -m PyInstaller --onedir --windowed main.py`) untuk mengompilasi seluruh kode kelompok menjadi satu folder distribusi mandiri yang berisi berkas file eksekusi klik langsung bernama `main.exe`.