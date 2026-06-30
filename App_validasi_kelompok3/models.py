"""
models.py — Core NLP Matcher & Logic
Tugas Anggota 3 (Miftah Wira): Cross-Session Matching untuk validasi RPS vs BAP

Kontrak Interface dengan main.py:
  - validate() dipanggil TANPA argumen, ambil data sendiri dari DB
  - Return: tuple (list[dict], float)
    - list[dict] berisi key: no_sesi, tanggal, pokok_rps, materi_rps,
                             pokok_bap, materi_bap, status, keterangan,
                             pert, tgl, rps_pokok, rps_materi, bap_pokok, bap_materi
    - float = persentase kepatuhan (0.0 - 100.0)
"""

import re

try:
    from database import fetch_all
    _DB_TERSEDIA = True
except ImportError:
    _DB_TERSEDIA = False
    def fetch_all(q, p=None): return []


# ─────────────────────────────────────────────
# 1. TEXT CLEANER
# ─────────────────────────────────────────────

def clean_text(text: str) -> set:
    """
    Membersihkan string dan mengubahnya menjadi set kata unik.

    Steps:
      1. Lowercase semua karakter
      2. Ganti tanda baca (/ , - .) dengan spasi via Regex
      3. Hapus karakter non-alfanumerik lainnya
      4. Split → set kata unik (buang token kosong)

    Args:
        text: string mentah dari kolom materi RPS atau BAP

    Returns:
        set of unique words

    Example:
        >>> clean_text("Pengantar OOP, Kelas/Objek - Enkapsulasi.")
        {'pengantar', 'oop', 'kelas', 'objek', 'enkapsulasi'}
    """
    if not text or not isinstance(text, str):
        return set()

    text = text.lower()
    text = re.sub(r'[/,\-.]', ' ', text)       # target punctuation → spasi
    text = re.sub(r'[^\w\s]', ' ', text)        # sisa karakter aneh → spasi
    words = {w for w in text.split() if w}

    return words


# ─────────────────────────────────────────────
# 2. SIMILARITY (Jaccard Index)
# ─────────────────────────────────────────────

def _hitung_similarity(set_a: set, set_b: set) -> float:
    """
    Menghitung kemiripan dua set kata menggunakan Jaccard Index.
    Jaccard = |A ∩ B| / |A ∪ B|
    Rentang: 0.0 (tidak mirip) — 1.0 (identik)
    """
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0

    return len(set_a & set_b) / len(set_a | set_b)


# ─────────────────────────────────────────────
# 3. CORE VALIDATOR — Cross-Session Matching
# ─────────────────────────────────────────────

def validate(threshold: float = 0.3) -> tuple[list[dict], float]:
    """
    Memvalidasi kesesuaian materi RPS terhadap BAP.

    Dipanggil tanpa argumen dari main.py:
        hasil, persen = validate()

    Alur logika:
      1. Ambil semua data RPS dan BAP dari database
      2. Cek kecocokan sesi yang SAMA (RPS[1] vs BAP[1])
      3. Jika tidak cocok → scan SEMUA sesi BAP lain (cross-session)
      4. Jika ketemu di sesi lain → "Sesuai" + keterangan pergeseran
      5. Jika tidak ketemu di mana pun → "Tidak Sesuai"

    Args:
        threshold: minimum Jaccard similarity agar dianggap cocok (default 0.3)

    Returns:
        tuple:
          - list[dict]: hasil per sesi RPS
          - float: persentase kepatuhan (0.0 – 100.0)
    """
    # ── Ambil data dari DB ──
    rps_rows = fetch_all("SELECT pertemuan, pokok_bahasan, materi_rps FROM rps ORDER BY pertemuan")
    bap_rows = fetch_all("SELECT pertemuan, tanggal, pokok_bahasan_bap, materi FROM bap ORDER BY pertemuan")

    if not rps_rows:
        return [], 0.0

    # ── Bangun lookup BAP: pertemuan → data + cleaned set ──
    bap_lookup: dict[int, dict] = {}
    for b in bap_rows:
        bap_lookup[b["pertemuan"]] = {
            "tanggal"         : str(b.get("tanggal", "")),
            "pokok_bahasan_bap": b.get("pokok_bahasan_bap", ""),
            "materi"          : b.get("materi", ""),
            "words"           : clean_text(b.get("materi", "")),
        }

    hasil = []

    for rps in rps_rows:
        no_sesi   = rps["pertemuan"]
        pokok_rps = rps.get("pokok_bahasan", "")
        materi_rps = rps.get("materi_rps", "")
        set_rps   = clean_text(materi_rps)

        # Nilai default (jika tidak ditemukan match)
        entry = {
            # Key untuk main.py / Treeview
            "no_sesi"   : no_sesi,
            "tanggal"   : "—",
            "pokok_rps" : pokok_rps,
            "materi_rps": materi_rps,
            "pokok_bap" : "—",
            "materi_bap": "—",
            "status"    : "Tidak Sesuai",
            "keterangan": "Materi tidak ditemukan di BAP manapun.",
            # Key untuk report_generator.py
            "pert"      : no_sesi,
            "tgl"       : "—",
            "rps_pokok" : pokok_rps,
            "rps_materi": materi_rps,
            "bap_pokok" : "—",
            "bap_materi": "—",
        }

        # ── STEP 1: Cek sesi yang sama ──
        matched = False
        if no_sesi in bap_lookup:
            bap_same = bap_lookup[no_sesi]
            score    = _hitung_similarity(set_rps, bap_same["words"])

            if score >= threshold:
                _isi_entry_sesuai(
                    entry, bap_same, no_sesi,
                    score, same_session=True
                )
                matched = True

        # ── STEP 2: Cross-Session Scanning ──
        if not matched:
            best_score = 0.0
            best_sesi  = None
            best_bap   = None

            for sesi_bap, bap_data in bap_lookup.items():
                if sesi_bap == no_sesi:
                    continue  # sudah dicek di Step 1

                score = _hitung_similarity(set_rps, bap_data["words"])
                if score > best_score:
                    best_score = score
                    best_sesi  = sesi_bap
                    best_bap   = bap_data

            if best_score >= threshold and best_sesi is not None:
                _isi_entry_sesuai(
                    entry, best_bap, best_sesi,
                    best_score, same_session=False
                )
                matched = True

        # ── STEP 3: Tidak cocok di mana pun ──
        if not matched and no_sesi in bap_lookup:
            # Isi kolom BAP tetap dengan data sesi yang sama (untuk laporan)
            bap_same = bap_lookup[no_sesi]
            entry["tanggal"]    = bap_same["tanggal"]
            entry["pokok_bap"]  = bap_same["pokok_bahasan_bap"]
            entry["materi_bap"] = bap_same["materi"]
            entry["tgl"]        = bap_same["tanggal"]
            entry["bap_pokok"]  = bap_same["pokok_bahasan_bap"]
            entry["bap_materi"] = bap_same["materi"]

        hasil.append(entry)

    # ── Hitung persentase ──
    persen = calculate_compliance(hasil)

    return hasil, persen


def _isi_entry_sesuai(entry: dict, bap: dict, sesi_match: int,
                      score: float, same_session: bool):
    """Helper: mengisi entry dict saat materi dinyatakan Sesuai."""
    tanggal    = bap["tanggal"]
    pokok_bap  = bap["pokok_bahasan_bap"]
    materi_bap = bap["materi"]

    if same_session:
        keterangan = f"Valid! Materi sesuai pada Sesi {sesi_match}."
    else:
        keterangan = f"Valid! Materi diajarkan bergeser pada Sesi {sesi_match}."

    entry.update({
        "tanggal"   : tanggal,
        "pokok_bap" : pokok_bap,
        "materi_bap": materi_bap,
        "status"    : "Sesuai",
        "keterangan": keterangan,
        # alias untuk report_generator
        "tgl"       : tanggal,
        "bap_pokok" : pokok_bap,
        "bap_materi": materi_bap,
    })


# ─────────────────────────────────────────────
# 4. COMPLIANCE CALCULATOR
# ─────────────────────────────────────────────

def calculate_compliance(hasil: list[dict]) -> float:
    """
    Menghitung persentase kepatuhan berdasarkan hasil validate().

    Args:
        hasil: list[dict] output dari validate()

    Returns:
        float persentase (0.0 – 100.0)
    """
    total = len(hasil)
    if total == 0:
        return 0.0

    sesuai = sum(1 for r in hasil if r.get("status") == "Sesuai")
    return round((sesuai / total) * 100, 2)


# ─────────────────────────────────────────────
# QUICK TEST (tanpa MySQL — mode offline)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Simulasi data jika DB tidak tersedia
    _DUMMY_RPS = [
        {"pertemuan": 1, "pokok_bahasan": "Pengantar OOP",   "materi_rps": "Pengantar OOP, Kelas dan Objek"},
        {"pertemuan": 2, "pokok_bahasan": "Enkapsulasi",     "materi_rps": "Enkapsulasi dan Abstraksi"},
        {"pertemuan": 3, "pokok_bahasan": "Inheritance",     "materi_rps": "Inheritance / Pewarisan Kelas"},
        {"pertemuan": 4, "pokok_bahasan": "Polymorphism",    "materi_rps": "Polymorphism dan Method Overriding"},
        {"pertemuan": 5, "pokok_bahasan": "Exception",       "materi_rps": "Exception Handling dan Try Catch"},
    ]
    _DUMMY_BAP = [
        {"pertemuan": 1, "tanggal": "2025-02-10", "pokok_bahasan_bap": "Pengantar OOP",  "materi": "Pengantar OOP Kelas Objek"},
        {"pertemuan": 2, "tanggal": "2025-02-17", "pokok_bahasan_bap": "Review",         "materi": "Review dan kuis singkat"},
        {"pertemuan": 3, "tanggal": "2025-02-24", "pokok_bahasan_bap": "Enkapsulasi",    "materi": "Enkapsulasi Abstraksi Data"},
        {"pertemuan": 4, "tanggal": "2025-03-03", "pokok_bahasan_bap": "Inheritance",    "materi": "Inheritance Pewarisan Kelas"},
        {"pertemuan": 5, "tanggal": "2025-03-10", "pokok_bahasan_bap": "Polymorphism",   "materi": "Polymorphism Method Overriding"},
        # Sesi 5 RPS (Exception Handling) tidak ada padanannya
    ]

    # Override fetch_all untuk mode offline
    import unittest.mock as mock

    def _mock_fetch(query, params=None):
        if "FROM rps" in query:
            return _DUMMY_RPS
        if "FROM bap" in query:
            return _DUMMY_BAP
        return []

    import models as _self
    with mock.patch.object(_self, 'fetch_all', side_effect=_mock_fetch):
        hasil, persen = _self.validate()

    print("=" * 65)
    print("HASIL VALIDASI RPS vs BAP (MODE OFFLINE / DUMMY DATA)")
    print("=" * 65)
    for r in hasil:
        print(f"\nSesi {r['no_sesi']:>2} | {r['pokok_rps']}")
        print(f"  Materi RPS   : {r['materi_rps']}")
        print(f"  Status       : {r['status']}")
        print(f"  Keterangan   : {r['keterangan']}")
        print(f"  Tanggal BAP  : {r['tanggal']}")

    print("\n" + "=" * 65)
    total  = len(hasil)
    sesuai = sum(1 for r in hasil if r["status"] == "Sesuai")
    print(f"  Total Sesi        : {total}")
    print(f"  Sesi Sesuai       : {sesuai}")
    print(f"  Sesi Tidak Sesuai : {total - sesuai}")
    print(f"  Kepatuhan         : {persen}%")
    print("=" * 65)
