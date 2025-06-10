from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# Buat dokumen
doc = Document()

# Ubah ukuran halaman menjadi Legal (21.59 cm x 35.56 cm)
section = doc.sections[0]
section.page_height = Cm(35.56)
section.page_width = Cm(21.59)
section.orientation = WD_ORIENT.PORTRAIT
section.left_margin = Cm(2.5)
section.right_margin = Cm(2.5)
section.top_margin = Cm(2.5)
section.bottom_margin = Cm(2.5)

# Judul
doc.add_heading('📋 SOP - Penerbitan Izin Pemanfaatan Air Limbah', level=1)

# Subjudul
doc.add_paragraph('### Bagian Proses dan Pelaksana (dengan simbol visual sederhana)')

# Data tabel
kotak = "🟦"
panah = "➡️"
diamond = "🔷"
dokumen = "📄"

data = [
    ["1", "Pemohon ajukan permohonan", kotak, "", "", "", "", "", "Dokumen Permohonan", "15 menit", "Tanda Terima"],
    ["2", "Meneruskan surat", "", kotak, "", "", "", "", "Surat", "15 menit", "-"],
    ["3", "Merancang surat persetujuan", "", "", kotak, "", "", "", "Draft", "2 hari", "Draft"],
    ["4", "Telaah dan beri persetujuan", "", "", "", kotak, "", "", "Draft", "1 hari", "Persetujuan"],
    ["5", "Verifikasi + Tinjauan Lapangan", "", kotak, "", "", "", "", "Form + Bukti Lapangan", "3 hari", "Berita Acara"],
    ["6", "Cek kelengkapan", kotak, "", "", "", "", "", "📄", "15 menit", "✔️ atau ❌"],
    ["7", "Keputusan Izin", "", kotak, "", "", diamond, "", "Naskah Izin", "1 hari", "Surat Izin"]
]

columns = ["No", "Kegiatan", "Kasubbid Perizinan", "Kabid WASDAL", "Sekretaris", "Kaban", "Kabag Hukum", "Bupati", "Kelengkapan", "Waktu", "Output"]

# Tambahkan tabel ke dokumen
table = doc.add_table(rows=1, cols=len(columns))
table.autofit = True

# Header
hdr_cells = table.rows[0].cells
for i, col in enumerate(columns):
    hdr_cells[i].text = col

# Baris isi
for row in data:
    row_cells = table.add_row().cells
    for i, item in enumerate(row):
        row_cells[i].text = str(item)

# Simpan dokumen
doc.save("SOP_Izin_Pemanfaatan_Air_Limbah_Legal.docx")
