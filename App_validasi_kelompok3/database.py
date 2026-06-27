import mysql.connector
from mysql.connector import Error

def get_connection():
    """
    Membuat dan mengembalikan koneksi ke basis data MySQL lokal (XAMPP).
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',         # Username default XAMPP
            password='',         # Password default XAMPP (kosong)
            database='pbo_rps_bap'
        )
        return connection
    except Error as e:
        print(f"[DB ERROR] Gagal menghubungkan ke MySQL: {e}")
        return None

def init_database():
    """
    Mengotomatisasi pembuatan database dan tabel rps & bap jika belum ada pada server.
    """
    # Langkah Awal: Koneksi tanpa memilih DB untuk memastikan DB pbo_rps_bap telah terbuat
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS pbo_rps_bap")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"[DB ERROR] Gagal menginisialisasi Database induk: {e}")
        return

    # Langkah Kedua: Membuat struktur tabel di dalam database pbo_rps_bap
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        
        # Inisialisasi Tabel rps
        query_rps = """
        CREATE TABLE IF NOT EXISTS rps (
            pertemuan INT PRIMARY KEY,
            pokok_bahasan VARCHAR(255) NOT NULL,
            materi_rps TEXT NOT NULL
        )
        """
        cursor.execute(query_rps)
        
        # Inisialisasi Tabel bap (Mendukung pencatatan tipe data DATE)
        query_bap = """
        CREATE TABLE IF NOT EXISTS bap (
            pertemuan INT PRIMARY KEY,
            tanggal DATE NOT NULL,
            pokok_bahasan_bap VARCHAR(255) NOT NULL,
            materi TEXT NOT NULL
        )
        """
        cursor.execute(query_bap)
        
        conn.commit()
        print("[DB INFO] Database dan struktur tabel rps/bap berhasil diamankan.")
        
    except Error as e:
        print(f"[DB ERROR] Gagal membuat struktur tabel: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def execute_query(query, params=None):
    """
    Menjalankan query modifikasi/aksi (INSERT, UPDATE, DELETE, TRUNCATE).
    Mendukung pengamanan penyimpanan string tanggal format 'YYYY-MM-DD'.
    """
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return True
    except Error as e:
        print(f"[DB ERROR] Eksekusi query gagal: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def fetch_all(query, params=None):
    """
    Mengambil seluruh baris data dari query SELECT.
    Mengembalikan data dalam bentuk list of dictionary agar mempermudah pemetaan ke GUI Treeview.
    """
    conn = get_connection()
    if conn is None:
        return []
    
    try:
        # dictionary=True mengubah hasil tuple menjadi key-value pasang sesuai nama kolom
        cursor = conn.cursor(dictionary=True) 
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"[DB ERROR] Gagal mengambil data (Fetch All): {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def reset_all_data():
    """
    Fungsi khusus Tombol 'Reset Semua Data' menggunakan aksi TRUNCATE TABLE.
    Menghapus seluruh cache data dengan bersih tanpa merusak struktur tabel.
    """
    # Bersihkan tabel BAP terlebih dahulu untuk keamanan dependensi data, lalu tabel RPS
    truncate_bap = "TRUNCATE TABLE bap"
    truncate_rps = "TRUNCATE TABLE rps"
    
    success_bap = execute_query(truncate_bap)
    success_rps = execute_query(truncate_rps)
    
    if success_bap and success_rps:
        print("[DB INFO] Fitur Reset Sukses: Tabel rps dan bap telah dikosongkan.")
        return True
    else:
        print("[DB WARN] Reset gagal atau hanya berhasil sebagian.")
        return False

# Trigger inisialisasi otomatis jika file database.py ini dijalankan mandiri
if __name__ == "__main__":
    init_database()