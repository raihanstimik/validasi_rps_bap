from fpdf import FPDF

class ReportGenerator:
    def __init__(self):
        pass

    def export_pdf(self, file_path, results, persen):
        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        
        # Header Laporan
        pdf.cell(0, 10, "LAPORAN EVALUASI KESESUAIAN MATERI KULIAH (RPS VS BAP)", ln=True, align="C")
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 8, f"Tingkat Kepatuhan Kelayakan: {persen}%", ln=True, align="C")
        pdf.ln(5)

        # Header Tabel Matriks
        headers = ["SESI", "TANGGAL", "POKOK RPS", "MATERI RPS", "POKOK BAP", "MATERI BAP", "STATUS"]
        widths = [15, 25, 45, 50, 45, 50, 25]
        
        pdf.set_font("Arial", "B", 9)
        pdf.set_fill_color(30, 58, 138) # Warna Biru Tua
        pdf.set_text_color(255, 255, 255)
        
        for i, h in enumerate(headers):
            pdf.cell(widths[i], 8, h, border=1, align="C", fill=True)
        pdf.ln()

        # Isi Baris Data Berwarna Terang
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 8.5)
        
        for row in results:
            # Set warna background baris berdasarkan status kelulusan materi
            if row['status'] == "Sesuai":
                pdf.set_fill_color(209, 250, 229) # Hijau Terang
            elif row['status'] == "Tidak Sesuai":
                pdf.set_fill_color(254, 243, 199) # Kuning Terang
            else:
                pdf.set_fill_color(254, 226, 226) # Merah Terang
                
            pdf.cell(widths[0], 10, str(row['pert']), border=1, align="C", fill=True)
            pdf.cell(widths[1], 10, str(row['tgl']), border=1, align="C", fill=True)
            pdf.cell(widths[2], 10, str(row['rps_pokok'])[:25], border=1, fill=True)
            pdf.cell(widths[3], 10, str(row['rps_materi'])[:28], border=1, fill=True)
            pdf.cell(widths[4], 10, str(row['bap_pokok'] or "-")[:25], border=1, fill=True)
            pdf.cell(widths[5], 10, str(row['bap_materi'] or "-")[:28], border=1, fill=True)
            pdf.cell(widths[6], 10, str(row['status']), border=1, align="C", fill=True)
            pdf.ln()

        # Pembersihan String untuk mencegah crash unicode huruf ilegal
        pdf.output(file_path)
        return True