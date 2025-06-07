import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from io import BytesIO
import zipfile
from num2words import num2words
import locale
from docx import Document
import os
import base64
import streamlit.components.v1 as components
from docx2pdf import convert  # Hanya di Windows/macOS

# Set locale ke Indonesia
try:
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
except:
    pass

st.title("📄 Generator Banyak Surat CSR (ZIP + Preview PDF + Terbilang)")

# Upload file
excel_file = st.file_uploader("📤 Upload Excel (daftar perusahaan)", type="xlsx")
template_file = st.file_uploader("📤 Upload Template Surat (Word .docx)", type="docx")

# Fungsi preview PDF dalam iframe
def preview_pdf_from_docx(template_file, data):
    tpl = DocxTemplate(template_file)

    jumlah = data.get("Jumlah_Sumbangan", 0)
    try:
        jumlah_float = float(jumlah)
    except:
        jumlah_float = 0.0

    jumlah_formatted = f"{jumlah_float:,.0f}".replace(",", ".")
    jumlah_terbilang = num2words(jumlah_float, lang='id').replace("koma nol", "").strip()

    context = {
        "Nama_Perusahaan": data.get("Nama_Perusahaan", ""),
        "Nama_Direktur": data.get("Nama_Direktur", ""),
        "Jabatan_Direktur": data.get("Jabatan_Direktur", ""),
        "Kegiatan": data.get("Kegiatan", ""),
        "Lokasi": data.get("Lokasi", ""),
        "Jumlah_Sumbangan": f"Rp. {jumlah_formatted},-",
        "Jumlah_Terbilang": jumlah_terbilang,
        "Jenis_Barang": data.get("Jenis_Barang", "")
    }

    tpl.render(context)

    docx_path = "preview_temp.docx"
    pdf_path = "preview_temp.pdf"
    tpl.save(docx_path)

    try:
        convert(docx_path, pdf_path)

        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")

        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        components.html(pdf_display, height=1000)

        os.remove(docx_path)
        os.remove(pdf_path)

    except Exception as e:
        st.error("Gagal mengubah ke PDF. Apakah Anda menjalankan di Windows/macOS dan punya Microsoft Word?")
        st.exception(e)

# Fungsi buat ZIP surat
def generate_zip(template_file, data_rows):
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for row in data_rows:
            tpl = DocxTemplate(template_file)

            jumlah = row.get("Jumlah_Sumbangan", 0)
            try:
                jumlah_float = float(jumlah)
            except:
                jumlah_float = 0.0

            jumlah_formatted = f"{jumlah_float:,.0f}".replace(",", ".")
            jumlah_terbilang = num2words(jumlah_float, lang='id').replace("koma nol", "").strip()

            context = {
                "Nama_Perusahaan": row.get("Nama_Perusahaan", ""),
                "Nama_Direktur": row.get("Nama_Direktur", ""),
                "Jabatan_Direktur": row.get("Jabatan_Direktur", ""),
                "Kegiatan": row.get("Kegiatan", ""),
                "Lokasi": row.get("Lokasi", ""),
                "Jumlah_Sumbangan": f"Rp. {jumlah_formatted},-",
                "Jumlah_Terbilang": jumlah_terbilang,
                "Jenis_Barang": row.get("Jenis_Barang", "")
            }

            try:
                tpl.render(context)
            except Exception as e:
                st.error(f"Gagal memproses surat untuk {context['Nama_Perusahaan']}: {e}")
                continue

            doc_io = BytesIO()
            tpl.save(doc_io)
            doc_io.seek(0)

            safe_nama = context["Nama_Perusahaan"].replace("/", "-").replace("\\", "-")
            filename = f"Surat_{safe_nama}.docx"
            zip_file.writestr(filename, doc_io.read())

    zip_buffer.seek(0)
    return zip_buffer

# Proses utama
if excel_file and template_file:
    df = pd.read_excel(excel_file)
    df = df.fillna("")

    required_columns = {"Nama_Perusahaan", "Nama_Direktur", "Jabatan_Direktur", "Kegiatan", "Lokasi", "Jumlah_Sumbangan", "Jenis_Barang"}
    if not required_columns.issubset(set(df.columns)):
        st.error(f"Kolom wajib tidak lengkap. Harus ada: {', '.join(required_columns)}")
    else:
        df_valid = df[df["Nama_Perusahaan"].str.strip() != ""]
        if df_valid.empty:
            st.error("Tidak ada data perusahaan yang valid. Kolom 'Nama_Perusahaan' wajib diisi.")
        else:
            data_rows = df_valid.to_dict(orient="records")
            st.success(f"✅ Ditemukan {len(data_rows)} data perusahaan.")
            st.dataframe(df_valid)

            if st.button("📄 Preview Surat Pertama (PDF)"):
                preview_pdf_from_docx(template_file, data_rows[0])

            if st.button("📦 Buat & Unduh Semua Surat (ZIP)"):
                hasil_zip = generate_zip(template_file, data_rows)
                st.download_button(
                    label="Download ZIP Surat",
                    data=hasil_zip,
                    file_name="semua_surat_csr.zip",
                    mime="application/zip"
                )

