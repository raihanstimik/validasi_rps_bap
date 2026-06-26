# 🗂️ Spesifikasi Tugas Anggota 2: Database Administrator (`database.py`)

## 🎯 Fokus Utama
Mengelola siklus hidup koneksi database MySQL, eksekusi penyimpanan, dan pengambilan data secara aman agar tidak menyebabkan aplikasi membeku (*freeze*).

## 📊 Struktur Tabel MySQL yang Harus Disiapkan:
1. **Tabel `rps`**:
   - `pertemuan` (INT atau VARCHAR, Primary Key/Identifier)
   - `pokok_bahasan` (TEXT / LONGTEXT)
2. **Tabel `bap`**:
   - `pertemuan` (INT atau VARCHAR)
   - `materi` (TEXT / LONGTEXT)

## 🛠️ Rincian Fungsi Utama Class `DatabaseManager`:
1. `__init__()`: Menyimpan konfigurasi kredensial (Host, User, Password, Database Name).
2. `connect()`: Melakukan jembatan koneksi ke MySQL menggunakan `mysql.connector`. Wajib menyertakan parameter `dictionary=True` pada objek cursor agar data yang ditarik berbentuk format Key-Value Python Dictionary.
3. `execute_query(query, params)`: Berfungsi untuk mengeksekusi aksi `INSERT`, `UPDATE`, atau `DELETE`. Wajib menyertakan `self.conn.commit()` dan mengembalikan jumlah baris yang terpengaruh.
4. `fetch_all(query, params)`: Berfungsi khusus menarik data `SELECT`. Wajib dilapisi blok `try-except` yang mengembalikan `[]` (list kosong) jika query gagal, agar aplikasi utama tidak mendadak *close/crash*.