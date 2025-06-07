import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from io import BytesIO
import zipfile

st.title("Generator Banyak Surat CSR (ZIP)")

excel_file = st.file_uploader("Upload Excel (daftar perusahaan)", type="xlsx")
template_file = st.file_uploader("Upload Template Surat (Word .docx)", type="docx")

def generate_zip(template_file, data_rows):
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for row in data_rows:
            tpl = DocxTemplate(template_file)

            # Ambil data dengan nilai default jika tidak ada
            context = {
                "Nama_Perusahaan": row.get("Nama_Perusahaan", ""),
                "Nama_Direktur": row.get("Nama_Direktur", ""),  # Kosong jika tidak ada
                "Jabatan_Direktur": row.get("Jabatan_Direktur", "")  # Kosong jika tidak ada
            }

            tpl.render(context)

            doc_io = BytesIO()
            tpl.save(doc_io)
            doc_io.seek(0)

            # Buat nama file yang aman
            safe_nama = context["Nama_Perusahaan"].replace("/", "-")
            filename = f"Surat_{safe_nama}.docx"
            zip_file.writestr(filename, doc_io.read())

    zip_buffer.seek(0)
    return zip_buffer


if excel_file and template_file:
    df = pd.read_excel(excel_file)
    nama_perusahaan = df.iloc[:, 0].dropna().tolist()

    if st.button("Buat Surat"):
        hasil_zip = generate_zip(template_file, nama_perusahaan)

        st.download_button("Download Semua Surat (.zip)", hasil_zip, file_name="semua_surat.zip")
