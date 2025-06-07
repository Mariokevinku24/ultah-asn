import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from io import BytesIO
import zipfile

st.title("Generator Banyak Surat CSR (ZIP)")

# Upload file
excel_file = st.file_uploader("Upload Excel (daftar perusahaan)", type="xlsx")
template_file = st.file_uploader("Upload Template Surat (Word .docx)", type="docx")

# Fungsi pembuat ZIP surat
def generate_zip(template_file, data_rows):
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for row in data_rows:
            tpl = DocxTemplate(template_file)

context = {
    "Nama_Perusahaan": row.get("Nama_Perusahaan", ""),
    "Nama_Direktur": row.get("Nama_Direktur", ""),
    "Jabatan_Direktur": row.get("Jabatan_Direktur", ""),
    "Kegiatan": row.get("Kegiatan", ""),
    "Lokasi": row.get("Lokasi", ""),
    "Jumlah_Sumbangan": row.get("Jumlah_Sumbangan", ""),
    "Jenis_Barang": row.get("Jenis_Barang", "")
}

            tpl.render(context)

            doc_io = BytesIO()
            tpl.save(doc_io)
            doc_io.seek(0)

            safe_nama = context["Nama_Perusahaan"].replace("/", "-").replace("\\", "-")
            filename = f"Surat_{safe_nama}.docx"
            zip_file.writestr(filename, doc_io.read())

    zip_buffer.seek(0)
    return zip_buffer

# Logika utama aplikasi
if excel_file and template_file:
    df = pd.read_excel(excel_file)
    df = df.fillna("")  # Hindari NaN

    # Filter baris yang Nama_Perusahaan-nya kosong
    df_valid = df[df["Nama_Perusahaan"].str.strip() != ""]

    if df_valid.empty:
        st.error("Tidak ada data perusahaan yang valid. Kolom 'Nama_Perusahaan' wajib diisi.")
    else:
        data_rows = df_valid.to_dict(orient="records")

        if st.button("Buat Surat"):
            hasil_zip = generate_zip(template_file, data_rows)

            st.download_button(
                label="Download Semua Surat (.zip)",
                data=hasil_zip,
                file_name="semua_surat_csr.zip",
                mime="application/zip"
            )
