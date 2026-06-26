# 🗂️ Spesifikasi Tugas Anggota 3: Core NLP Matcher & Logic (`models.py`)

* **Fokus Utama:** Merancang algoritma pembersihan string dan **Logika Pencarian Lintas Sesi (Cross-Session Matching)**.
* **Komponen Spesifik yang Harus Dibuat:**
    * **Fungsi `clean_text(text)`**: Mengubah string ke lowercase, menghapus tanda baca (`/`, `,`, `-`, `.`) via Regex menjadi spasi, dan memecah kalimat menjadi kumpulan kata unik (`set`).
    * **Fungsi `validate()` dengan Logika Toleransi Pergeseran Sesi**:
        * Sistem pertama-tama akan mengecek kecocokan materi pada nomor sesi yang sama (Sesi RPS 1 vs Sesi BAP 1).
        * **Logika Tambahan (Pencarian Lintas Sesi):** Jika pada sesi yang sama tidak cocok, sistem tidak langsung memberikan status "Tidak Sesuai". Sistem akan melakukan *scanning* (pencarian sekunder) ke seluruh sesi BAP lainnya. 
        * Jika materi RPS Sesi 1 ternyata ditemukan di BAP Sesi 3, sistem akan tetap menetapkan status **"Sesuai"** dengan catatan otomatis di kolom Keterangan: *"Valid! Materi diajarkan bergeser pada Sesi 3"*.
    * **Kalkulator Kepatuhan**: Menghitung persentase kelayakan akhir berdasarkan total materi yang berhasil terlaksana.
