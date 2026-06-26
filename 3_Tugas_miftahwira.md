# 🗂️ Spesifikasi Tugas Anggota 3: Core NLP Matcher & Logic (`models.py`)

## 🎯 Fokus Utama
Membuat algoritma pemrosesan kata kunci pintar yang membandingkan materi di RPS dengan BAP secara adil, kebal terhadap variasi penulisan tanda baca, dan huruf besar/kecil.

## 🛠️ Rincian Fungsi Utama Class `Validator`:
1. `clean_text(text)`:
   - Menerima string mentah dari database.
   - Mengubah semua huruf menjadi kecil (*case-folding*).
   - Menggunakan Regular Expression (`re.sub`) untuk mengubah tanda baca pengganggu seperti `/`, `,`, `-`, `.`, dan enter (`\n`) menjadi spasi biasa.
   - Memecah kalimat menjadi kumpulan kata unik (`set`) dan membuang kata yang terlalu pendek (panjang < 3 huruf).
2. `validate()`:
   - Memanggil `db.fetch_all` untuk mengambil data dari tabel `rps` dan `bap`.
   - Mengubah data BAP menjadi dictionary berbasis nomor pertemuan untuk mempercepat pencarian.
   - Melakukan perulangan (`for`) terhadap data RPS.
   - Jika pertemuan yang sama ditemukan di BAP, lakukan operasi irisan set (`words_rps.intersection(words_bap)`).
   - Jika ada kata yang sama (> 0), set status menjadi **"Sesuai"**. Jika tidak ada, set status menjadi **"Tidak Sesuai"**. Jika data BAP kosong, set status menjadi **"Hilang"**.
   - Menghitung persentase kepatuhan kuliah dengan rumus: `(Total Sesuai / Total Pertemuan RPS) * 100`.

## 📥 Input & Output Data:
- **Input**: Membaca baris Dictionary hasil query dari tabel database via `DatabaseManager`.
- **Output**: Mengembalikan dua nilai (`return results, persen`), di mana `results` adalah List berisi Dictionary detail status per pertemuan.