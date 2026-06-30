# pdf_extractor.py
# Anggota 4: PDF Data Extractor
# Tugas: Mengurus penyerapan berkas dokumen luar berbentuk PDF (RPS maupun BAP)
#        menggunakan library PyPDF2 / pdfplumber, lalu menyimpan hasil parsing ke database.

import re

# Coba gunakan pdfplumber terlebih dahulu (ekstraksi teks lebih rapi & per-baris),
# jika tidak tersedia maka fallback ke PyPDF2.
try:
    import pdfplumber
    _PDF_ENGINE = "pdfplumber"
except ImportError:
    pdfplumber = None
    _PDF_ENGINE = None

try:
    import PyPDF2
    if _PDF_ENGINE is None:
        _PDF_ENGINE = "PyPDF2"
except ImportError:
    PyPDF2 = None

# Modul database.py (dibuat oleh Anggota 2) menyediakan execute_query()
# untuk mengeksekusi statement INSERT/UPDATE ke MySQL.
try:
    from database import execute_query
except ImportError:
    # Fallback agar file ini tetap bisa diuji/dijalankan secara mandiri
    # sebelum database.py terintegrasi penuh.
    def execute_query(query, params=None):
        print("[WARN] database.execute_query tidak ditemukan. Query tidak dieksekusi.")
        print("Query  :", query)
        print("Params :", params)
        return False


# ---------------------------------------------------------------------------
# UTILITAS UMUM
# ---------------------------------------------------------------------------

def _read_pdf_text(file_path):
    """
    Membaca seluruh isi teks PDF dan mengembalikannya sebagai satu string utuh,
    dengan setiap baris dipisahkan oleh karakter newline.
    Mengutamakan pdfplumber, fallback ke PyPDF2 jika pdfplumber tidak tersedia.
    """
    full_text = ""

    if pdfplumber is not None:
        try:
            with pdfplumber.open(file_path) as pdf:
                pages_text = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)
                full_text = "\n".join(pages_text)
        except Exception as e:
            print(f"[ERROR] Gagal membaca PDF dengan pdfplumber: {e}")
            full_text = ""

    # Fallback ke PyPDF2 apabila pdfplumber tidak terpasang atau gagal membaca
    if not full_text and PyPDF2 is not None:
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                pages_text = []
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)
                full_text = "\n".join(pages_text)
        except Exception as e:
            print(f"[ERROR] Gagal membaca PDF dengan PyPDF2: {e}")
            full_text = ""

    if not full_text:
        raise RuntimeError(
            "Tidak dapat membaca isi PDF. Pastikan PyPDF2 atau pdfplumber "
            "telah terinstal dan file PDF tidak rusak / tidak terenkripsi."
        )

    return full_text


def _normalize_date(raw_date):
    """
    Mengubah berbagai format tanggal umum (DD/MM/YYYY, DD-MM-YYYY, DD Bulan YYYY)
    menjadi format standar YYYY-MM-DD agar konsisten dengan kolom DATE di MySQL.
    """
    raw_date = raw_date.strip()

    bulan_map = {
        "januari": "01", "februari": "02", "maret": "03", "april": "04",
        "mei": "05", "juni": "06", "juli": "07", "agustus": "08",
        "september": "09", "oktober": "10", "november": "11", "desember": "12",
    }

    # Format: 12 Januari 2025
    match = re.match(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", raw_date)
    if match:
        day, bulan_text, year = match.groups()
        bulan_num = bulan_map.get(bulan_text.lower())
        if bulan_num:
            return f"{year}-{bulan_num}-{day.zfill(2)}"

    # Format: 12/01/2025 atau 12-01-2025
    match = re.match(r"(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})", raw_date)
    if match:
        day, month, year = match.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    # Format sudah YYYY-MM-DD
    match = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", raw_date)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    # Jika tidak ada format yang cocok, kembalikan None agar bisa ditangani caller
    return None


# ---------------------------------------------------------------------------
# FUNGSI 1: extract_rps_to_db
# ---------------------------------------------------------------------------

def extract_rps_to_db(file_path):
    """
    Membaca dokumen cetak RPS, memilah teks 'Pokok Bahasan' dan 'Materi RPS'
    per sesi/pertemuan, lalu menyimpannya ke tabel `rps`.

    Pola yang dicari per blok sesi pada teks PDF (umumnya hasil cetak RPS kampus):
        Pertemuan / Sesi : <angka>
        Pokok Bahasan    : <teks>
        Materi           : <teks, bisa multi-baris>

    Return:
        int -> jumlah baris/sesi yang berhasil diekstrak & disimpan ke DB.
    """
    text = _read_pdf_text(file_path)

    # Memecah teks menjadi blok-blok per sesi/pertemuan menggunakan keyword
    # "Pertemuan" atau "Sesi" yang diikuti angka.
    session_pattern = re.compile(
        r"(?:Pertemuan|Sesi)\s*(?:ke[- ]?)?(\d+)\s*[:\-]?",
        re.IGNORECASE
    )

    matches = list(session_pattern.finditer(text))
    if not matches:
        print("[WARN] Tidak ditemukan penanda sesi/pertemuan pada dokumen RPS.")
        return 0

    inserted_count = 0

    for i, match in enumerate(matches):
        pertemuan = int(match.group(1))

        # Ambil potongan teks dari awal sesi ini sampai sebelum sesi berikutnya
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]

        # Ekstrak Pokok Bahasan
        pokok_match = re.search(
            r"Pokok\s*Bahasan\s*[:\-]\s*(.+)", block, re.IGNORECASE
        )
        pokok_bahasan = pokok_match.group(1).splitlines()[0].strip() if pokok_match else ""

        # Ekstrak Materi (ambil sisa baris setelah label "Materi" sampai akhir blok
        # atau sampai bertemu label lain seperti "Pokok Bahasan" sesi berikutnya)
        materi_match = re.search(
            r"Materi(?:\s*RPS)?\s*[:\-]\s*(.+)", block, re.IGNORECASE | re.DOTALL
        )
        materi_rps = materi_match.group(1).strip() if materi_match else ""
        # Bersihkan baris kosong berlebih
        materi_rps = re.sub(r"\n{2,}", "\n", materi_rps).strip()

        if not pokok_bahasan and not materi_rps:
            # Lewati blok yang tidak mengandung data relevan
            continue

        query = """
            INSERT INTO rps (pertemuan, pokok_bahasan, materi_rps)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                pokok_bahasan = VALUES(pokok_bahasan),
                materi_rps = VALUES(materi_rps)
        """
        params = (pertemuan, pokok_bahasan, materi_rps)

        success = execute_query(query, params)
        if success:
            inserted_count += 1

    print(f"[INFO] extract_rps_to_db: {inserted_count} sesi RPS berhasil diekstrak dari '{file_path}'.")
    return inserted_count


# ---------------------------------------------------------------------------
# FUNGSI 2: extract_bap_to_db
# ---------------------------------------------------------------------------

def extract_bap_to_db(file_path):
    """
    Membaca dokumen PDF Berita Acara Perkuliahan (BAP) cetakan sistem kampus,
    lalu mengekstrak teks tanggal, pokok bahasan, dan materi secara otomatis
    ke dalam tabel `bap`.

    Pola yang dicari per blok pertemuan pada teks PDF BAP:
        Pertemuan / Sesi Ke : <angka>
        Tanggal              : <tanggal>
        Pokok Bahasan        : <teks>
        Materi               : <teks, bisa multi-baris>

    Return:
        int -> jumlah baris/sesi BAP yang berhasil diekstrak & disimpan ke DB.
    """
    text = _read_pdf_text(file_path)

    session_pattern = re.compile(
        r"(?:Pertemuan|Sesi)\s*(?:ke[- ]?)?(\d+)\s*[:\-]?",
        re.IGNORECASE
    )

    matches = list(session_pattern.finditer(text))
    if not matches:
        print("[WARN] Tidak ditemukan penanda sesi/pertemuan pada dokumen BAP.")
        return 0

    inserted_count = 0

    for i, match in enumerate(matches):
        pertemuan = int(match.group(1))

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]

        # Ekstrak Tanggal
        tanggal_match = re.search(
            r"Tanggal\s*[:\-]\s*([0-9A-Za-z/\-\s]+)", block, re.IGNORECASE
        )
        tanggal_raw = tanggal_match.group(1).splitlines()[0].strip() if tanggal_match else ""
        tanggal = _normalize_date(tanggal_raw) if tanggal_raw else None

        # Ekstrak Pokok Bahasan
        pokok_match = re.search(
            r"Pokok\s*Bahasan\s*[:\-]\s*(.+)", block, re.IGNORECASE
        )
        pokok_bahasan_bap = pokok_match.group(1).splitlines()[0].strip() if pokok_match else ""

        # Ekstrak Materi
        materi_match = re.search(
            r"Materi\s*[:\-]\s*(.+)", block, re.IGNORECASE | re.DOTALL
        )
        materi = materi_match.group(1).strip() if materi_match else ""
        materi = re.sub(r"\n{2,}", "\n", materi).strip()

        if not pokok_bahasan_bap and not materi and not tanggal:
            continue

        query = """
            INSERT INTO bap (pertemuan, tanggal, pokok_bahasan_bap, materi)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                tanggal = VALUES(tanggal),
                pokok_bahasan_bap = VALUES(pokok_bahasan_bap),
                materi = VALUES(materi)
        """
        params = (pertemuan, tanggal, pokok_bahasan_bap, materi)

        success = execute_query(query, params)
        if success:
            inserted_count += 1

    print(f"[INFO] extract_bap_to_db: {inserted_count} sesi BAP berhasil diekstrak dari '{file_path}'.")
    return inserted_count


# ---------------------------------------------------------------------------
# PENGUJIAN MANDIRI (opsional, hanya jalan saat file dieksekusi langsung)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"PDF Extractor siap digunakan. Engine aktif: {_PDF_ENGINE or 'Tidak ada engine PDF terpasang'}")
    print("Gunakan extract_rps_to_db(file_path) atau extract_bap_to_db(file_path) untuk memproses dokumen.")