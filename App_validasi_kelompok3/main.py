import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime

try:
    from tkcalendar import DateEntry
    _TKCAL_TERSEDIA = True
except ImportError:
    _TKCAL_TERSEDIA = False
    class DateEntry(tk.Entry):
        def __init__(self, *a, **kw):
            for k in ("date_pattern", "background", "foreground", "borderwidth"):
                kw.pop(k, None)
            super().__init__(*a, **kw)
            self.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        def get_date(self):
            try:
                return datetime.datetime.strptime(self.get(), "%Y-%m-%d").date()
            except ValueError:
                return datetime.date.today()
        def set_date(self, d):
            self.delete(0, "end")
            self.insert(0, d.strftime("%Y-%m-%d"))

try:
    from database import init_database, execute_query, fetch_all, reset_all_data
    _DB_TERSEDIA = True
except ImportError:
    _DB_TERSEDIA = False
    def init_database(): pass
    def execute_query(q, p=None): return False
    def fetch_all(q, p=None): return []
    def reset_all_data(): return False

try:
    from models import validate
    _MODELS_TERSEDIA = True
except ImportError:
    _MODELS_TERSEDIA = False
    def validate(): return ([], 0.0)

try:
    from pdf_extractor import extract_rps_to_db, extract_bap_to_db
    _PDF_TERSEDIA = True
except ImportError:
    _PDF_TERSEDIA = False
    def extract_rps_to_db(file_path): return False
    def extract_bap_to_db(file_path): return False

try:
    from report_generator import export_report
    _REPORT_TERSEDIA = True
except ImportError:
    _REPORT_TERSEDIA = False
    def export_report(file_path, results, persen): return False


WARNA = {
    "bg_utama"         : "#F3F4F6",
    "header_bg"        : "#1E3A8A",
    "header_fg"        : "#FFFFFF",
    "header_sub"       : "#93C5FD",
    "btn_hijau"        : "#16A34A",
    "btn_merah"        : "#DC2626",
    "btn_biru"         : "#2563EB",
    "btn_ungu"         : "#7C3AED",
    "btn_abu"          : "#475569",
    "btn_rst"          : "#374151",
    "btn_fg"           : "#FFFFFF",
    "btn_rst_fg"       : "#D1D5DB",
    "panel_bg"         : "#FFFFFF",
    "tabel_heading_bg" : "#1E3A8A",
    "tabel_heading_fg" : "#FFFFFF",
    "tabel_bg"         : "#FFFFFF",
    "baris_sesuai"     : "#DCFCE7",
    "baris_tidak"      : "#FEF9C3",
    "baris_hilang"     : "#FFE4E6",
    "log_bg"           : "#FFFBEB",
    "log_fg"           : "#1E3A8A",
    "log_sukses"       : "#15803D",
    "log_warn"         : "#B45309",
    "log_error"        : "#B91C1C",
    "db_online"        : "#16A34A",
    "db_offline"       : "#DC2626",
    "db_na"            : "#6B7280",
}

FONT = {
    "judul"  : ("Segoe UI", 15, "bold"),
    "sub"    : ("Segoe UI", 9),
    "label"  : ("Segoe UI", 9),
    "labelb" : ("Segoe UI", 9, "bold"),
    "tombol" : ("Segoe UI", 9, "bold"),
    "tabel"  : ("Segoe UI", 9),
    "log"    : ("Segoe UI", 9),
    "logb"   : ("Segoe UI", 9, "bold"),
}

KOLOM_TABEL = (
    "no_sesi", "tanggal",
    "pokok_rps", "materi_rps",
    "pokok_bap", "materi_bap",
    "status", "keterangan",
)
LABEL_KOLOM = {
    "no_sesi"   : "NO SESI",
    "tanggal"   : "TANGGAL",
    "pokok_rps" : "POKOK BAHASAN (RPS)",
    "materi_rps": "MATERI (RPS)",
    "pokok_bap" : "POKOK BAHASAN (BAP)",
    "materi_bap": "MATERI (BAP)",
    "status"    : "STATUS",
    "keterangan": "KETERANGAN",
}
LEBAR_KOLOM = {
    "no_sesi"   : 60,
    "tanggal"   : 90,
    "pokok_rps" : 160,
    "materi_rps": 160,
    "pokok_bap" : 160,
    "materi_bap": 160,
    "status"    : 100,
    "keterangan": 200,
}


def _darken(hex_color: str, factor: float = 0.82) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return "#{:02X}{:02X}{:02X}".format(int(r*factor), int(g*factor), int(b*factor))


class AplikasiValidasiRPS:

    def __init__(self, root: tk.Tk):
        self.root = root
        self._setup_window()

        self.hasil_validasi  = []
        self.persen_validasi = 0.0
        self._db_connected   = False

        self._build_header()
        self._build_body()
        self._build_statusbar()

        self._inisialisasi_db()
        self.log("Aplikasi siap.", level="info")
        if not _TKCAL_TERSEDIA:
            self.log("tkcalendar tidak ditemukan — jalankan: pip install tkcalendar", level="warn")

    def _setup_window(self):
        self.root.title("Validasi Kesesuaian RPS vs BAP — PBO Python")
        self.root.geometry("1250x700")
        self.root.minsize(1000, 600)
        self.root.configure(bg=WARNA["bg_utama"])
        self.root.resizable(True, True)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)

    def _build_header(self):
        frm = tk.Frame(self.root, bg=WARNA["header_bg"], pady=10)
        frm.grid(row=0, column=0, sticky="ew")
        frm.columnconfigure(0, weight=1)

        tk.Label(frm, text="🎓  Sistem Validasi Kesesuaian RPS vs BAP",
                 font=FONT["judul"], bg=WARNA["header_bg"], fg=WARNA["header_fg"],
                 anchor="w", padx=16).grid(row=0, column=0, sticky="w")

        tk.Label(frm, text="Praktikum Pemrograman Berorientasi Objek — Pengolahan Teks",
                 font=FONT["sub"], bg=WARNA["header_bg"], fg=WARNA["header_sub"],
                 anchor="w", padx=16).grid(row=1, column=0, sticky="w")

        db_frm = tk.Frame(frm, bg=WARNA["header_bg"])
        db_frm.grid(row=0, column=1, rowspan=2, sticky="e", padx=16)
        tk.Label(db_frm, text="Database MySQL", font=FONT["sub"],
                 bg=WARNA["header_bg"], fg=WARNA["header_sub"]).pack(anchor="e")
        self.lbl_db = tk.Label(db_frm, text="● Menghubungkan...",
                               font=("Segoe UI", 8, "bold"),
                               bg=WARNA["header_bg"], fg=WARNA["db_na"])
        self.lbl_db.pack(anchor="e")

    def _build_body(self):
        body = tk.Frame(self.root, bg=WARNA["bg_utama"])
        body.grid(row=1, column=0, sticky="nsew", padx=10, pady=8)
        body.columnconfigure(0, weight=0)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)
        self._build_left_panel(body)
        self._build_right_panel(body)

    def _build_left_panel(self, parent):
        frm = tk.LabelFrame(
            parent, text="  📝  Input Manual BAP  ",
            font=FONT["labelb"], bg=WARNA["panel_bg"], fg="#1E3A8A",
            relief="solid", bd=1, padx=12, pady=10,
        )
        frm.grid(row=0, column=0, sticky="ns", padx=(0, 8))
        frm.columnconfigure(0, weight=1)
        frm.columnconfigure(1, weight=1)

        tk.Label(frm, text="No. Sesi / Pertemuan", font=FONT["label"],
                 bg=WARNA["panel_bg"], anchor="w"
                 ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 2))
        self.entry_sesi = tk.Entry(frm, font=FONT["label"], width=28, relief="solid", bd=1)
        self.entry_sesi.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        tk.Label(frm, text="Tanggal Sesi Perkuliahan", font=FONT["label"],
                 bg=WARNA["panel_bg"], anchor="w"
                 ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 2))
        self.entry_tanggal = DateEntry(
            frm, font=FONT["label"], width=26,
            date_pattern="yyyy-mm-dd",
            background="#1E3A8A", foreground="white", borderwidth=1,
        )
        self.entry_tanggal.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        tk.Label(frm, text="Pokok Bahasan BAP", font=FONT["label"],
                 bg=WARNA["panel_bg"], anchor="w"
                 ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 2))
        self.entry_pokok = tk.Entry(frm, font=FONT["label"], width=28, relief="solid", bd=1)
        self.entry_pokok.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        tk.Label(frm, text="Materi BAP", font=FONT["label"],
                 bg=WARNA["panel_bg"], anchor="w"
                 ).grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 2))
        self.text_materi = tk.Text(frm, font=FONT["label"], width=28, height=6,
                                   relief="solid", bd=1, wrap="word")
        self.text_materi.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        ttk.Separator(frm, orient="horizontal").grid(
            row=8, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self._btn_panel(frm, "➕  Tambahkan BAP", WARNA["btn_hijau"],
                        self._aksi_tambah_bap, row=9, col=0, px=(0, 3))
        self._btn_panel(frm, "🧹  Bersihkan Form", WARNA["btn_abu"],
                        self._aksi_bersihkan_form, row=9, col=1, px=(3, 0))

        ttk.Separator(frm, orient="horizontal").grid(
            row=10, column=0, columnspan=2, sticky="ew", pady=(10, 8))

        self._btn_panel(frm, "📄  Upload RPS (PDF)",   WARNA["btn_biru"],  self._aksi_load_rps,    row=11, col=0, px=(0, 5), py=(0, 10))
        self._btn_panel(frm, "📋  Upload BAP (PDF)", "#0891B2",          self._aksi_upload_bap,  row=11, col=1, px=(5, 0), py=(0, 10))

        self._btn_full(frm, "🔍  Proses Validasi",   WARNA["btn_ungu"],  self._aksi_validasi,       row=12)
        self._btn_full(frm, "📥  Cetak Laporan PDF", WARNA["btn_merah"], self._aksi_cetak_laporan,  row=13)
        self._btn_full(frm, "💥  Reset Semua Data",  WARNA["btn_rst"],   self._aksi_reset_data,     row=14,
                       fg=WARNA["btn_rst_fg"], pady=(0, 0))

    def _btn_full(self, parent, teks, warna, callback, row, fg=None, pady=(0, 4)):
        """Tombol full-width (columnspan=2)."""
        b = tk.Button(
            parent, text=teks, font=FONT["tombol"],
            bg=warna, fg=fg or WARNA["btn_fg"],
            activebackground=_darken(warna), activeforeground=fg or WARNA["btn_fg"],
            relief="flat", cursor="hand2", bd=0, padx=10, pady=7, command=callback,
        )
        b.grid(row=row, column=0, columnspan=2, sticky="ew", pady=pady)
        b.bind("<Enter>", lambda e: b.configure(bg=_darken(warna)))
        b.bind("<Leave>", lambda e: b.configure(bg=warna))
        return b

    def _btn_panel(self, parent, teks, warna, callback, row, col, px=(0, 0), py=(0, 4)):
        """Tombol setengah lebar (1 kolom)."""
        b = tk.Button(
            parent, text=teks, font=FONT["tombol"],
            bg=warna, fg=WARNA["btn_fg"],
            activebackground=_darken(warna), activeforeground=WARNA["btn_fg"],
            relief="flat", cursor="hand2", bd=0, padx=6, pady=7, command=callback,
        )
        b.grid(row=row, column=col, sticky="ew", padx=px, pady=py)
        b.bind("<Enter>", lambda e: b.configure(bg=_darken(warna)))
        b.bind("<Leave>", lambda e: b.configure(bg=warna))
        return b

    def _build_right_panel(self, parent):
        frm = tk.Frame(parent, bg=WARNA["bg_utama"])
        frm.grid(row=0, column=1, sticky="nsew")
        frm.columnconfigure(0, weight=1)
        frm.rowconfigure(0, weight=3)
        frm.rowconfigure(1, weight=1)
        self._build_tabel(frm)
        self._build_log(frm)

    def _build_tabel(self, parent):
        wrap = tk.Frame(parent, bg=WARNA["bg_utama"])
        wrap.grid(row=0, column=0, sticky="nsew", pady=(0, 6))
        wrap.columnconfigure(0, weight=1)
        wrap.rowconfigure(1, weight=1)

        tk.Label(wrap, text="📊  Matriks Hasil Validasi", font=FONT["labelb"],
                 bg=WARNA["bg_utama"], fg="#374151", anchor="w"
                 ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("App.Treeview.Heading",
                        background=WARNA["tabel_heading_bg"],
                        foreground=WARNA["tabel_heading_fg"],
                        font=FONT["labelb"], relief="flat")
        style.configure("App.Treeview", font=FONT["tabel"], rowheight=24,
                        background=WARNA["tabel_bg"], fieldbackground=WARNA["tabel_bg"])
        style.map("App.Treeview",
                  background=[("selected", "#BFDBFE")],
                  foreground=[("selected", "#1E3A8A")])

        self.tabel = ttk.Treeview(wrap, columns=KOLOM_TABEL,
                                   show="headings", style="App.Treeview",
                                   selectmode="browse")
        for col in KOLOM_TABEL:
            self.tabel.heading(col, text=LABEL_KOLOM[col], anchor="center")
            self.tabel.column(col, width=LEBAR_KOLOM[col], minwidth=50, anchor="w")
        self.tabel.column("no_sesi",  anchor="center")
        self.tabel.column("tanggal",  anchor="center")
        self.tabel.column("status",   anchor="center")

        self.tabel.tag_configure("sesuai", background=WARNA["baris_sesuai"])
        self.tabel.tag_configure("tidak",  background=WARNA["baris_tidak"])
        self.tabel.tag_configure("hilang", background=WARNA["baris_hilang"])

        vsb = ttk.Scrollbar(wrap, orient="vertical",   command=self.tabel.yview)
        hsb = ttk.Scrollbar(wrap, orient="horizontal", command=self.tabel.xview)
        self.tabel.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tabel.grid(row=1, column=0, sticky="nsew")
        vsb.grid(row=1, column=1, sticky="ns")
        hsb.grid(row=2, column=0, sticky="ew")

    def _build_log(self, parent):
        wrap = tk.Frame(parent, bg=WARNA["bg_utama"])
        wrap.grid(row=1, column=0, sticky="nsew")
        wrap.columnconfigure(0, weight=1)
        wrap.rowconfigure(1, weight=1)

        hdr = tk.Frame(wrap, bg="#FEF3C7", pady=4)
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew")
        tk.Label(hdr, text="📋  Live Log Sistem", font=FONT["logb"],
                 bg="#FEF3C7", fg="#92400E", padx=10).pack(side="left")
        tk.Button(hdr, text="Bersihkan", font=("Segoe UI", 8),
                  bg="#FDE68A", fg="#78350F", relief="flat", cursor="hand2",
                  padx=6, command=self._clear_log).pack(side="right", padx=8)

        self.log_widget = tk.Text(
            wrap, font=FONT["log"],
            bg=WARNA["log_bg"], fg=WARNA["log_fg"],
            relief="flat", wrap="word", state="disabled",
            cursor="arrow", padx=10, pady=6, height=7,
        )
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.log_widget.yview)
        self.log_widget.configure(yscrollcommand=vsb.set)
        self.log_widget.grid(row=1, column=0, sticky="nsew")
        vsb.grid(row=1, column=1, sticky="ns")

        self.log_widget.tag_configure("info",   foreground=WARNA["log_fg"])
        self.log_widget.tag_configure("sukses", foreground=WARNA["log_sukses"])
        self.log_widget.tag_configure("warn",   foreground=WARNA["log_warn"])
        self.log_widget.tag_configure("error",  foreground=WARNA["log_error"])

    def _build_statusbar(self):
        frm = tk.Frame(self.root, bg="#E5E7EB", height=22)
        frm.grid(row=2, column=0, sticky="ew")
        self.lbl_status = tk.Label(frm, text="Siap.", font=("Segoe UI", 8),
                                   bg="#E5E7EB", fg="#6B7280", anchor="w", padx=10)
        self.lbl_status.pack(side="left")
        self.lbl_persen = tk.Label(frm, text="", font=("Segoe UI", 8, "bold"),
                                   bg="#E5E7EB", fg="#1E3A8A", anchor="e", padx=10)
        self.lbl_persen.pack(side="right")

    def _set_status(self, teks):
        self.lbl_status.configure(text=teks)

    def log(self, pesan: str, level: str = "info"):
        waktu  = datetime.datetime.now().strftime("%H:%M:%S")
        prefix = {"info": "[INFO]", "sukses": "[OK  ]",
                  "warn": "[WARN]", "error":  "[ERR ]"}.get(level, "[LOG ]")
        self.log_widget.configure(state="normal")
        self.log_widget.insert("end", f"{waktu}  {prefix}  {pesan}\n", level)
        self.log_widget.see("end")
        self.log_widget.configure(state="disabled")

    def _clear_log(self):
        self.log_widget.configure(state="normal")
        self.log_widget.delete("1.0", "end")
        self.log_widget.configure(state="disabled")

    def _inisialisasi_db(self):
        if not _DB_TERSEDIA:
            self.lbl_db.configure(text="● Modul tidak ditemukan", fg=WARNA["db_na"])
            self.log("database.py tidak ditemukan — berjalan tanpa DB.", level="warn")
            return
        try:
            init_database()
            test = fetch_all("SELECT 1")
            if test is not None:
                self._db_connected = True
                self.lbl_db.configure(text="● Terhubung (localhost)", fg=WARNA["db_online"])
                self.log("Koneksi MySQL berhasil — pbo_rps_bap siap.", level="sukses")
            else:
                raise ConnectionError("fetch_all gagal")
        except Exception as e:
            self.lbl_db.configure(text="● Gagal terhubung", fg=WARNA["db_offline"])
            self.log(f"Koneksi MySQL gagal: {e}", level="error")
            self.log("Pastikan XAMPP (MySQL) sudah berjalan.", level="warn")

    def _aksi_tambah_bap(self):
        sesi   = self.entry_sesi.get().strip()
        pokok  = self.entry_pokok.get().strip()
        materi = self.text_materi.get("1.0", "end").strip()

        if not sesi or not pokok or not materi:
            messagebox.showwarning("Input Tidak Lengkap",
                                   "No. Sesi, Pokok Bahasan, dan Materi wajib diisi.")
            return
        if not sesi.isdigit():
            messagebox.showwarning("Input Tidak Valid", "No. Sesi harus berupa angka.")
            return

        try:
            tanggal = self.entry_tanggal.get_date().strftime("%Y-%m-%d")
        except Exception:
            tanggal = datetime.date.today().strftime("%Y-%m-%d")

        if not _DB_TERSEDIA or not self._db_connected:
            self.log("Tidak dapat menyimpan: koneksi DB tidak tersedia.", level="error")
            return

        query = """
            INSERT INTO bap (pertemuan, tanggal, pokok_bahasan_bap, materi)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                tanggal = VALUES(tanggal),
                pokok_bahasan_bap = VALUES(pokok_bahasan_bap),
                materi = VALUES(materi)
        """
        if execute_query(query, (int(sesi), tanggal, pokok, materi)):
            self.log(f"BAP Sesi {sesi} ({tanggal}) berhasil disimpan.", level="sukses")
            self._set_status(f"BAP Sesi {sesi} tersimpan.")
        else:
            self.log(f"Gagal menyimpan BAP Sesi {sesi}.", level="error")

    def _aksi_bersihkan_form(self):
        self.entry_sesi.delete(0, "end")
        self.entry_pokok.delete(0, "end")
        self.text_materi.delete("1.0", "end")
        try:
            self.entry_tanggal.set_date(datetime.date.today())
        except Exception:
            pass
        self.log("Form dibersihkan.", level="info")

    def _aksi_upload_bap(self):
        """
        Membuka dialog file PDF BAP, lalu memanggil extract_bap_to_db(file_path) dari Taufik.
        Alternatif dari input manual form — user bisa pilih salah satu atau keduanya.
        """
        if not _PDF_TERSEDIA:
            messagebox.showwarning("Modul Tidak Tersedia",
                                   "pdf_extractor.py belum tersedia.\nHubungi Taufik.")
            return
        file_path = filedialog.askopenfilename(
            title="Pilih File BAP (PDF)",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if not file_path:
            self.log("Upload BAP dibatalkan.", level="warn")
            return
        self.log(f"Mengekstrak BAP: {file_path.split('/')[-1]}...", level="info")
        self._set_status("Mengekstrak BAP...")
        try:
            if extract_bap_to_db(file_path):
                self.log("BAP berhasil diekstrak dan disimpan ke database.", level="sukses")
                self._set_status("BAP berhasil diunggah.")
            else:
                self.log("Ekstraksi BAP gagal atau tidak ada data ditemukan.", level="error")
                self._set_status("Gagal mengunggah BAP.")
        except Exception as e:
            self.log(f"Error saat ekstrak BAP: {e}", level="error")

    def _aksi_load_rps(self):
        if not _PDF_TERSEDIA:
            messagebox.showwarning("Modul Tidak Tersedia",
                                   "pdf_extractor.py belum tersedia.\nHubungi Taufik.")
            return
        file_path = filedialog.askopenfilename(
            title="Pilih File RPS (PDF)",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if not file_path:
            self.log("Load RPS dibatalkan.", level="warn")
            return
        self.log(f"Mengekstrak RPS: {file_path.split('/')[-1]}...", level="info")
        self._set_status("Mengekstrak RPS...")
        try:
            if extract_rps_to_db(file_path):
                self.log("RPS berhasil diekstrak dan disimpan ke database.", level="sukses")
                self._set_status("RPS berhasil dimuat.")
            else:
                self.log("Ekstraksi RPS gagal.", level="error")
                self._set_status("Gagal memuat RPS.")
        except Exception as e:
            self.log(f"Error saat ekstrak RPS: {e}", level="error")

    def _aksi_validasi(self):
        if not _MODELS_TERSEDIA:
            messagebox.showwarning("Modul Tidak Tersedia",
                                   "models.py belum tersedia.\nHubungi Miftah Wira.")
            return
        self.log("Memulai proses validasi NLP...", level="info")
        self._set_status("Memvalidasi...")
        try:
            hasil, persen = validate()
            if not hasil:
                self.log("Validasi selesai — tidak ada data. Pastikan RPS & BAP sudah diinput.", level="warn")
                self._set_status("Validasi selesai — data kosong.")
                return
            self.hasil_validasi  = hasil
            self.persen_validasi = persen
            self._tampilkan_tabel(hasil)
            sesuai = sum(1 for r in hasil if r.get("status") == "Sesuai")
            self.log(f"Validasi selesai — {sesuai}/{len(hasil)} sesi sesuai | Kepatuhan: {persen:.1f}%", level="sukses")
            self.lbl_persen.configure(text=f"Kepatuhan: {persen:.1f}%")
            self._set_status(f"Validasi selesai — Kepatuhan: {persen:.1f}%")
        except Exception as e:
            self.log(f"Error saat validasi: {e}", level="error")

    def _aksi_cetak_laporan(self):
        if not _REPORT_TERSEDIA:
            messagebox.showwarning("Modul Tidak Tersedia",
                                   "report_generator.py belum tersedia.\nHubungi Miftahudin.")
            return
        if not self.hasil_validasi:
            messagebox.showwarning("Data Kosong", "Jalankan validasi terlebih dahulu.")
            return
        file_path = filedialog.asksaveasfilename(
            title="Simpan Laporan PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="Laporan_Validasi_RPS_BAP.pdf",
        )
        if not file_path:
            self.log("Cetak laporan dibatalkan.", level="warn")
            return
        self.log("Mengekspor laporan PDF...", level="info")
        try:
            if export_report(file_path, self.hasil_validasi, self.persen_validasi):
                self.log(f"Laporan disimpan: {file_path.split('/')[-1]}", level="sukses")
                self._set_status("Laporan berhasil dicetak.")
                messagebox.showinfo("Berhasil", f"Laporan disimpan di:\n{file_path}")
            else:
                self.log("Export laporan gagal.", level="error")
        except Exception as e:
            self.log(f"Error saat cetak laporan: {e}", level="error")

    def _aksi_reset_data(self):
        if not self._db_connected:
            messagebox.showerror("Koneksi Gagal",
                                 "Reset tidak dapat dilakukan: database tidak terhubung.")
            return
        if not messagebox.askyesno("Konfirmasi Reset",
                                   "💥  Tindakan ini akan menghapus SEMUA data RPS dan BAP.\n\n"
                                   "Data tidak dapat dikembalikan. Lanjutkan?",
                                   icon="warning"):
            self.log("Reset dibatalkan.", level="warn")
            return
        self.log("Mengeksekusi TRUNCATE tabel rps & bap...", level="warn")
        try:
            if reset_all_data():
                self.hasil_validasi  = []
                self.persen_validasi = 0.0
                for item in self.tabel.get_children():
                    self.tabel.delete(item)
                self.lbl_persen.configure(text="")
                self.log("Reset berhasil — semua data dihapus.", level="sukses")
                self._set_status("Reset selesai.")
                messagebox.showinfo("Reset Selesai", "Semua data berhasil dihapus.")
            else:
                self.log("Reset gagal.", level="error")
        except Exception as e:
            self.log(f"Error saat reset: {e}", level="error")

    def _tampilkan_tabel(self, hasil: list):
        for item in self.tabel.get_children():
            self.tabel.delete(item)
        TAG = {"Sesuai": "sesuai", "Tidak Sesuai": "tidak", "Hilang": "hilang"}
        for baris in hasil:
            status = baris.get("status", "")
            self.tabel.insert("", "end", tags=(TAG.get(status, ""),), values=(
                baris.get("no_sesi",    baris.get("pertemuan", "—")),
                baris.get("tanggal",    "—"),
                baris.get("pokok_rps",  baris.get("pokok_bahasan", "—")),
                baris.get("materi_rps", "—"),
                baris.get("pokok_bap",  baris.get("pokok_bahasan_bap", "—")),
                baris.get("materi_bap", baris.get("materi", "—")),
                status,
                baris.get("keterangan", "—"),
            ))

    def tampilkan_data(self, hasil: list, persen: float = 0.0):
        """Dipanggil langsung oleh models.py jika menggunakan callback pattern."""
        self.hasil_validasi  = hasil
        self.persen_validasi = persen
        self._tampilkan_tabel(hasil)
        self.lbl_persen.configure(text=f"Kepatuhan: {persen:.1f}%")

def main():
    root = tk.Tk()
    AplikasiValidasiRPS(root)
    root.mainloop()

if __name__ == "__main__":
    main()